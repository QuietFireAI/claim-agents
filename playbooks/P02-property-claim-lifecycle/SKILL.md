---
name: P02-property-claim-lifecycle
description: "Swarm deployment: assigned property claim through docs, inspection, estimate, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 12, 13. The human decides coverage and closure; the swarm keeps every gate visible."
---

# Playbook P02 - Property Claim Lifecycle

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
`claim.assignment` with line of business = property.

## Preconditions
- P01 completed: verified policy, clocks live, checklist issued.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Evidence (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 05 | Collect checklist docs; chase on cadence; anomalies to 09 as observations | `doc.received` → 02, 08, 13 | item-level inventory current |
| 2 | 06 | Schedule inspection inside the severity SLA window; confirm access | `inspection.schedule` fulfilled; result → 08, 13 | inspection result with verbatim findings |
| 3 | 07 | Coordinate mitigation vendors as requested; verify deliverables landed | `vendor.status` → 02, 08, 13 | artifact-verified milestones |

### Phase 2 - Valuation (gated on inspection + docs)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 08 | Assemble estimate package, sources attached; variance report if estimates diverge | `estimate.package` → 02, 11, 13 | package with methods, sources, variances |

### Phase 3 - Human decision support
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 5 | 02 | Assemble closure package when all gates green; amber gates named | `closure.package` → human, 13 | package delivered; human decision logged by 13 |
| 6 | 11 | Execute payments/reserves ONLY on signed authority; records to 12/13 | `payment.record`, `reserve.record` | records carry authority envelope_id |
| 7 | 04 | Status updates on the playbook cadence throughout | `claimant.message.send` | every send logged verbatim |

## HITL gates (hard stops)
- No figure leaves the swarm: 08's numbers are adjuster work product only.
- Payment execution without signed `payment.authority` is an integrity violation, not an error.

## Completion criteria
Closure package delivered to the human with every gate stated; post-decision records complete.

## Abort paths
- Human coverage hold at any point: swarm freezes client-visible steps, records continue.
- Safety hold on inspection access: Phase 1 step 2 holds; hazard routed.
