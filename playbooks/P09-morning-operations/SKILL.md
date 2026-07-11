---
name: P09-morning-operations
description: "Swarm deployment: the claims desk's morning book. Overnight FNOLs, today's clocks, the inspection calendar, aging exceptions - assembled from records and presented for human review before the day starts. Agents 14, 13, 12."
---

# Playbook P09 - Morning Operations

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Scheduled daily start (owner-configured time) or owner command.

## Preconditions
- EOD books from the previous day exist (P10 completion on the log); if absent, the book runs with the gap NAMED, never silently thinner.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Assemble (parallel, all to human review)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 14 | Pull overnight intake and lifecycle exceptions from the record | `record.request` → 13 | overnight section sourced |
| 2 | 14 | Pull today's clock alerts and lead-time exposures | (from 12's `deadline.alert` stream) | clock section current with lead-times |
| 3 | 14 | Assemble the inspection calendar and aging-claim exceptions | (from record pulls) | calendar + exceptions sections sourced |

### Present
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 14 | Deliver the morning book; sections with unavailable sources marked absent | `report.package` → human | book delivered; the human directs, the book never self-executes |

## HITL gates (hard stops)
- A source unavailable at assembly time is a named absence - never yesterday's numbers backfilled (14's tuple).

## Completion criteria
Morning book delivered to the human with every section sourced or marked absent.

## Abort paths
- Record source down: section marked absent; book still delivers on time.
