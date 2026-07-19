---
name: P05-fraud-referral
description: "Swarm deployment: threshold-crossing signal record to SIU referral package. Agents 09, 13, plus contributing observers. The claim's normal lifecycle NEVER changes - delay-on-suspicion is the named illegal move."
---

# Playbook P05 - Fraud Referral

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.2 (ratified 2026-07-18; extended & ratified 2026-07-18 - owner sign-off)

## Trigger
09's aggregated signal score crosses the owner-ratified threshold on a claim.

## Preconditions
- Every contributing signal carries source and verbatim basis (09's intake rule).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Package (silent to the lifecycle)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 09 | Assemble referral package: signals, sources, timeline from 13's chronology | `record.request` → 13 | chronology attached |
| 2 | 09 | Route the package to the human SIU decision-maker | `fraud.referral` → human, 13 | referral logged; decision is human |

### Phase 2 - Human decision (swarm posture unchanged)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 13 | Register the SIU decision as a record entry when the human supplies it | (record entry) | decision on file; handling changes only on explicit human direction |

## HITL gates (hard stops)
- No agent's behavior on the claim changes at referral - schedules, payments-on-authority, and communications continue exactly per playbook.
- The referral's existence is need-to-know sealed (09's tuple); no cross-agent disclosure.

## Completion criteria
Referral package delivered to the human SIU decision-maker; lifecycle posture verified unchanged.

## Abort paths
- Any request to alter claim handling on suspicion: integrity.violation; the playbook itself never touches the lifecycle.
