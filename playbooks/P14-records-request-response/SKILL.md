---
name: P14-records-request-response
description: "Swarm deployment: external records request to human-approved disclosure inside the response clock. Agents 13, 12, 05, 04, 02. The swarm inventories existence; a human approves every release - privilege and privacy are human calls."
---

# Playbook P14 - Records Request Response

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.2 (ratified 2026-07-18; extended & ratified 2026-07-18 - owner sign-off)

## Trigger
External records request lands: claimant file access, examination, audit, or litigation discovery notice (which also fires P11 if it carries representation).

## Preconditions
- The request is captured verbatim with date, requester, scope, and stated deadline (or the regulatory default).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Clock and inventory
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 12 | Arm the response clock (regulatory default if none stated) | `deadline.alert` → 02, 14 (at lead-times) | clock live |
| 2 | 13 | Disclosure inventory: existence, type, date, source per item | `records.disclosure.package` → human, 12 | inventory delivered inside lead-time |
| 3 | 05 | Flag items with privilege/work-product markers or third-party content | `doc.received` → 13 (marker references) | flag status per item - flagged, not judged |

### Phase 2 - Human release
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 13 | Record the human's release decision and what was disclosed | `record.response` + `interaction.log` | disclosure record: who, what, when, under whose approval |
| 5 | 04/02 | Transmit per the approved scope (claimant lane via 04 unless represented - then human-only) | `claimant.message.send` / human handoff | transmission artifact on record |

## HITL gates (hard stops)
- Nothing beyond the approved item list transmits - the human's itemized approval is the ceiling.
- Privilege and work-product calls are human-only - the swarm flags markers, it never decides what is protected.
- If the claim is represented, transmission is human-only end to end (absolute line 5).

## Completion criteria
Human-approved disclosure transmitted inside the clock with a complete itemized record; or refusal/clarification recorded the same way.

## Abort paths
- Scope ambiguous or overbroad: clarification to human before any work product leaves the swarm.
- Request is litigation discovery: human immediately - discovery response is counsel's lane, the swarm only inventories.
