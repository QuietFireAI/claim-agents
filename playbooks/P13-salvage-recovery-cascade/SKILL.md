---
name: P13-salvage-recovery-cascade
description: "Swarm deployment: salvage value and subrogation facts to signed, executed recovery. Agents 08, 11, 10, 13. Recovery is money: demands, acceptances, and reserve effects move only on signed authority."
---

# Playbook P13 - Salvage & Recovery Cascade

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)

## Trigger
`salvage.record` at 10 (from valuation 08 or posted proceeds 11), or an accepted `subro.package` returning as a recovery to execute.

## Preconditions
- Salvage values and liability facts are on record from valuation and the claim file - recovery arithmetic runs on posted facts only.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Assemble
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 10 | Recovery package: subro facts, salvage values, netting arithmetic shown | `subro.package` → human, 13 | every number carries its source |
| 2 | 13 | Claim-file support attached (existence/type/date/source) | `record.response` → 10 | file citations complete |

### Phase 2 - Signed execution
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 10 | Demand issues / acceptance executes on signed authority only | (await `recovery.authority` ← human) | signed envelope on the chain first |
| 4 | 11 | Proceeds post; books reconcile to $0.00 variance | `payment.record` + `salvage.record` → 12, 13 | reconciliation clean or exception raised |

## HITL gates (hard stops)
- No demand, settlement acceptance, or waiver moves without signed `recovery.authority` - recovery is money, same doctrine as payments.
- Netting is arithmetic shown, never judgment applied - allocation questions route to the human.

## Completion criteria
Recovery executed on signed authority, proceeds posted, books at $0.00 variance; or the blocking question named to the human.

## Abort paths
- Counterparty disputes liability or amount: package the dispute verbatim for the human - the swarm never negotiates.
- Proceeds do not reconcile to the posted expectation: reconciliation.exception; the variance is named, never absorbed.
