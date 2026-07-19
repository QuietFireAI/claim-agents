# TUNING_MANUAL - claim-agents

Every configurable parameter, placeholder, and ratification in this identity.
Rule (inherited doctrine): any commit introducing a tunable updates this
manual in the same commit.

---

## TOP OF LIST - Deliberate placeholders & unratified content (read before deployment)

Full sweep 2026-07-18: everything stubbed, templated, or pending sign-off is
listed here. If it's not in this table it's ratified content or real spec.

| Item | Where | Status | What blocks / what to do |
|---|---|---|---|
| Signer identity | `config/authority_signers.json` | **RATIFIED FOR TEST 2026-07-18** — "Dr. Jeff Phillips" is a fictional test persona | Demo/test only. Production MUST replace `signer_login` with a real IdP login before go-live; the IdP seam (INTEGRATIONS.md) is a go-live prerequisite for any authority intent. |
| Reserve/payment rule entries | `config/reserve_rules.json` | **DOCTRINE RATIFIED / entries empty** | Empty table is fail-closed by structure: nothing matches, nothing moves unsigned. Load ratified carrier rules at deployment. |
| Fraud signal categories | `config/fraud_signal_taxonomy.json` | **DOCTRINE RATIFIED / entries deployment content** | Silent-aggregation + signed-endings doctrine binding; refine categories against the book of business. |
| Carrier rule table | `config/carrier_rule_table.json` | **DEPLOYMENT CONTENT** | Owner-ratified version required before lifecycle playbooks run. |
| Vendor panel | `config/vendor_panel.json` | **UNRATIFIED — fails closed** | Needs your actual vendor relationships; loads refuse while UNRATIFIED stands. |
| Message templates | `config/message_templates.json` | **UNRATIFIED — awaiting owner sign-off per template** | Fill `approved_by` per template to ratify wording (includes new `representation_acknowledged`). |
| Runtime | whole repo | **BLUEPRINT, not runtime-hardened** | Side-loads into the dispatcher-agents runtime; no working build exists yet (owner decision 2026-07-18, Option A). |

---

## Ratified (owner: Jeff Phillips, 2026-07-18)

| Parameter | Value | Consumer |
|---|---|---|
| Books reconciliation tolerance | **$0.00** — permeates all blueprints | 11 → `reconciliation.exception` |
| Zero-threshold money doctrine | contract/rule-matching auto-applies with citation; everything else signed, any amount | 11, 10 |
| Representation halt | same-turn, claim-wide, conservative on uncertain authenticity | P11 (class 1) |
| Statutory clock conservatism | earlier date governs, escalate before the miss | 12 (pre-existing doctrine, restated) |

### The $0.00 rule (permeates ALL identity blueprints - owner decision 2026-07-18)

Any variance between posted money and reconciled books, any amount, is a
`reconciliation.exception` routed to the human and the books. No "close
enough" lane, no de-minimis write-down. The HITL is notified on every
variance. Identity-independent doctrine.

---

## PROPOSED thresholds — pending owner ratification

These numbers are proposals, not ratified. They fail to the conservative
side until the owner ratifies or amends them (statutory rules always govern
where shorter).

| Parameter | Proposed | Consumer |
|---|---|---|
| FNOL acknowledgment SLA | 24 hours | 01/04, P01 |
| Claimant status-update cadence | every 30 days on open claims | 04, fair-claims practice |
| Inspection scheduling SLA | 72 hours from assignment | 06 |
| DOI response lead-time alert | 10 days before deadline | 12 (P08) |
| DOI response escalation | 3 days before deadline | 12 (P08) |
| Records-response lead alert / escalation | 10 / 3 days | 12 (P14) |
| Reserve review staleness | 90 days | 11 |
| Salvage/recovery follow-up trigger | 30 days without counterparty response | 10 (P13) |

---

## Regulatory clocks (fixed by law/contract, not tunable - listed for completeness)

| Clock | Basis | Playbook |
|---|---|---|
| Fair-claims acknowledgment/decision windows | state UCPA / DOI regs (varies) | P01, P02, P03 |
| DOI inquiry response deadlines | per inquiry / state reg | P08 |
| Records/file access response | state claim-file access rules | P14 |

Conservatism rule governs every derivation: the earlier date wins, and the
clock escalates before the miss (absolute line 4 doctrine).
