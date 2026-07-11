---
name: P01-fnol-to-assignment
description: "Swarm deployment: reported loss to verified, assigned, clock-instantiated claim. Agents 01, 02, 03, 12, 13. The speed-to-FNOL front door - acknowledgment and assignment SLAs run from first contact."
---

# Playbook P01 - FNOL to Assignment

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)

## Trigger
`claim.fnol` package lands at 02, any channel, any hour.

## Preconditions
- FNOL package carries provenance per field; unknowns marked unknown (01's capture rule).
- Assignment matrix and severity rubric are the owner-ratified versions on file.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Verify and score (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 02 | Score severity per ratified rubric; worst-case band on missing inputs, gap named | `policy.verify.request` → 03 | score + gap list on the claim record |
| 2 | 03 | Verify policy status/limits/endorsements on date of loss from live systems | `policy.verify.result` → 02, 13 | result with system timestamps |
| 3 | 12 | Instantiate jurisdiction clock set from assignment context | (internal; alerts arm) | clock set on record with lead-times |

### Phase 2 - Assign (gated on Phase 1)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 02 | Assign per matrix; out-of-matrix combinations go to human queue | `claim.assignment` → 06, 12, 13 | assignment envelope acked; lapse/mismatch facts routed to human if present |
| 5 | 02 | Open document checklist for the line of business | `doc.request` → 05 | checklist issued and logged |
| 6 | 02 | Acknowledgment to claimant per statutory template | `claimant.message.request` → 04 | send logged with disclosure set |

## HITL gates (hard stops)
- Phase 2 does not start on an unverified policy - 'not found' holds in intake-verified state (02 tuple).
- Injury/fatality flags route the human notification inside the acknowledgment SLA, not after it.

## Completion criteria
Claim verified, scored, assigned per matrix, clocks live, checklist issued, acknowledgment sent - all inside the acknowledgment SLA.

## Abort paths
- Policy 'not found' or lapsed: hold in intake-verified state; human direction resumes.
- Assignment matrix gap: human queue; playbook holds at Phase 2.
