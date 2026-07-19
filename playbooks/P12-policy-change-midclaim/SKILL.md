---
name: P12-policy-change-midclaim
description: "Swarm deployment: discovered policy change (endorsement, cancellation, reinstatement) to re-anchored claim facts. Agents 03, 02, 08, 12, 13. A change re-opens verification forward - it never rewrites posted history, and it never becomes a coverage statement."
---

# Playbook P12 - Policy Change Mid-Claim

**Swarm:** DispatcherAgents Claim Swarm (Insurance)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off)

## Trigger
`policy.change.notice` at 03 from re-verify or carrier feed, differing from the policy facts the claim was anchored on.

## Preconditions
- The prior policy facts are on record with timestamps - a change is only a change against a recorded baseline.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Blast radius
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 03 | Report the change with both fact sets and timestamps | `policy.change.notice` → 02, 08, 12, 13 | old and new policy facts on record |
| 2 | 13 | Return every work product anchored on the prior facts | `record.response` → 02, 08 | affected-item list with citations |

### Phase 2 - Re-anchor
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3 | 08 | Valuation re-anchored to corrected facts; both bases named | `estimate.package` → 02, 11, 13 | delta shown as fact, not judgment |
| 4 | 12 | Statutory and contract clocks re-derived; conservatism rule | `deadline.alert` → 02, 04, 14 (as needed) | earlier date governs, on record |
| 5 | 02 | Human notified with the change package - determinations are licensed | `clarification.request` → human | human holds every coverage-adjacent call |

## HITL gates (hard stops)
- No coverage statement, implication, or reassurance to anyone at any step (absolute line 1) - the change is reported as fact only.
- Posted history never edited to match new facts - the change is recorded forward only.

## Completion criteria
Blast radius named, valuation and clocks re-anchored to corrected facts, human notified with both fact sets; posted history intact.

## Abort paths
- Change implies retroactive cancellation/rescission: human immediately with the full record - rescission is a legal conversation.
- Carrier feed and policy system disagree: both reported with timestamps; the discrepancy is the fact (03's discrepancy doctrine).
