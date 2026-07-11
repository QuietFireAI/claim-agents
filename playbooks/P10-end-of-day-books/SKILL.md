---
name: P10-end-of-day-books
description: "Swarm deployment: the closing books. Every claim touched, every clock advanced or missed, the missed-item sweep against the morning book. Agents 14, 13, 12. Gaps named; a clean-looking book with hidden gaps is the named failure."
---

# Playbook P10 - End-of-Day Books

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Scheduled day end (owner-configured time) or owner command.

## Preconditions
- The morning book (P09) exists as the sweep baseline; if absent, the sweep names that first.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Assemble
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 14 | Pull the day's full activity chronology | `record.request` → 13 | activity section sourced with timestamps |
| 2 | 14 | Reconcile clocks: advanced, satisfied, at-risk, missed - misses quantified | (from 12's alert stream + records) | clock reconciliation complete |
| 3 | 14 | Missed-item sweep: every morning-book item without a day touch, named with its owner | (sweep vs. P09 baseline) | sweep list complete; no silent reassignment |

### Present
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 14 | Deliver the EOD books | `report.package` → human | books delivered and logged; P10 completion event on the log for tomorrow's P09 |

## HITL gates (hard stops)
- The sweep never reassigns - it names (14's tuple). Reassignment is the human's morning decision.

## Completion criteria
EOD books delivered; sweep complete with owners named; completion event logged for tomorrow's P09.

## Abort paths
- Morning baseline absent: sweep names that first and proceeds on records alone.
