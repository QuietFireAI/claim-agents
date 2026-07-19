"""Real spokes for the insurance-claim (P&C) vertical, built against the
ratified v0.2 spec (44 routes, P01-P14) - agent by agent, gate by gate.

Scope honesty (TUNING_MANUAL TOP OF LIST): every playbook path P01-P14
plus the hard gates. Exhaustive per-tuple depth (92 tuples) is the next
pass, tracked, not pretended.

The five absolute lines, in code:
  1. No coverage statements       -> no spoke has a coverage-statement
                                     path; determinations are licensed
                                     humans; 04's guard rejects the words.
  2. No unsigned money            -> 11 (payments/reserves) and 10
                                     (recovery) execute only on
                                     hub-verified signed authority.
  3. Handling never changes on suspicion -> 09 aggregates silently;
                                     nothing downstream reads fraud
                                     state; endings are signed
                                     dispositions.
  4. Clocks never slip silently   -> 12 alerts at lead-time and
                                     escalates before the miss.
  5. Represented claimants are human-only -> representation.notice halts
                                     04 claim-wide same turn; inbound is
                                     logged and routed, never answered.
"""
from __future__ import annotations

from .core import Envelope

UNKNOWN = "unknown"
SOURCE_VERIFIED = "source_verified"

_REPRESENTATION_WORDS = ("attorney", "my lawyer", "law office", "counsel",
                         "represented by", "letter of representation")
_INJURY_WORDS = ("injury", "injured", "hospital", "ambulance", "hurt")
_COVERAGE_WORDS = ("you are covered", "this is covered", "we will pay",
                   "policy covers this", "fully covered")


def _env(frm, to, intent, ctx, payload, confidence=UNKNOWN,
         escalation_flag=False):
    return Envelope(from_agent=frm, to_agent=to, intent=intent,
                    client_context_id=ctx, payload=payload,
                    confidence=confidence, escalation_flag=escalation_flag,
                    provenance={"source": f"spoke-{frm}",
                                "captured_at": "runtime",
                                "verbatim_available": True})


# ------------------------------------------------------------------ 01
class Spoke01FNOLIntake:
    """First notice of loss. Captures verbatim; detects representation and
    injury language at the front door; never states coverage."""

    REQUIRED = ("insured", "policy_number", "date_of_loss", "loss_description")

    def __init__(self, hub):
        self.hub = hub
        self.held = {}
        hub.register("01", self.handle)

    def capture_fnol(self, ctx, fnol):
        text = str(fnol.get("loss_description", "")).lower()
        if any(w in text for w in _REPRESENTATION_WORDS):
            for to in ("02", "04", "12", "13"):
                self.hub.send(_env("01", to, "representation.notice", ctx,
                                   {"verbatim": fnol["loss_description"],
                                    "source": "fnol"}))
        if any(w in text for w in _INJURY_WORDS):
            self.hub.send(_env("01", "queue", "escalation.injury", ctx,
                               {"verbatim": fnol["loss_description"]},
                               escalation_flag=True))
        missing = [f for f in self.REQUIRED if not fnol.get(f)]
        if missing:
            self.held[ctx] = missing
            self.hub.send(_env("01", "queue", "clarification.request", ctx,
                               {"reason": "incomplete_fnol",
                                "missing": missing}))
            return
        self.hub.send(_env("01", "02", "claim.fnol", ctx,
                           {"fnol": dict(fnol), "captured_verbatim": True},
                           confidence=SOURCE_VERIFIED))
        self.hub.send(_env("01", "13", "interaction.log", ctx,
                           {"event": "fnol_captured"}))

    def handle(self, env):
        return  # record.response informational


# ------------------------------------------------------------------ 02
class Spoke02ClaimTriage:
    """Claim owner. Assigns, tracks posture (incl. represented), never
    determines coverage - it routes the question to the human."""

    def __init__(self, hub):
        self.hub = hub
        self.claims = {}

    def _st(self, ctx):
        return self.claims.setdefault(ctx, {
            "assigned": False, "represented": False, "policy": None,
            "estimate": None, "closed": False})

    def handle(self, env):
        ctx = env.client_context_id
        st = self._st(ctx)
        if env.intent == "claim.fnol":
            st["assigned"] = True
            for to in ("06", "12", "13"):
                self.hub.send(_env("02", to, "claim.assignment", ctx,
                                   {"severity": "standard"}))
            self.hub.send(_env("02", "03", "policy.verify.request", ctx,
                               {"policy_number":
                                env.payload["fnol"]["policy_number"]}))
        elif env.intent == "representation.notice":
            st["represented"] = True
            self.hub.send(_env("02", "13", "interaction.log", ctx,
                               {"event": "posture_represented"}))
            self.hub.send(_env("02", "human", "closure.package", ctx,
                               {"kind": "representation_handoff",
                                "held_inventory_requested": True},
                               escalation_flag=True))
        elif env.intent == "policy.verify.result":
            st["policy"] = env.payload
        elif env.intent == "policy.change.notice":
            # blast radius: ask 13 for affected items; human gets the change
            self.hub.send(_env("02", "13", "record.request", ctx,
                               {"scope": "anchored_on_prior_policy"}))
            self.hub.send(_env("02", "queue", "clarification.request", ctx,
                               {"reason": "policy_changed_midclaim",
                                "facts": env.payload},
                               escalation_flag=True))
        elif env.intent == "estimate.package":
            st["estimate"] = env.payload
        elif env.intent in ("vendor.status", "deadline.alert",
                            "claimant.reply", "record.response",
                            "cat.event", "doc.received"):
            st.setdefault("events", []).append(env.intent)

    def request_closure(self, ctx):
        st = self._st(ctx)
        pkg = {"policy_facts": st["policy"], "estimate": st["estimate"],
               "coverage_statement": None}   # line 1: never
        self.hub.send(_env("02", "human", "closure.package", ctx, pkg,
                           escalation_flag=True))
        self.hub.send(_env("02", "13", "closure.package", ctx, pkg))


# ------------------------------------------------------------------ 03
class Spoke03PolicyVerification:
    """Policy facts with system timestamps; discrepancies are reported,
    never argued; mid-claim changes fire the blast-radius lane."""

    def __init__(self, hub, policy_db=None):
        self.hub = hub
        self.db = policy_db or {}

    def handle(self, env):
        if env.intent != "policy.verify.request":
            return
        ctx = env.client_context_id
        res = dict(self.db.get(env.payload["policy_number"],
                               {"status": "unknown",
                                "reason": "not_on_file"}))
        res["ts"] = "runtime"
        for to in ("02", "13") if env.from_agent == "02" else ("08", "13"):
            self.hub.send(_env("03", to, "policy.verify.result", ctx, res,
                               confidence=SOURCE_VERIFIED
                               if res.get("status") != "unknown" else UNKNOWN))

    def policy_changed(self, ctx, new_facts):
        res = dict(new_facts); res["ts"] = "runtime"; res["changed"] = True
        for to in ("02", "08", "12", "13"):
            self.hub.send(_env("03", to, "policy.change.notice", ctx, res,
                               confidence=SOURCE_VERIFIED))


# ------------------------------------------------------------------ 04
class Spoke04ClaimantComm:
    """Claimant-facing hub. Absolute lines 1 and 5 live here: no coverage
    words ever leave; representation halts the channel same turn."""

    def __init__(self, hub, templates=None):
        self.hub = hub
        self.templates = templates or {}
        self.halted = set()          # ctx with representation posture
        self.held_outbound = {}      # ctx -> [held messages]
        self.sent = []

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent == "representation.notice":
            self.halted.add(ctx)     # claim-wide, same turn
            return
        if env.intent == "claimant.message.request":
            body = self.templates.get(env.payload.get("template_id"),
                                      env.payload.get("template_id", ""))
            low = str(body).lower() + str(env.payload).lower()
            if any(w in low for w in _COVERAGE_WORDS):
                # line 1: the words themselves are rejected at the door
                self.hub.send(_env("04", "queue", "integrity.violation", ctx,
                                   {"reason": "coverage_statement_blocked",
                                    "requested_by": env.from_agent},
                                   escalation_flag=True))
                return
            if ctx in self.halted:
                self.held_outbound.setdefault(ctx, []).append(env.payload)
                self.hub.send(_env("04", "14", "agent.status", ctx,
                                   {"waiting_on": "human",
                                    "reason": "represented_halt",
                                    "held": len(self.held_outbound[ctx])}))
                return
            out = {"template_id": env.payload.get("template_id"),
                   "body": body, "facts": env.payload.get("facts", {})}
            self.sent.append((ctx, out))
            self.hub.send(_env("04", "external", "claimant.message.send",
                               ctx, out))
            self.hub.send(_env("04", "13", "interaction.log", ctx,
                               {"event": "claimant_message",
                                "template": out["template_id"]}))

    def claimant_reply(self, ctx, text):
        low = text.lower()
        if any(w in low for w in _REPRESENTATION_WORDS):
            for to in ("02", "04", "12", "13"):
                self.hub.send(_env("04", to, "representation.notice", ctx,
                                   {"verbatim": text, "source": "claimant"}))
            return
        if ctx in self.halted:
            # inbound after halt: logged and routed verbatim, never answered
            self.hub.send(_env("04", "13", "interaction.log", ctx,
                               {"event": "inbound_while_represented",
                                "verbatim": text}))
            self.hub.send(_env("04", "queue", "escalation.represented_inbound",
                               ctx, {"verbatim": text},
                               escalation_flag=True))
            return
        for to in ("02", "05", "06"):
            self.hub.send(_env("04", to, "claimant.reply", ctx,
                               {"verbatim": text}))


# ------------------------------------------------------------------ 05
class Spoke05DocumentCollection:
    """Evidence pipeline. Attorney letterhead in documents fires the
    representation lane; privilege markers are flagged, never judged."""

    def __init__(self, hub):
        self.hub = hub
        self.inventory = {}

    def handle(self, env):
        if env.intent == "doc.request":
            self.inventory.setdefault(env.client_context_id, []).append(
                {"requested": env.payload.get("doc_type"),
                 "by": env.from_agent, "status": "requested"})

    def receive_document(self, ctx, doc):
        text = str(doc.get("source", "")).lower() + \
            str(doc.get("doc_type", "")).lower()
        if doc.get("representation_language") or "law office" in text:
            for to in ("02", "04", "12", "13"):
                self.hub.send(_env("05", to, "representation.notice", ctx,
                                   {"source": "document",
                                    "doc_type": doc.get("doc_type")}))
        item = {"doc_type": doc.get("doc_type"), "date": doc.get("date"),
                "source": doc.get("source"), "status": "received",
                "privilege_flag": bool(doc.get("privilege_marker"))}
        self.inventory.setdefault(ctx, []).append(item)
        for to in ("02", "08", "13"):
            self.hub.send(_env("05", to, "doc.received", ctx, item,
                               confidence=SOURCE_VERIFIED))


# ------------------------------------------------------------------ 06
class Spoke06InspectionScheduling:
    def __init__(self, hub):
        self.hub = hub
        self.scheduled = {}

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent in ("claim.assignment", "inspection.schedule"):
            if ctx in self.scheduled:
                return
            self.scheduled[ctx] = "requested"
            self.hub.send(_env("06", "07", "vendor.request", ctx,
                               {"kind": "inspection"}))
        elif env.intent == "claimant.reply":
            pass

    def inspection_done(self, ctx, result):
        self.scheduled[ctx] = "complete"
        for to in ("08", "13"):
            self.hub.send(_env("06", to, "inspection.result", ctx,
                               dict(result), confidence=SOURCE_VERIFIED))


# ------------------------------------------------------------------ 07
class Spoke07VendorCoordination:
    def __init__(self, hub, panel=None):
        self.hub = hub
        self.panel = panel or {}     # kind -> vendor id (ratified panel)
        self.jobs = {}

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent != "vendor.request":
            return
        kind = env.payload["kind"]
        vendor = self.panel.get(kind)
        if vendor is None:
            # fail-closed: no panel entry = no dispatch, human review
            self.hub.send(_env("07", "queue", "clarification.request", ctx,
                               {"reason": "no_ratified_vendor",
                                "kind": kind}, escalation_flag=True))
            return
        self.jobs[ctx] = {"kind": kind, "vendor": vendor}
        for to in ("02", "08", "13"):
            self.hub.send(_env("07", to, "vendor.status", ctx,
                               {"kind": kind, "vendor": vendor,
                                "status": "dispatched"}))


# ------------------------------------------------------------------ 08
class Spoke08EstimateValuation:
    """Numbers with sources. Salvage surfaces here; deltas are facts."""

    def __init__(self, hub):
        self.hub = hub
        self.facts = {}

    def handle(self, env):
        ctx = env.client_context_id
        st = self.facts.setdefault(ctx, {"inspection": None, "docs": []})
        if env.intent == "inspection.result":
            st["inspection"] = env.payload
            pkg = {"amount": env.payload.get("estimate_amount"),
                   "basis": "inspection.result",
                   "line_items_sourced": True}
            for to in ("02", "11", "13"):
                self.hub.send(_env("08", to, "estimate.package", ctx, pkg,
                                   confidence=SOURCE_VERIFIED))
            if env.payload.get("salvage_value"):
                for to in ("10", "13"):
                    self.hub.send(_env("08", to, "salvage.record", ctx,
                                       {"salvage_value":
                                        env.payload["salvage_value"],
                                        "source": "inspection"}))
        elif env.intent == "doc.received":
            st["docs"].append(env.payload)
        elif env.intent == "policy.change.notice":
            st["policy_change"] = env.payload


# ------------------------------------------------------------------ 09
class Spoke09FraudSignals:
    """Silent aggregation, signed endings. NOTHING here is readable by
    handling paths - line 3 is structural: no other spoke references
    this state, and this spoke sends only referrals and logs."""

    def __init__(self, hub):
        self.hub = hub
        self.signals = {}
        self.dispositions = {}

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent == "fraud.signal":
            self.signals.setdefault(ctx, []).append(env.payload)
        elif env.intent == "fraud.disposition":
            # hub verified the signature; a signal's ending is signed
            self.dispositions[ctx] = env.payload["disposition"]
            self.hub.send(_env("09", "13", "interaction.log", ctx,
                               {"event": "fraud_disposition_signed",
                                "disposition": env.payload["disposition"]}))

    def refer(self, ctx):
        pkg = {"signals": list(self.signals.get(ctx, [])),
               "handling_changed": False}     # line 3, stated on the record
        self.hub.send(_env("09", "human", "fraud.referral", ctx, pkg,
                           escalation_flag=True))
        self.hub.send(_env("09", "13", "fraud.referral", ctx, pkg))


# ------------------------------------------------------------------ 10
class Spoke10Subrogation:
    """Recovery preparation. Demands and acceptances are human money."""

    def __init__(self, hub):
        self.hub = hub
        self.cases = {}

    def handle(self, env):
        ctx = env.client_context_id
        st = self.cases.setdefault(ctx, {"signals": [], "salvage": [],
                                         "executed": None})
        if env.intent == "subro.signal":
            st["signals"].append(env.payload)
            pkg = {"signals": list(st["signals"]),
                   "salvage": list(st["salvage"]),
                   "netting": "arithmetic_shown"}
            self.hub.send(_env("10", "human", "subro.package", ctx, pkg,
                               escalation_flag=True))
            self.hub.send(_env("10", "13", "subro.package", ctx, pkg))
        elif env.intent == "salvage.record":
            st["salvage"].append(env.payload)
        elif env.intent == "recovery.authority":
            st["executed"] = env.payload      # signed; hub enforced it
            self.hub.send(_env("10", "13", "interaction.log", ctx,
                               {"event": "recovery_executed_signed",
                                "amount": env.payload.get("amount")}))


# ------------------------------------------------------------------ 11
class Spoke11PaymentsReserves:
    """Money. Payments and reserve changes move only on signed authority;
    books reconcile to $0.00; salvage proceeds post to the record."""

    def __init__(self, hub):
        self.hub = hub
        self.ledger = {}

    def _st(self, ctx):
        return self.ledger.setdefault(ctx, {"paid": 0.0, "reserve": None,
                                            "estimate": None})

    def handle(self, env):
        ctx = env.client_context_id
        st = self._st(ctx)
        if env.intent == "payment.authority":
            st["paid"] += env.payload["amount"]
            for to in ("12", "13"):
                self.hub.send(_env("11", to, "payment.record", ctx,
                                   {"amount": env.payload["amount"],
                                    "signed": True}))
            expected = env.payload.get("expected_total")
            if expected is not None and abs(expected - st["paid"]) > 0.0:
                for to in ("human", "13"):
                    self.hub.send(_env("11", to, "reconciliation.exception",
                                       ctx, {"expected": expected,
                                             "paid": st["paid"],
                                             "variance": round(
                                                 st["paid"] - expected, 2)},
                                       escalation_flag=(to == "human")))
        elif env.intent == "reserve.authority":
            st["reserve"] = env.payload["amount"]
            for to in ("12", "13"):
                self.hub.send(_env("11", to, "reserve.record", ctx,
                                   {"amount": env.payload["amount"],
                                    "signed": True}))
        elif env.intent == "estimate.package":
            st["estimate"] = env.payload

    def post_salvage_proceeds(self, ctx, amount):
        for to in ("10", "13"):
            self.hub.send(_env("11", to, "salvage.record", ctx,
                               {"proceeds": amount, "posted": True}))


# ------------------------------------------------------------------ 12
class Spoke12ComplianceDeadlines:
    """Fair-claims clocks. Lead-time alert, then escalation. DOI inquiries
    become human packages on a clock; conservatism rule: earlier wins."""

    DOI_LEAD, DOI_ESC = 10, 3            # ratified 2026-07-18
    RECORDS_LEAD, RECORDS_ESC = 10, 3    # ratified 2026-07-18

    def __init__(self, hub):
        self.hub = hub
        self.clocks = {}

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent == "doi.inquiry":
            self.arm(ctx, "doi_response",
                     deadline_day=env.payload.get("deadline_day", 15),
                     lead=self.DOI_LEAD, esc=self.DOI_ESC)
            pkg = {"inquiry_verbatim": env.payload,
                   "response_draft": None}   # humans respond to regulators
            self.hub.send(_env("12", "human", "doi.response.package", ctx,
                               pkg, escalation_flag=True))
            self.hub.send(_env("12", "13", "doi.response.package", ctx, pkg))
        elif env.intent == "records.disclosure.package":
            self.arm(ctx, "records_response",
                     deadline_day=env.payload.get("deadline_day", 30),
                     lead=self.RECORDS_LEAD, esc=self.RECORDS_ESC)
        elif env.intent == "representation.notice":
            self.arm(ctx, "represented_posture_review", deadline_day=5,
                     lead=3, esc=1)
        elif env.intent in ("claim.assignment", "payment.record",
                            "reserve.record", "policy.change.notice"):
            pass

    def arm(self, ctx, kind, deadline_day, lead, esc):
        self.clocks.setdefault(ctx, []).append(
            {"kind": kind, "deadline_day": deadline_day, "lead": lead,
             "esc": esc, "alerted": False, "escalated": False})

    def run_daily(self, today):
        for ctx, clocks in self.clocks.items():
            for c in clocks:
                remaining = c["deadline_day"] - today
                if remaining <= c["esc"] and not c["escalated"]:
                    c["escalated"] = True
                    self.hub.send(_env("12", "queue", "escalation.clock",
                                       ctx, {"kind": c["kind"],
                                             "days_remaining": remaining},
                                       escalation_flag=True))
                elif remaining <= c["lead"] and not c["alerted"]:
                    c["alerted"] = True
                    for to in ("02", "04", "14"):
                        self.hub.send(_env("12", to, "deadline.alert", ctx,
                                           {"kind": c["kind"],
                                            "days_remaining": remaining}))


# ------------------------------------------------------------------ 13
class Spoke13ClaimFileRecords:
    """The claim file. Append-only; disclosure inventory is existence/
    type/date/source only; privilege flags travel, judgments don't."""

    def __init__(self, hub):
        self.hub = hub
        self.log = {}
        self.copies = {}

    def handle(self, env):
        ctx = env.client_context_id
        if env.intent == "record.request":
            self.hub.send(_env("13", env.from_agent, "record.response", ctx,
                               {"entries": list(self.log.get(ctx, [])),
                                "complete_as_of": "runtime"}))
        elif env.intent == "interaction.log":
            self.log.setdefault(ctx, []).append(
                {"from": env.from_agent, "event": env.payload})
        else:
            self.copies.setdefault(ctx, []).append(
                {"intent": env.intent, "from": env.from_agent,
                 "payload": env.payload})

    def external_records_request(self, ctx, request):
        inv = [{"type": e["intent"], "date": "runtime", "source": e["from"],
                "privilege_flag": bool(
                    isinstance(e.get("payload"), dict)
                    and e["payload"].get("privilege_flag"))}
               for e in self.copies.get(ctx, [])]
        pkg = {"request_verbatim": request, "inventory": inv,
               "content_sealed": True,
               "deadline_day": request.get("deadline_day", 30)}
        self.hub.send(_env("13", "human", "records.disclosure.package", ctx,
                           pkg, escalation_flag=True))
        self.hub.send(_env("13", "12", "records.disclosure.package", ctx,
                           {"deadline_day": pkg["deadline_day"]}))


# ------------------------------------------------------------------ 14
class Spoke14DailyOperations:
    def __init__(self, hub):
        self.hub = hub
        self.waits, self.alerts = [], []

    def handle(self, env):
        if env.intent == "agent.status":
            self.waits.append(env.payload)
        elif env.intent == "deadline.alert":
            self.alerts.append(env.payload)

    def morning_report(self, ctx="ops"):
        pkg = {"waits": list(self.waits), "clock_alerts": list(self.alerts)}
        self.hub.send(_env("14", "human", "report.package", ctx, pkg))
        return pkg

    def cat_event(self, ctx, details):
        self.hub.send(_env("14", "02", "cat.event", ctx, dict(details)))
