---
name: P11-representation-notice-halt
description: "Swarm deployment: attorney/representation notice to claim-wide contact halt with a clean handoff package. Agents 01/04/05 (detection), 02, 12, 13. Absolute line 5: represented claimants are human-only - this playbook is the halt executing."
---

# Playbook P11 - Representation Notice Halt

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)

## Trigger
`representation.notice` from any detection channel: FNOL language (01), claimant channel (04), or documents (05).

## Preconditions
- The notice is captured verbatim with source, date, and the representative's stated identity - a halt anchored to a record, not a vibe.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Halt (same turn)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 04 | ALL direct claimant contact halts on the claim; pending outbound held | (hold; `agent.status` → 14) | held-message inventory exists |
| 2 | 02 | Claim posture set to represented; halt confirmed claim-wide | `claim.assignment` update → 12, 13 | posture on the claim record |

### Phase 2 - Package and re-anchor
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 13 | Claim file snapshot: notice verbatim, held messages, open items | `record.response` → 02 | handoff package complete |
| 4 | 12 | Fair-claims-practice clocks re-checked for represented posture | `deadline.alert` → 02, 14 (as needed) | every contact-based deadline re-anchored |
| 5 | 02 | Deliver the posture package for human direction on the channel | `closure.package`-style delivery → human, 13 | human direction requested with the full record |

## HITL gates (hard stops)
- No outbound to the claimant or representative from any agent until explicit human direction - inbound is logged and routed, never answered.
- No coverage statement in the held-message review or anywhere else (absolute line 1).

## Completion criteria
Contact halted claim-wide same turn, held inventory and file snapshot delivered, clocks re-anchored, human direction requested.

## Abort paths
- Notice authenticity uncertain (unsigned, unverifiable source): halt anyway; clarification to human - the conservative posture is the halt.
- Statutory contact required while halted (acknowledgment clocks): route to human with both obligations named - conflicts of law are human calls.
