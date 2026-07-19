---
name: P04-total-loss-handling
description: "Swarm deployment: human-declared total loss through valuation support, title docs, and settlement records. Agents 02, 04, 05, 08, 11, 13. Every settlement conversation is human; the swarm handles paper and records."
---

# Playbook P04 - Total Loss Handling

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.2 (ratified 2026-07-18; extended & ratified 2026-07-18 - owner sign-off)

## Trigger
Human declares total loss on a claim (signed direction referencing 08's threshold fact).

## Preconditions
- Human total-loss declaration on file; P02/P03 evidence base current.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Valuation support
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 08 | Assemble ACV package: comparables, approved-table depreciation, jurisdiction fees/taxes - all sourced | `estimate.package` → 02, 11, 13 | ACV package; adjuster owns the number's use |
| 2 | 05 | Request title, lienholder, and odometer documents per total-loss checklist | `doc.received` → 02, 13 | title docs inventoried; lienholder named |

### Phase 2 - Human settlement (swarm supports records only)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 04 | Send human-approved settlement communications; NOTHING off-template | `claimant.message.send` | sends logged; any claimant counter routes verbatim to human |
| 4 | 11 | Execute settlement payment on signed authority; lienholder split per authority terms | `payment.record` → 12, 13 | records carry the authority and the split |
| 5 | 02 | Closure package post-payment with salvage/title status stated | `closure.package` → human, 13 | human closes; 13 logs |

## HITL gates (hard stops)
- Negotiation is human end to end - a claimant counter-offer never gets a swarm response beyond the routing acknowledgment template.
- Lienholder payoff figures come from documents on file, never from phone summaries.

## Completion criteria
Settlement payment recorded against signed authority; title/lien docs on file; closure package delivered.

## Abort paths
- Claimant counter-offer: route verbatim to human; all settlement communication holds.
- Lienholder document conflict: hold payment execution; human resolves.
