---
name: P06-subrogation-handoff
description: "Swarm deployment: recovery signal to preserved evidence and demand package for human pursuit. Agents 10, 05, 08, 13. Preservation fires immediately; the pursuit decision waits for no artifact."
---

# Playbook P06 - Subrogation Handoff

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.2 (ratified 2026-07-18; extended & ratified 2026-07-18 - owner sign-off)

## Trigger
`subro.signal` matching the recovery-opportunity checklist at 10.

## Preconditions
- Signal carries the liability-basis evidence pointer (police report, inspection finding, vendor observation).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Preserve (immediate)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 10 | Issue evidence-preservation requests the moment the opportunity is identified | `doc.request` → 05 | preservation requests logged with spoliation-window basis |
| 2 | 05 | Execute preservation: custody flags on physical-evidence pointers, retention holds via 13 | `doc.received` → 02, 08, 13 | custody status inventoried |

### Phase 2 - Package
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 10 | Assemble demand package: liability basis, damages support from 08, evidence inventory, statute dates (shortest theory governs) | `subro.package` → human, 13 | package delivered; pursuit decision is human |

## HITL gates (hard stops)
- Habitability/repair urgency versus preservation conflicts escalate immediately (10's tuple) - neither clock is silently sacrificed.
- No contact with the third party or their carrier originates from the swarm.

## Completion criteria
Evidence preserved with custody flags; demand package delivered for human pursuit decision.

## Abort paths
- Preservation vs. habitability conflict: immediate human escalation; neither clock silently sacrificed.
- Third-party carrier contact received: route verbatim; assembly continues unless human holds.
