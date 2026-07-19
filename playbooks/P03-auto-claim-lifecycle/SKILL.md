---
name: P03-auto-claim-lifecycle
description: "Swarm deployment: assigned auto claim through appraisal, valuation, rental coordination, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 13. Total-loss threshold checks fire as facts to the adjuster."
---

# Playbook P03 - Auto Claim Lifecycle

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.2 (ratified 2026-07-18; extended & ratified 2026-07-18 - owner sign-off)

## Trigger
`claim.assignment` with line of business = auto.

## Preconditions
- P01 completed; listed-vehicle/driver facts from 03 attached to the assignment.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Evidence (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 05 | Collect photos, police report, repair estimates per auto checklist | `doc.received` → 02, 08, 13 | inventory current; police-report fault facts also fire `subro.signal` |
| 2 | 06 | Schedule appraisal (field or desk per severity band) | `inspection.result` → 08, 13 | appraisal findings verbatim |
| 3 | 07 | Rental coordination within policy terms from 03's verified limits | `vendor.status` → 02, 13 | rental record with term basis attached |

### Phase 2 - Valuation
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 08 | Estimate package; run total-loss threshold per jurisdiction; within-margin reported as within-margin | `estimate.package` → 02, 11, 13 | package with threshold comparison as fact |

### Phase 3 - Human decision support
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 5 | 02 | Closure package with all gates stated | `closure.package` → human, 13 | human decision logged |
| 6 | 11 | Authority-gated payment/reserve records | `payment.record` → 12, 13 | authority envelope_id attached |

## HITL gates (hard stops)
- Unlisted-driver or unlisted-vehicle facts route to the human as facts (03's rule) - the lifecycle continues unless the human holds it.
- Total-loss crossing triggers P04 on human direction, never automatically.

## Completion criteria
Closure package delivered with threshold facts stated; records reconciled.

## Abort paths
- Human coverage hold: as P02.
- Total-loss crossing: this playbook holds valuation-forward steps pending human P04 direction.
