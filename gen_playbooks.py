#!/usr/bin/env python3
"""Generate playbooks P01-P10 for the DispatcherAgents Claim swarm."""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "playbooks")

def build(p):
    s = f'---\nname: {p["num"]}-{p["slug"]}\ndescription: "{p["desc"]}"\n---\n\n'
    s += f'# Playbook {p["num"]} - {p["name"]}\n\n'
    s += "**Swarm:** DispatcherAgents Claim Swarm (Insurance)\n**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)\n**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)\n\n"
    s += "## Trigger\n" + p["trigger"] + "\n\n## Preconditions\n"
    for x in p["pre"]: s += f"- {x}\n"
    s += "Precondition unmet = playbook does not start; `clarification.request` to human.\n\n## Deployment sequence\n"
    for title, rows in p["phases"]:
        s += f"\n### {title}\n| Step | Agent | Action | Intent | Proof of done |\n|---|---|---|---|---|\n"
        for r in rows: s += "| " + " | ".join(r) + " |\n"
    s += "\n## HITL gates (hard stops)\n"
    for g in p["gates"]: s += f"- {g}\n"
    s += "\n## Completion criteria\n" + p["completion"] + "\n\n## Abort paths\n"
    for a in p["abort"]: s += f"- {a}\n"
    if p.get("notes"): s += "\n## Notes for the Dispatcher\n" + p["notes"] + "\n"
    return s

from claim_playbooks import PB  # single source (fork-drift fix 2026-07-18)
CA = {
 "P01": ("Claim verified, scored, assigned per matrix, clocks live, checklist issued, acknowledgment sent - all inside the acknowledgment SLA.",
   ["Policy 'not found' or lapsed: hold in intake-verified state; human direction resumes.",
    "Assignment matrix gap: human queue; playbook holds at Phase 2."]),
 "P02": ("Closure package delivered to the human with every gate stated; post-decision records complete.",
   ["Human coverage hold at any point: swarm freezes client-visible steps, records continue.",
    "Safety hold on inspection access: Phase 1 step 2 holds; hazard routed."]),
 "P03": ("Closure package delivered with threshold facts stated; records reconciled.",
   ["Human coverage hold: as P02.",
    "Total-loss crossing: this playbook holds valuation-forward steps pending human P04 direction."]),
 "P04": ("Settlement payment recorded against signed authority; title/lien docs on file; closure package delivered.",
   ["Claimant counter-offer: route verbatim to human; all settlement communication holds.",
    "Lienholder document conflict: hold payment execution; human resolves."]),
 "P05": ("Referral package delivered to the human SIU decision-maker; lifecycle posture verified unchanged.",
   ["Any request to alter claim handling on suspicion: integrity.violation; the playbook itself never touches the lifecycle."]),
 "P06": ("Evidence preserved with custody flags; demand package delivered for human pursuit decision.",
   ["Preservation vs. habitability conflict: immediate human escalation; neither clock silently sacrificed.",
    "Third-party carrier contact received: route verbatim; assembly continues unless human holds."]),
 "P07": ("Financial records executed against authority and reconciled; closure package delivered.",
   ["Authority anomaly (stale estimate version, changed payee): hold + re-confirm; execution waits.",
    "Amber closure gate: package delivers with the amber named; closure is the human's call."]),
 "P08": ("Signature-ready response package delivered inside the ratified lead-time.",
   ["Certain shortfall: deliver early with the gap named - a partial package on time beats a full one late.",
    "Regulator deadline ambiguity: conservatism rule; the earlier date governs."]),
 "P09": ("Morning book delivered to the human with every section sourced or marked absent.",
   ["Record source down: section marked absent; book still delivers on time."]),
 "P10": ("EOD books delivered; sweep complete with owners named; completion event logged for tomorrow's P09.",
   ["Morning baseline absent: sweep names that first and proceeds on records alone."]),
}
for p in PB:
    p["completion"], p["abort"] = CA[p["num"]]

def main():
    os.makedirs(ROOT, exist_ok=True)
    for p in PB:
        d = os.path.join(ROOT, f"{p['num']}-{p['slug']}")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w").write(build(p))
        print("emitted", p["num"])

if __name__ == "__main__":
    main()
