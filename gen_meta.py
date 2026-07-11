#!/usr/bin/env python3
"""Generate the meta pre-decision layer: per-agent DECISIONS.md (tuple layer)
and SWARM.md (framework manifest + swarm-level tuples).
Tuples are (crossing, answer): the deliberation happened before the run."""
import os
from generate_skills import ROUTES, AGENTS

PKG = os.path.dirname(os.path.abspath(__file__))

SWARM_TUPLES = [
 ("two playbooks match one trigger", "run neither; clarification.request naming both"),
 ("a playbook step conflicts with an agent's legal line", "halt playbook; integrity.violation - spec defect, never a judgment call"),
 ("workload exceeds capacity", "priority order: escalations > active-transaction deadlines > client-facing requests > internal/marketing > discovery; ties go to the older item"),
 ("signed human instruction conflicts with a playbook", "signed human wins; deviation logged in the after-action report"),
 ("required data is stale beyond threshold", "regenerate; never present stale as current"),
 ("one parallel step fails mid-phase", "complete independent siblings; hold dependents; flag - never abandon the phase silently"),
 ("identical envelope arrives twice", "process once; envelope_id is the idempotency key"),
 ("uncertainty about whether a legal line is crossed", "treat as crossed; escalate"),
 ("no suitable tuple exists for the task at hand", "STOP; clarification.request to the human and wait - a missing tuple is a design omission to fix, never a license to improvise"),
 ("context fade suspected or long run", "re-read MANNERS.md and own SKILL.md before the next action"),
 ("visibility limited but the path seems clear", "proceed only within stopping distance: reversible increments; irreversible or client-visible actions wait for full verified authority"),
 ("two runs contend for the same agent", "higher priority class proceeds; the lower takes the siding - held live on route, resumes when the segment clears; contention never aborts a run"),
 ("task requires a path outside declared edges", "refuse; clarification.request - an undeclared path is ambiguity, not opportunity"),
 ("an unlisted crossing is reached", "ambiguity protocol; propose the missing tuple in the after-action report for human ratification"),
]

D = {
"00": [
 ("route valid but ambiguous", "hold in clarification queue; never route on 'most likely'"),
 ("signature invalid on authority intent", "reject + integrity.violation; notify human out-of-band"),
 ("duplicate envelope_id arrives", "re-ack the original outcome; never process twice"),
 ("compliance.hold received mid-run", "suspend the named claim's traffic; only 12's release or human direction resumes it"),
 ("two agents claim the same open request", "the earlier record.request wins; the later is re-pointed with the earlier's envelope_id"),
 ("a spoke reports done without its artifact", "treat as not-done; taint gate applies - the artifact is the proof"),
],
"01": [
 ("reporter is a third party, not the insured", "capture with relationship named; verification of standing is 03/human territory"),
 ("injuries mentioned then walked back", "the injury flag stays set with both statements verbatim; flags ratchet up at intake, never down"),
 ("loss date is 'a while ago'", "capture verbatim, mark date unknown; late-report handling is 02/12's clock decision"),
 ("reporter reports two distinct losses in one call", "two FNOL packages, cross-referenced; never merged"),
 ("emergency in progress (active water, fire aftermath)", "capture mitigation-need flag first, full FNOL second; route the flag ahead of package completion"),
],
"02": [
 ("severity rubric inputs missing at scoring time", "score with the missing input at its worst-case band and name the gap; never wait to score an injury flag"),
 ("assignment matrix has no row for this combination", "human queue; a matrix gap is a design omission, never a nearest-row pick"),
 ("policy verified lapsed on date of loss", "package the fact to human immediately; downstream work holds - lapse handling is a licensed decision"),
 ("claimant demands a specific adjuster", "record the request in the assignment envelope; the matrix and human decide"),
 ("closure package has one amber gate", "the package does not go to the human as closure-ready; amber is named, not rounded green"),
],
"03": [
 ("named insured mismatch (marriage, trust, LLC transfer)", "report the mismatch with both names verbatim; standing determination is human"),
 ("endorsement effective date is the loss date itself", "report the timestamp collision as a fact with system times; never resolve which came first by assumption"),
 ("prior verification cached from earlier in this claim", "re-verify against the live system; policy facts are re-checked, never remembered"),
 ("verification requested for a policy in another company's book", "refuse; out-of-book lookup is an integrity flag, not a favor"),
],
"04": [
 ("claimant is distressed and asks 'will I be okay?'", "empathy template plus process facts; never reassurance that implies coverage"),
 ("message request arrives for a claim flagged represented", "refuse the send; return the request to sender with the representation flag"),
 ("claimant communicates in a language without an approved template", "human queue; machine-translating a legal disclosure is a compliance breach"),
 ("two message requests to the same claimant in one hour", "bundle per the cadence rule; double-texting a claimant is a real-world failure"),
 ("claimant reply contains a threat of self-harm", "immediate human escalation, highest priority, verbatim; no template applies"),
],
"05": [
 ("proof of loss arrives unsigned", "inventory as received-defective; the chase names the signature gap - never file it as satisfying the checklist"),
 ("claimant asks which receipts 'would help most'", "provide the checklist as-is; curating evidence coaching is over the line"),
 ("document arrives for the wrong claim number", "route to 13 for re-association with provenance; never re-label locally"),
 ("police report shows a third party at fault", "inventory it AND fire subro.signal; evidence duties stack, they don't compete"),
 ("medical bill arrives unrequested", "seal to human lane unopened per custody rule; inventory existence only"),
],
"06": [
 ("insured offers only a time outside adjuster hours", "escalate the conflict with both constraints; never book either side into a broken slot"),
 ("re-inspection requested on a claim with a fraud referral pending", "schedule normally; handling never changes on suspicion - that is 09's iron rule too"),
 ("access requires a tenant who is unresponsive", "route the access gap to human with attempts logged; never advise entry"),
 ("weather makes the inspection window unsafe", "reschedule with the hazard named; safety outranks the SLA clock"),
],
"07": [
 ("vendor ETA slips past the mitigation-critical window", "escalate with the slip quantified; secondary damage from a missed mitigation window is a named loss driver"),
 ("vendor submits photos that duplicate another claim's set", "vendor.status flags it AND fraud.signal fires; both routes, verbatim basis"),
 ("insured refuses the assigned vendor", "record the refusal; jurisdiction choice rules route to human - never argue the panel"),
 ("vendor requests direct claimant contact", "deny; all claimant contact flows through 04's templates"),
],
"08": [
 ("two approved pricing sources disagree on one line item", "variance report per line, not per estimate; granular variance is the adjuster's raw material"),
 ("total-loss threshold lands within the rounding margin", "report as within-margin, not as a determination either way"),
 ("prior-claim damage overlaps this claim's scope", "flag the overlap with both claim records; never net it out silently"),
 ("estimate requested before inspection results exist", "desk-estimate label mandatory with inputs named; an unlabeled desk number reads as an inspected one"),
],
"09": [
 ("a single strong indicator versus many weak ones", "the ratified scoring decides; no indicator gets judgment weight"),
 ("SIU asks for 'everything suspicious this month'", "answer via 13 record scope rules; fishing expeditions get scoped queries, not dumps"),
 ("an agent asks whether a claim 'is being looked at'", "refuse; signal-record existence is need-to-know sealed"),
 ("indicator arrives on a closed claim", "aggregate normally and route at threshold; closure does not expire the referral duty"),
],
"10": [
 ("preservation request conflicts with claimant's repair urgency", "escalate immediately with both clocks; habitability versus spoliation is a human call"),
 ("statute date differs by theory of recovery", "track the shortest; conservatism is the ratified clock rule here too"),
 ("carrier for the third party contacts the swarm directly", "route verbatim to human; no acknowledgment beyond receipt"),
 ("deductible recovery for the insured rides on pursuit", "note it in the package economics; the insured's interest is named, never promised"),
],
"11": [
 ("authority envelope arrives twice (retry)", "execute once; envelope_id idempotency is the financial-safety rule"),
 ("partial payment authorized against a superseded estimate line", "hold; re-confirm - money against stale math is the named failure"),
 ("reserve decrease authorized while a new estimate is in flight", "execute the signed authority AND flag the timing to human; execution and flagging are not alternatives"),
 ("payee asks for payment split across accounts", "hold and route to human; payment-instruction changes are never agent-absorbed"),
],
"12": [
 ("clock event depends on a disputed receipt date", "earlier date runs the clock; conservatism is ratified"),
 ("regulator requests an extension response same-day", "package immediately with the gap named; a partial package on time beats a full one late - the human signs either way"),
 ("fair-claims rule conflicts with a playbook step", "compliance.hold; spec defect doctrine - the playbook halts, the rule does not bend"),
 ("new jurisdiction rule announced but not yet ratified into the table", "alert the human with the delta; the table changes only by ratification"),
],
"13": [
 ("record correction requested by the agent that wrote it", "append the correction referencing the original; authorship grants no edit rights"),
 ("record request for a sealed medical entry", "refuse with the seal named; unsealing is human-only regardless of requester"),
 ("chronology requested spanning a litigation hold", "produce it AND name the hold; production rules are counsel's call"),
 ("storage failure detected on write", "the write is not done until re-verified on storage; an unconfirmed write is reported failed, never assumed"),
],
"14": [
 ("book source data is mid-update at assembly time", "snapshot with the timestamp named; a book is a photograph, not a live feed"),
 ("EOD sweep finds a morning item nobody touched", "the miss is named with its owner; the sweep never reassigns silently"),
 ("cat.event scope is ambiguous (county vs. zip list)", "rebroadcast with the ambiguity named and the narrower scope active; scope expands only on human direction"),
 ("human requests a 'cleaner' book", "decline; the book's gaps are its value - integrity.violation if pressed"),
],
}

def decisions_md(num, name):
    rows = "\n".join(f"- ({c}, {a})" for c, a in D[num])
    rows += "\n\n(Root rule, restated: no suitable tuple - or an uncertain match - means STOP and ask the human.)"
    return f"""# Agent {num} - Predeliberated Decisions (Tuple Layer) v0.1 (ratified 2026-07-11 - owner sign-off)

PRE-TEXT - ROOT OF THE TUPLE DECISION TREE (owner rule, binding):
before ANY task or decision, consult this layer. If NO suitable tuple covers
the task: STOP. Contact the human via clarification.request and wait. Do not
improvise, do not pick the nearest tuple, do not proceed on judgment - a
missing tuple is a design omission to be fixed, never a license to act. A
PARTIAL OR UNCERTAIN MATCH IS NOT-FOUND: if it takes judgment to decide the
tuple fits, it does not fit - STOP applies. The after-action proposes the
missing tuple so the omission is closed.

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) - a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything.

{rows}
"""

def swarm_md():
    agents_list = "\n".join(f"- {a['num']} {a['name']}" for a in AGENTS)
    intents = sorted({i for i, *_ in ROUTES})
    tuples = "\n".join(f"- ({c}, {a})" for c, a in SWARM_TUPLES)
    return f"""# SWARM.md - Framework Manifest + Swarm-Level Decisions (v0.1, ratified 2026-07-11 - owner sign-off)

Framework context for the dispatcher and every agent: as much predefined
structure as exists, until learning (after-action dataset) takes over.
MANIFEST SECTION IS MACHINE-GENERATED from ROUTES/AGENTS in generate_skills.py
 -  regenerate via gen_meta.py; hand-edits here will be overwritten and are a
defect, not a change.

## Manifest (generated)
- Agents: {len(AGENTS)+1} (00-dispatcher + {len(AGENTS)} spokes)
- Routes: {len(ROUTES)} entries, {len(intents)} distinct intents
- Playbooks: P01-P10 (playbooks/)
- Layer stack: MANNERS.md → DISPATCHER_CORE.md → identity/ → DECISIONS.md
  (per agent) → playbooks/ → agent SKILL.md files
- Track principle: the ROUTE-SPACE IS CLOSED. Agents run on predetermined
  track; an option absent from the routing table, playbooks, and tuples does
  not exist. Trains request routes; only the hub lines switches. Content-space
  is BOUNDED (manners, compliance verdicts) but not closed - generative freight
  is why inspection exists (12's compliance holds, verify_swarm, after-action).
- Routes never originate on the train: a run = a FIXED route + VARIABLE events
  (scheduled work at the stations along the line, or unforeseen events that
  trigger the restricted-speed doctrine). Agents never create routes or work
  assignments; on arrival they produce documents and evaluations from
  predetermined possibilities, autonomously, under dispatcher permission.
- Crew principle: the track cannot disobey and the train cannot disobey - the
  CREW can, and derailments are crew decisions on compliant hardware. In this
  swarm the model is the crew, not the train. Rulebooks alone never stopped
  crew-caused derailments; automated enforcement did. Every rule therefore
  ships with its enforcement twin: instruction < detection (verify_swarm,
  after-action, audit log) < structural impossibility (acks, signatures,
  closed routes). Constraint reduces variance, not bias - a wrong tuple makes
  the swarm consistently wrong, which is why spec ratification outranks spec
  volume.
- Shared-segment principle: spokes are shared track segments - concurrent runs
  (trains) traverse the same agents. The dispatcher's value concentrates where
  track is shared: sequencing, priority class, and context isolation are block
  protection for segments used by other trains.
- Spokes:
{agents_list}
- Intents: {", ".join(f"`{i}`" for i in intents)}

## Swarm-level decision tuples (predictable scenarios, pre-deliberated)
{tuples}

Status: v0.1 ratified 2026-07-11 (owner sign-off) - manifest verified against generator data at generation
time; not runtime-tested.
"""

def main():
    # dispatcher decisions live in its folder like every spoke's
    names = {a["num"]: a["name"] for a in AGENTS}
    names["00"] = "Dispatcher"
    slugs = {a["num"]: f'{a["num"]}-{a["slug"]}' for a in AGENTS}
    slugs["00"] = "00-dispatcher"
    for num in sorted(D):
        path = os.path.join(PKG, slugs[num], "DECISIONS.md")
        open(path, "w").write(decisions_md(num, names[num]))
    open(os.path.join(PKG, "SWARM.md"), "w").write(swarm_md())
    print(f"wrote {len(D)} DECISIONS.md + SWARM.md")

if __name__ == "__main__":
    main()
