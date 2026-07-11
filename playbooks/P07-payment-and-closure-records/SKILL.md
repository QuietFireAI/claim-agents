---
name: P07-payment-and-closure-records
description: "Swarm deployment: signed authority to executed, reconciled, compliance-visible financial records and the closure package. Agents 11, 12, 02, 13. Records only - authority moves money, the swarm moves paper."
---

# Playbook P07 - Payment & Closure Records

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Signed `payment.authority` envelope arrives at 11, or 02 determines all closure gates green.

## Preconditions
- Authority references a current estimate version; payee details match the record (11's hold tuples otherwise).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Execute on authority
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 11 | Verify authority signature context, estimate version, payee details; execute; anomalies hold + re-confirm | `payment.record` → 12, 13 | record with authority envelope_id |
| 2 | 12 | Register the financial event against the claim's clocks | (clock update) | clock state current |

### Phase 2 - Closure package
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 02 | Assemble closure package: docs complete, estimate final, payments reconciled, clocks satisfied - ambers named | `closure.package` → human, 13 | package delivered; the human closes |
| 4 | 04 | Send closure communications on the approved template after the human's closure decision | `claimant.message.send` | send logged with the human decision reference |

## HITL gates (hard stops)
- An amber gate in the closure package is presented amber - 02's no-rounding tuple.
- Deductible/coinsurance math carries its formula and source line in the record.

## Completion criteria
Financial records executed against authority and reconciled; closure package delivered.

## Abort paths
- Authority anomaly (stale estimate version, changed payee): hold + re-confirm; execution waits.
- Amber closure gate: package delivers with the amber named; closure is the human's call.
