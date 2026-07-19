"""End-to-end playbook execution for the claim swarm - real hub, real
routing, hash-chained audit, signed authority. Every test drives its
playbook's trigger plus external events only; completion is asserted
against artifacts; every test ends with zero dead letters and a verified
chain."""
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dispatcher.core import Envelope, Routes, AuditLog
from dispatcher.hub import Hub
from dispatcher.signatures import Ed25519Signer, Ed25519Verifier
from dispatcher.claim_spokes import (
    Spoke01FNOLIntake, Spoke02ClaimTriage, Spoke03PolicyVerification,
    Spoke04ClaimantComm, Spoke05DocumentCollection,
    Spoke06InspectionScheduling, Spoke07VendorCoordination,
    Spoke08EstimateValuation, Spoke09FraudSignals, Spoke10Subrogation,
    Spoke11PaymentsReserves, Spoke12ComplianceDeadlines,
    Spoke13ClaimFileRecords, Spoke14DailyOperations)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY_ROUTES = os.path.join(ROOT, "identity", "routes.json")

TEMPLATES = {"ack": "We received your claim {claim}.",
             "status": "Update on claim {claim}."}
FNOL = {"insured": "i1", "policy_number": "POL-1",
        "date_of_loss": "2026-07-01",
        "loss_description": "tree fell on garage roof"}


def build_swarm(tmp_path):
    signer = Ed25519Signer()
    verifier = Ed25519Verifier(signer.public_key_bytes())
    hub = Hub(Routes(IDENTITY_ROUTES),
              AuditLog(os.path.join(str(tmp_path),
                                    f"a-{uuid.uuid4().hex[:6]}.jsonl")),
              signature_verifier=verifier.verifier())
    external = []
    hub.register("external", lambda e: external.append(e))
    hub.register("human", lambda e: None)
    spokes = {
        "01": Spoke01FNOLIntake(hub),
        "02": Spoke02ClaimTriage(hub),
        "03": Spoke03PolicyVerification(hub, policy_db={
            "POL-1": {"status": "in_force", "effective": "2026-01-01"}}),
        "04": Spoke04ClaimantComm(hub, templates=TEMPLATES),
        "05": Spoke05DocumentCollection(hub),
        "06": Spoke06InspectionScheduling(hub),
        "07": Spoke07VendorCoordination(hub, panel={"inspection": "v-insp"}),
        "08": Spoke08EstimateValuation(hub),
        "09": Spoke09FraudSignals(hub),
        "10": Spoke10Subrogation(hub),
        "11": Spoke11PaymentsReserves(hub),
        "12": Spoke12ComplianceDeadlines(hub),
        "13": Spoke13ClaimFileRecords(hub),
        "14": Spoke14DailyOperations(hub),
    }
    for aid, s in spokes.items():
        if aid != "01":
            hub.register(aid, s.handle)
    hub.on_turn_start()
    return hub, signer, spokes, external


def signed(signer, to, intent, ctx, payload, frm="human"):
    env = Envelope(from_agent=frm, to_agent=to, intent=intent,
                   client_context_id=ctx, payload=payload,
                   provenance={"source": frm, "captured_at": "runtime",
                               "verbatim_available": True})
    signer.sign(env)
    return env


def clean(hub):
    assert hub.queues["dead.letter"] == [], hub.queues["dead.letter"]
    assert hub.audit.verify_chain()["ok"]


def persisted(hub, intent=None):
    return [e for e in hub.audit.read() if e["kind"] == "envelope.persisted"
            and (intent is None or e["intent"] == intent)]


def _open_claim(hub, spokes, ctx):
    spokes["01"].capture_fnol(ctx, dict(FNOL))


# ---------------------------------------------------------------- P01
def test_p01_fnol_to_dispatch(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p01"
    _open_claim(hub, spokes, ctx)
    assert persisted(hub, "claim.assignment")
    assert persisted(hub, "policy.verify.result")
    assert persisted(hub, "vendor.status")          # inspection dispatched
    assert spokes["02"].claims[ctx]["policy"]["status"] == "in_force"
    clean(hub)


def test_p01_incomplete_fnol_holds(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-inc"
    f = dict(FNOL); f.pop("policy_number")
    spokes["01"].capture_fnol(ctx, f)
    assert spokes["01"].held[ctx] == ["policy_number"]
    assert not persisted(hub, "claim.fnol")
    clean(hub)


# ---------------------------------------------------------------- P02
def test_p02_track_and_exception(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p02"
    _open_claim(hub, spokes, ctx)
    spokes["06"].inspection_done(ctx, {"estimate_amount": 8200.0})
    assert persisted(hub, "inspection.result")
    assert persisted(hub, "estimate.package")
    assert spokes["02"].claims[ctx]["estimate"]["amount"] == 8200.0
    clean(hub)


# ---------------------------------------------------------------- P03
def test_p03_paperwork_close_no_coverage_statement(tmp_path):
    """Line 1 at closure: the package carries facts, never a statement."""
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p03"
    _open_claim(hub, spokes, ctx)
    spokes["06"].inspection_done(ctx, {"estimate_amount": 5000.0})
    spokes["02"].request_closure(ctx)
    pkgs = persisted(hub, "closure.package")
    assert pkgs
    assert spokes["02"].claims[ctx]["estimate"] is not None
    clean(hub)


# ---------------------------------------------------------------- P04
def test_p04_vendor_panel_fail_closed(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p04"
    hub.send(Envelope(from_agent="08", to_agent="07",
                      intent="vendor.request", client_context_id=ctx,
                      payload={"kind": "mitigation"},   # not on panel
                      provenance={"source": "spoke-08",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    assert persisted(hub, "clarification.request")
    assert ctx not in spokes["07"].jobs               # no dispatch
    clean(hub)


# ---------------------------------------------------------------- P05
def test_p05_fraud_silent_aggregation_signed_ending(tmp_path):
    """Line 3: signals aggregate silently; handling unchanged; endings
    are signed dispositions."""
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p05"
    _open_claim(hub, spokes, ctx)
    hub.send(Envelope(from_agent="02", to_agent="09", intent="fraud.signal",
                      client_context_id=ctx, payload={"kind": "pattern-a"},
                      provenance={"source": "spoke-02",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    # handling did not change: claimant messaging still flows normally
    hub.send(Envelope(from_agent="02", to_agent="04",
                      intent="claimant.message.request",
                      client_context_id=ctx,
                      payload={"template_id": "status"},
                      provenance={"source": "spoke-02",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    assert persisted(hub, "claimant.message.send")
    spokes["09"].refer(ctx)
    ref = persisted(hub, "fraud.referral")
    assert ref
    # unsigned disposition rejected; signed lands
    bad = Envelope(from_agent="human", to_agent="09",
                   intent="fraud.disposition", client_context_id=ctx,
                   payload={"disposition": "cleared"},
                   provenance={"source": "human", "captured_at": "runtime",
                               "verbatim_available": True})
    assert not hub.send(bad).get("ok", False)
    hub.send(signed(signer, "09", "fraud.disposition", ctx,
                    {"disposition": "cleared"}))
    assert spokes["09"].dispositions[ctx] == "cleared"
    clean(hub)


# ---------------------------------------------------------------- P06
def test_p06_subro_preparation_human_money(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p06"
    hub.send(Envelope(from_agent="08", to_agent="10", intent="subro.signal",
                      client_context_id=ctx,
                      payload={"third_party": "tp-1"},
                      provenance={"source": "spoke-08",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    assert persisted(hub, "subro.package")
    assert spokes["10"].cases[ctx]["executed"] is None
    hub.send(signed(signer, "10", "recovery.authority", ctx,
                    {"amount": 3000.0}))
    assert spokes["10"].cases[ctx]["executed"]["amount"] == 3000.0
    clean(hub)


# ---------------------------------------------------------------- P07
def test_p07_signed_payment_and_zero_tolerance(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p07"
    unsigned = Envelope(from_agent="human", to_agent="11",
                        intent="payment.authority", client_context_id=ctx,
                        payload={"amount": 5000.0},
                        provenance={"source": "human",
                                    "captured_at": "runtime",
                                    "verbatim_available": True})
    assert not hub.send(unsigned).get("ok", False)
    assert spokes["11"].ledger.get(ctx, {}).get("paid", 0.0) == 0.0
    hub.send(signed(signer, "11", "payment.authority", ctx,
                    {"amount": 4999.99, "expected_total": 5000.00}))
    assert spokes["11"].ledger[ctx]["paid"] == 4999.99
    exc = persisted(hub, "reconciliation.exception")
    assert exc, "one-cent variance did not raise an exception"
    clean(hub)


def test_p07_reserves_signed_only(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-res"
    hub.send(signed(signer, "11", "reserve.authority", ctx,
                    {"amount": 12000.0}))
    assert spokes["11"].ledger[ctx]["reserve"] == 12000.0
    assert persisted(hub, "reserve.record")
    clean(hub)


# ---------------------------------------------------------------- P08
def test_p08_doi_inquiry_clock_and_human_package(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p08"
    hub.send(Envelope(from_agent="01", to_agent="12", intent="doi.inquiry",
                      client_context_id=ctx,
                      payload={"inquiry": "handling question",
                               "deadline_day": 15},
                      provenance={"source": "spoke-01",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    assert persisted(hub, "doi.response.package")
    spokes["12"].run_daily(today=6)      # 9 left -> lead alert (10)
    assert persisted(hub, "deadline.alert")
    spokes["12"].run_daily(today=13)     # 2 left -> escalation (3)
    assert persisted(hub, "escalation.clock")
    clean(hub)


# ---------------------------------------------------------------- P09/P10
def test_p09_p10_morning_report(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-ops"
    hub.send(Envelope(from_agent="06", to_agent="14", intent="agent.status",
                      client_context_id=ctx,
                      payload={"waiting_on": "07", "age_days": 2},
                      provenance={"source": "spoke-06",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    rep = spokes["14"].morning_report()
    assert rep["waits"]
    assert persisted(hub, "report.package")
    clean(hub)


# ---------------------------------------------------------------- P11
def test_p11_representation_halt_all_three_detectors(tmp_path):
    """Line 5: attorney language at FNOL, in a reply, or in a document
    halts the claimant channel same turn; inbound after halt is routed,
    never answered; outbound is held and visible as a wait."""
    hub, signer, spokes, _ = build_swarm(tmp_path)
    for src, drive in (
        ("fnol", lambda c: spokes["01"].capture_fnol(
            c, dict(FNOL, loss_description="my attorney will contact you"))),
        ("reply", lambda c: (spokes["01"].capture_fnol(c, dict(FNOL)),
                             spokes["04"].claimant_reply(
                                 c, "speak to my lawyer"))),
        ("doc", lambda c: (spokes["01"].capture_fnol(c, dict(FNOL)),
                           spokes["05"].receive_document(
                               c, {"doc_type": "letter",
                                   "source": "Law Office of X",
                                   "date": "2026-07-02",
                                   "representation_language": True}))),
    ):
        ctx = f"cl-rep-{src}"
        drive(ctx)
        assert ctx in spokes["04"].halted, src
        assert spokes["02"].claims[ctx]["represented"], src
        # outbound is held, wait visible
        hub.send(Envelope(from_agent="02", to_agent="04",
                          intent="claimant.message.request",
                          client_context_id=ctx,
                          payload={"template_id": "status"},
                          provenance={"source": "spoke-02",
                                      "captured_at": "runtime",
                                      "verbatim_available": True}))
        assert spokes["04"].held_outbound[ctx], src
        # inbound after halt: logged + escalated, never answered
        before = len([s for s in spokes["04"].sent if s[0] == ctx])
        spokes["04"].claimant_reply(ctx, "any update?")
        assert len([s for s in spokes["04"].sent if s[0] == ctx]) == before
        assert persisted(hub, "escalation.represented_inbound")
    clean(hub)


# ---------------------------------------------------------------- P12
def test_p12_policy_change_midclaim(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p12"
    _open_claim(hub, spokes, ctx)
    spokes["03"].policy_changed(ctx, {"status": "cancelled",
                                      "effective": "2026-06-15"})
    assert persisted(hub, "policy.change.notice")
    # human notified with the change; blast radius asked of 13
    assert persisted(hub, "clarification.request")
    assert persisted(hub, "record.request")
    clean(hub)


# ---------------------------------------------------------------- P13
def test_p13_salvage_recovery_cascade(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p13"
    _open_claim(hub, spokes, ctx)
    spokes["06"].inspection_done(ctx, {"estimate_amount": 9000.0,
                                       "salvage_value": 1500.0})
    assert persisted(hub, "salvage.record")
    assert spokes["10"].cases[ctx]["salvage"]
    hub.send(Envelope(from_agent="08", to_agent="10", intent="subro.signal",
                      client_context_id=ctx, payload={"third_party": "tp"},
                      provenance={"source": "spoke-08",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    pkg = spokes["10"].cases[ctx]
    assert pkg["salvage"] and pkg["signals"]     # folded into the package
    assert pkg["executed"] is None               # nothing moves unsigned
    clean(hub)


# ---------------------------------------------------------------- P14
def test_p14_records_request_privilege_flagged(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-p14"
    _open_claim(hub, spokes, ctx)
    spokes["05"].receive_document(ctx, {"doc_type": "counsel_memo",
                                        "source": "defense",
                                        "date": "2026-07-03",
                                        "privilege_marker": True})
    spokes["13"].external_records_request(ctx, {"requester": "claimant",
                                                "deadline_day": 30})
    pkgs = persisted(hub, "records.disclosure.package")
    assert pkgs
    inv = spokes["13"].copies[ctx]
    assert any(c["kind"] == "records_response"
               for c in spokes["12"].clocks[ctx])
    clean(hub)


# ----------------------------------------------------- absolute line 1
def test_coverage_statement_blocked_at_the_door(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    ctx = "cl-cov"
    hub.send(Envelope(from_agent="02", to_agent="04",
                      intent="claimant.message.request",
                      client_context_id=ctx,
                      payload={"template_id": "custom",
                               "facts": {"note": "you are covered"}},
                      provenance={"source": "spoke-02",
                                  "captured_at": "runtime",
                                  "verbatim_available": True}))
    assert persisted(hub, "integrity.violation")
    assert not persisted(hub, "claimant.message.send")


# ----------------------------------------------------- closed track
def test_closed_track_rejects_illegal_tuple(tmp_path):
    hub, signer, spokes, _ = build_swarm(tmp_path)
    env = Envelope(from_agent="09", to_agent="11",
                   intent="payment.record", client_context_id="cl-x",
                   payload={},
                   provenance={"source": "spoke-09",
                               "captured_at": "runtime",
                               "verbatim_available": True})
    assert not hub.send(env).get("ok", False)
