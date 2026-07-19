# Playbooks P01-P14 - Insurance Claim Swarm

The consolidated catalog. Full per-playbook SKILL.md files live in
playbooks/. GENERATED from claim_playbooks.py.

## P01 - FNOL to Assignment

Swarm deployment: reported loss to verified, assigned, clock-instantiated claim. Agents 01, 02, 03, 12, 13. The speed-to-FNOL front door - acknowledgment and assignment SLAs run from first contact.

**Trigger:** `claim.fnol` package lands at 02, any channel, any hour.

**HITL gates (hard stops):**
- Phase 2 does not start on an unverified policy - 'not found' holds in intake-verified state (02 tuple).
- Injury/fatality flags route the human notification inside the acknowledgment SLA, not after it.

**Done means:** Claim verified, scored, assigned per matrix, clocks live, checklist issued, acknowledgment sent - all inside the acknowledgment SLA.

## P02 - Property Claim Lifecycle

Swarm deployment: assigned property claim through docs, inspection, estimate, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 12, 13. The human decides coverage and closure; the swarm keeps every gate visible.

**Trigger:** `claim.assignment` with line of business = property.

**HITL gates (hard stops):**
- No figure leaves the swarm: 08's numbers are adjuster work product only.
- Payment execution without signed `payment.authority` is an integrity violation, not an error.

**Done means:** Closure package delivered to the human with every gate stated; post-decision records complete.

## P03 - Auto Claim Lifecycle

Swarm deployment: assigned auto claim through appraisal, valuation, rental coordination, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 13. Total-loss threshold checks fire as facts to the adjuster.

**Trigger:** `claim.assignment` with line of business = auto.

**HITL gates (hard stops):**
- Unlisted-driver or unlisted-vehicle facts route to the human as facts (03's rule) - the lifecycle continues unless the human holds it.
- Total-loss crossing triggers P04 on human direction, never automatically.

**Done means:** Closure package delivered with threshold facts stated; records reconciled.

## P04 - Total Loss Handling

Swarm deployment: human-declared total loss through valuation support, title docs, and settlement records. Agents 02, 04, 05, 08, 11, 13. Every settlement conversation is human; the swarm handles paper and records.

**Trigger:** Human declares total loss on a claim (signed direction referencing 08's threshold fact).

**HITL gates (hard stops):**
- Negotiation is human end to end - a claimant counter-offer never gets a swarm response beyond the routing acknowledgment template.
- Lienholder payoff figures come from documents on file, never from phone summaries.

**Done means:** Settlement payment recorded against signed authority; title/lien docs on file; closure package delivered.

## P05 - Fraud Referral

Swarm deployment: threshold-crossing signal record to SIU referral package. Agents 09, 13, plus contributing observers. The claim's normal lifecycle NEVER changes - delay-on-suspicion is the named illegal move.

**Trigger:** 09's aggregated signal score crosses the owner-ratified threshold on a claim.

**HITL gates (hard stops):**
- No agent's behavior on the claim changes at referral - schedules, payments-on-authority, and communications continue exactly per playbook.
- The referral's existence is need-to-know sealed (09's tuple); no cross-agent disclosure.

**Done means:** Referral package delivered to the human SIU decision-maker; lifecycle posture verified unchanged.

## P06 - Subrogation Handoff

Swarm deployment: recovery signal to preserved evidence and demand package for human pursuit. Agents 10, 05, 08, 13. Preservation fires immediately; the pursuit decision waits for no artifact.

**Trigger:** `subro.signal` matching the recovery-opportunity checklist at 10.

**HITL gates (hard stops):**
- Habitability/repair urgency versus preservation conflicts escalate immediately (10's tuple) - neither clock is silently sacrificed.
- No contact with the third party or their carrier originates from the swarm.

**Done means:** Evidence preserved with custody flags; demand package delivered for human pursuit decision.

## P07 - Payment & Closure Records

Swarm deployment: signed authority to executed, reconciled, compliance-visible financial records and the closure package. Agents 11, 12, 02, 13. Records only - authority moves money, the swarm moves paper.

**Trigger:** Signed `payment.authority` envelope arrives at 11, or 02 determines all closure gates green.

**HITL gates (hard stops):**
- An amber gate in the closure package is presented amber - 02's no-rounding tuple.
- Deductible/coinsurance math carries its formula and source line in the record.

**Done means:** Financial records executed against authority and reconciled; closure package delivered.

## P08 - DOI Inquiry Response

Swarm deployment: regulator inquiry to a signature-ready response package inside the statutory window. Agents 12, 13, 05, 04. The human signs everything that leaves; the swarm's job is a complete package early.

**Trigger:** `doi.inquiry` routed to 12 from any intake point (01 at FNOL, 04 from a reply, human forward).

**HITL gates (hard stops):**
- Nothing goes to a regulator from the swarm - human signature always (12's legal line).
- Claimant communications pause on this claim only if the human directs; an inquiry is not a hold.

**Done means:** Signature-ready response package delivered inside the ratified lead-time.

## P09 - Morning Operations

Swarm deployment: the claims desk's morning book. Overnight FNOLs, today's clocks, the inspection calendar, aging exceptions - assembled from records and presented for human review before the day starts. Agents 14, 13, 12.

**Trigger:** Scheduled daily start (owner-configured time) or owner command.

**HITL gates (hard stops):**
- A source unavailable at assembly time is a named absence - never yesterday's numbers backfilled (14's tuple).

**Done means:** Morning book delivered to the human with every section sourced or marked absent.

## P10 - End-of-Day Books

Swarm deployment: the closing books. Every claim touched, every clock advanced or missed, the missed-item sweep against the morning book. Agents 14, 13, 12. Gaps named; a clean-looking book with hidden gaps is the named failure.

**Trigger:** Scheduled day end (owner-configured time) or owner command.

**HITL gates (hard stops):**
- The sweep never reassigns - it names (14's tuple). Reassignment is the human's morning decision.

**Done means:** EOD books delivered; sweep complete with owners named; completion event logged for tomorrow's P09.

## P11 - Representation Notice Halt

Swarm deployment: attorney/representation notice to claim-wide contact halt with a clean handoff package. Agents 01/04/05 (detection), 02, 12, 13. Absolute line 5: represented claimants are human-only - this playbook is the halt executing.

**Trigger:** `representation.notice` from any detection channel: FNOL language (01), claimant channel (04), or documents (05).

**HITL gates (hard stops):**
- No outbound to the claimant or representative from any agent until explicit human direction - inbound is logged and routed, never answered.
- No coverage statement in the held-message review or anywhere else (absolute line 1).

**Done means:** Contact halted claim-wide same turn, held inventory and file snapshot delivered, clocks re-anchored, human direction requested.

## P12 - Policy Change Mid-Claim

Swarm deployment: discovered policy change (endorsement, cancellation, reinstatement) to re-anchored claim facts. Agents 03, 02, 08, 12, 13. A change re-opens verification forward - it never rewrites posted history, and it never becomes a coverage statement.

**Trigger:** `policy.change.notice` at 03 from re-verify or carrier feed, differing from the policy facts the claim was anchored on.

**HITL gates (hard stops):**
- No coverage statement, implication, or reassurance to anyone at any step (absolute line 1) - the change is reported as fact only.
- Posted history never edited to match new facts - the change is recorded forward only.

**Done means:** Blast radius named, valuation and clocks re-anchored to corrected facts, human notified with both fact sets; posted history intact.

## P13 - Salvage & Recovery Cascade

Swarm deployment: salvage value and subrogation facts to signed, executed recovery. Agents 08, 11, 10, 13. Recovery is money: demands, acceptances, and reserve effects move only on signed authority.

**Trigger:** `salvage.record` at 10 (from valuation 08 or posted proceeds 11), or an accepted `subro.package` returning as a recovery to execute.

**HITL gates (hard stops):**
- No demand, settlement acceptance, or waiver moves without signed `recovery.authority` - recovery is money, same doctrine as payments.
- Netting is arithmetic shown, never judgment applied - allocation questions route to the human.

**Done means:** Recovery executed on signed authority, proceeds posted, books at $0.00 variance; or the blocking question named to the human.

## P14 - Records Request Response

Swarm deployment: external records request to human-approved disclosure inside the response clock. Agents 13, 12, 05, 04, 02. The swarm inventories existence; a human approves every release - privilege and privacy are human calls.

**Trigger:** External records request lands: claimant file access, examination, audit, or litigation discovery notice (which also fires P11 if it carries representation).

**HITL gates (hard stops):**
- Nothing beyond the approved item list transmits - the human's itemized approval is the ceiling.
- Privilege and work-product calls are human-only - the swarm flags markers, it never decides what is protected.
- If the claim is represented, transmission is human-only end to end (absolute line 5).

**Done means:** Human-approved disclosure transmitted inside the clock with a complete itemized record; or refusal/clarification recorded the same way.
