---
name: P08-doi-inquiry-response
description: "Swarm deployment: regulator inquiry to a signature-ready response package inside the statutory window. Agents 12, 13, 05, 04. The human signs everything that leaves; the swarm's job is a complete package early."
---

# Playbook P08 - DOI Inquiry Response

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)

## Trigger
`doi.inquiry` routed to 12 from any intake point (01 at FNOL, 04 from a reply, human forward).

## Preconditions
- The inquiry document itself is on file verbatim; the response clock is instantiated from the regulator's date, conservatism rule applied.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Assemble (clock-led)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 12 | Instantiate the response clock; alert at ratified lead-times | `deadline.alert` → 02, 04, 14 | clock live, alerts armed |
| 2 | 12 | Pull the claim chronology and verbatim communications from the record | `record.request` → 13 | chronology attached to the package |
| 3 | 05 | Collect any response-supporting documents not already on file | `doc.received` → 02, 13 (support set) | support docs inventoried |

### Phase 2 - Human signature
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 12 | Deliver the signature-ready package; a certain shortfall is delivered early with the gap named | `doi.response.package` → human, 13 | package delivered inside lead-time; human signs and files |

## HITL gates (hard stops)
- Nothing goes to a regulator from the swarm - human signature always (12's legal line).
- Claimant communications pause on this claim only if the human directs; an inquiry is not a hold.

## Completion criteria
Signature-ready response package delivered inside the ratified lead-time.

## Abort paths
- Certain shortfall: deliver early with the gap named - a partial package on time beats a full one late.
- Regulator deadline ambiguity: conservatism rule; the earlier date governs.
