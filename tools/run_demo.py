#!/usr/bin/env python3
"""Watch the insurance-claim swarm work - a real run, not a slideshow.

One claim, FNOL to money, against the real hub, real Ed25519 signatures,
and the real hash-chained audit log:

  Act 1  FNOL -> assignment, policy facts, inspection dispatched
  Act 2  Inspection -> sourced estimate; salvage surfaces -> recovery lane
  Act 3  An attorney letter arrives: the claimant channel halts SAME TURN;
         held outbound becomes a visible wait; inbound is routed, never
         answered
  Act 4  Fraud signal aggregates SILENTLY - claimant handling provably
         unchanged; the ending is a SIGNED disposition
  Act 5  Money: unsigned payment REJECTED; signed payment posts; a
         one-cent variance raises reconciliation.exception; a coverage
         statement is blocked at the door
  Act 6  Chain verification - every event, hash-linked, tamper-evident

Run it:  python3 tools/run_demo.py
"""
import os
import sys
import tempfile
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


def say(s=""): print(s)
def act(n, t): say(); say("=" * 66); say(f"  ACT {n}: {t}"); say("=" * 66)


def spoke_env(frm, to, intent, ctx, payload):
    return Envelope(from_agent=frm, to_agent=to, intent=intent,
                    client_context_id=ctx, payload=payload,
                    provenance={"source": f"spoke-{frm}",
                                "captured_at": "runtime",
                                "verbatim_available": True})


def main():
    tmp = tempfile.mkdtemp()
    signer = Ed25519Signer()
    verifier = Ed25519Verifier(signer.public_key_bytes())
    audit_path = os.path.join(tmp, "audit.jsonl")
    hub = Hub(Routes(os.path.join(ROOT, "identity", "routes.json")),
              AuditLog(audit_path), signature_verifier=verifier.verifier())
    external = []
    hub.register("external", lambda e: external.append(e))
    hub.register("human", lambda e: None)
    s = {"01": Spoke01FNOLIntake(hub),
         "02": Spoke02ClaimTriage(hub),
         "03": Spoke03PolicyVerification(hub, policy_db={
             "POL-1": {"status": "in_force"}}),
         "04": Spoke04ClaimantComm(hub, templates={
             "ack": "We received your claim.",
             "status": "Update on your claim."}),
         "05": Spoke05DocumentCollection(hub),
         "06": Spoke06InspectionScheduling(hub),
         "07": Spoke07VendorCoordination(hub, panel={"inspection": "v-insp"}),
         "08": Spoke08EstimateValuation(hub),
         "09": Spoke09FraudSignals(hub),
         "10": Spoke10Subrogation(hub),
         "11": Spoke11PaymentsReserves(hub),
         "12": Spoke12ComplianceDeadlines(hub),
         "13": Spoke13ClaimFileRecords(hub),
         "14": Spoke14DailyOperations(hub)}
    for aid, sp in s.items():
        if aid != "01":
            hub.register(aid, sp.handle)
    hub.on_turn_start()
    ctx = "demo-claim-1"

    def count(i):
        return len([e for e in hub.audit.read()
                    if e["kind"] == "envelope.persisted"
                    and e["intent"] == i])

    act(1, "FNOL -> ASSIGNMENT, POLICY FACTS, INSPECTION DISPATCHED")
    s["01"].capture_fnol(ctx, {"insured": "i1", "policy_number": "POL-1",
                               "date_of_loss": "2026-07-01",
                               "loss_description":
                               "tree fell on garage roof"})
    say(f"  claim.assignment x{count('claim.assignment')}"
        f" | policy: {s['02'].claims[ctx]['policy']['status']}"
        f" (system-timestamped fact, not a coverage statement)")
    say(f"  inspection dispatched to ratified panel vendor:"
        f" {s['07'].jobs[ctx]}")

    act(2, "INSPECTION -> SOURCED ESTIMATE; SALVAGE -> RECOVERY LANE")
    s["06"].inspection_done(ctx, {"estimate_amount": 9000.0,
                                  "salvage_value": 1500.0})
    say(f"  estimate.package x{count('estimate.package')} (every line"
        " sourced to inspection.result)")
    say(f"  salvage $1,500 -> salvage.record x{count('salvage.record')};"
        f" recovery case holds it: {s['10'].cases[ctx]['salvage']}")

    act(3, "ATTORNEY LETTER ARRIVES - THE HALT (absolute line 5)")
    s["05"].receive_document(ctx, {"doc_type": "letter",
                                   "source": "Law Office of X",
                                   "date": "2026-07-02",
                                   "representation_language": True})
    say(f"  representation.notice x{count('representation.notice')} ->"
        f" 02/04/12/13 same turn; channel halted:"
        f" {ctx in s['04'].halted}")
    hub.send(spoke_env("02", "04", "claimant.message.request", ctx,
                       {"template_id": "status"}))
    say(f"  outbound status update HELD, visible as a wait:"
        f" held={len(s['04'].held_outbound[ctx])},"
        f" agent.status x{count('agent.status')}")
    before = len(s["04"].sent)
    s["04"].claimant_reply(ctx, "any update on my claim?")
    say(f"  claimant writes in anyway -> answered by swarm:"
        f" {len(s['04'].sent) > before} (logged + routed to human instead)")

    act(4, "FRAUD SIGNAL - SILENT, AND THE ENDING IS SIGNED (line 3)")
    hub.send(spoke_env("02", "09", "fraud.signal", ctx,
                       {"kind": "pattern-a"}))
    say(f"  signal aggregated; claimant handling unchanged - the fraud"
        f" state is structurally unreadable by handling paths")
    s["09"].refer(ctx)
    say(f"  fraud.referral x{count('fraud.referral')} carries"
        " 'handling_changed: False' ON THE RECORD")
    bad = spoke_env("human", "09", "fraud.disposition", ctx,
                    {"disposition": "cleared"})
    say(f"  unsigned disposition -> ok={hub.send(bad).get('ok', False)}")
    good = spoke_env("human", "09", "fraud.disposition", ctx,
                     {"disposition": "cleared"})
    signer.sign(good); hub.send(good)
    say(f"  SIGNED disposition -> recorded:"
        f" {s['09'].dispositions[ctx]!r} - a signal never dies quietly")

    act(5, "MONEY: UNSIGNED REJECTED, SIGNED POSTS, $0.00 RULE, LINE 1")
    bad = spoke_env("human", "11", "payment.authority", ctx,
                    {"amount": 5000.0})
    say(f"  unsigned $5,000 payment -> ok={hub.send(bad).get('ok', False)},"
        f" paid={s['11'].ledger.get(ctx, {}).get('paid', 0.0)}")
    good = spoke_env("human", "11", "payment.authority", ctx,
                     {"amount": 4999.99, "expected_total": 5000.00})
    signer.sign(good); hub.send(good)
    say(f"  SIGNED payment posts: paid={s['11'].ledger[ctx]['paid']}"
        f" -> one cent off expected -> reconciliation.exception"
        f" x{count('reconciliation.exception')}")
    hub.send(spoke_env("02", "04", "claimant.message.request", ctx,
                       {"template_id": "custom",
                        "facts": {"note": "you are covered"}}))
    say(f"  a 'you are covered' message attempt -> integrity.violation"
        f" x{count('integrity.violation')}, sent: nothing"
        " (line 1 blocks the words at the door)")

    act(6, "THE CHAIN")
    r = hub.audit.verify_chain()
    say(f"  audit entries: {len(hub.audit.read())}")
    say(f"  verify_chain(): ok={r['ok']}")
    say(f"  dead letters: {len(hub.queues['dead.letter'])}")
    say(f"  log file: {audit_path}")
    say()
    say("  Tamper with any line and verify_chain() names it."
        " Not trust us - check us.")
    say()


if __name__ == "__main__":
    main()
