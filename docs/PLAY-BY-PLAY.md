# Play-by-Play - What Actually Happens, Step by Step

Every playbook narrated as hub traffic: who moves, what envelope
carries it, and what proves the step happened. GENERATED from
claim_playbooks.py. The e2e suite
(tests_claim/test_playbooks_e2e_all.py) executes these exact
sequences against the real hub - this document describes what the
tests prove.

## P01 - FNOL to Assignment

*It starts when:* `claim.fnol` package lands at 02, any channel, any hour.

**Phase 1 - Verify and score (parallel)**

1. Agent 02: Score severity per ratified rubric; worst-case band on missing inputs, gap named.
   - Wire: `policy.verify.request` → 03
   - Proof it happened: score + gap list on the claim record
2. Agent 03: Verify policy status/limits/endorsements on date of loss from live systems.
   - Wire: `policy.verify.result` → 02, 13
   - Proof it happened: result with system timestamps
3. Agent 12: Instantiate jurisdiction clock set from assignment context.
   - Wire: (internal; alerts arm)
   - Proof it happened: clock set on record with lead-times

**Phase 2 - Assign (gated on Phase 1)**

4. Agent 02: Assign per matrix; out-of-matrix combinations go to human queue.
   - Wire: `claim.assignment` → 06, 12, 13
   - Proof it happened: assignment envelope acked; lapse/mismatch facts routed to human if present
5. Agent 02: Open document checklist for the line of business.
   - Wire: `doc.request` → 05
   - Proof it happened: checklist issued and logged
6. Agent 02: Acknowledgment to claimant per statutory template.
   - Wire: `claimant.message.request` → 04
   - Proof it happened: send logged with disclosure set

*It can stop early:*
- Policy 'not found' or lapsed: hold in intake-verified state; human direction resumes.
- Assignment matrix gap: human queue; playbook holds at Phase 2.

## P02 - Property Claim Lifecycle

*It starts when:* `claim.assignment` with line of business = property.

**Phase 1 - Evidence (parallel)**

1. Agent 05: Collect checklist docs; chase on cadence; anomalies to 09 as observations.
   - Wire: `doc.received` → 02, 08, 13
   - Proof it happened: item-level inventory current
2. Agent 06: Schedule inspection inside the severity SLA window; confirm access.
   - Wire: `inspection.schedule` fulfilled; result → 08, 13
   - Proof it happened: inspection result with verbatim findings
3. Agent 07: Coordinate mitigation vendors as requested; verify deliverables landed.
   - Wire: `vendor.status` → 02, 08, 13
   - Proof it happened: artifact-verified milestones

**Phase 2 - Valuation (gated on inspection + docs)**

4. Agent 08: Assemble estimate package, sources attached; variance report if estimates diverge.
   - Wire: `estimate.package` → 02, 11, 13
   - Proof it happened: package with methods, sources, variances

**Phase 3 - Human decision support**

5. Agent 02: Assemble closure package when all gates green; amber gates named.
   - Wire: `closure.package` → human, 13
   - Proof it happened: package delivered; human decision logged by 13
6. Agent 11: Execute payments/reserves ONLY on signed authority; records to 12/13.
   - Wire: `payment.record`, `reserve.record`
   - Proof it happened: records carry authority envelope_id
7. Agent 04: Status updates on the playbook cadence throughout.
   - Wire: `claimant.message.send`
   - Proof it happened: every send logged verbatim

*It can stop early:*
- Human coverage hold at any point: swarm freezes client-visible steps, records continue.
- Safety hold on inspection access: Phase 1 step 2 holds; hazard routed.

## P03 - Auto Claim Lifecycle

*It starts when:* `claim.assignment` with line of business = auto.

**Phase 1 - Evidence (parallel)**

1. Agent 05: Collect photos, police report, repair estimates per auto checklist.
   - Wire: `doc.received` → 02, 08, 13
   - Proof it happened: inventory current; police-report fault facts also fire `subro.signal`
2. Agent 06: Schedule appraisal (field or desk per severity band).
   - Wire: `inspection.result` → 08, 13
   - Proof it happened: appraisal findings verbatim
3. Agent 07: Rental coordination within policy terms from 03's verified limits.
   - Wire: `vendor.status` → 02, 13
   - Proof it happened: rental record with term basis attached

**Phase 2 - Valuation**

4. Agent 08: Estimate package; run total-loss threshold per jurisdiction; within-margin reported as within-margin.
   - Wire: `estimate.package` → 02, 11, 13
   - Proof it happened: package with threshold comparison as fact

**Phase 3 - Human decision support**

5. Agent 02: Closure package with all gates stated.
   - Wire: `closure.package` → human, 13
   - Proof it happened: human decision logged
6. Agent 11: Authority-gated payment/reserve records.
   - Wire: `payment.record` → 12, 13
   - Proof it happened: authority envelope_id attached

*It can stop early:*
- Human coverage hold: as P02.
- Total-loss crossing: this playbook holds valuation-forward steps pending human P04 direction.

## P04 - Total Loss Handling

*It starts when:* Human declares total loss on a claim (signed direction referencing 08's threshold fact).

**Phase 1 - Valuation support**

1. Agent 08: Assemble ACV package: comparables, approved-table depreciation, jurisdiction fees/taxes - all sourced.
   - Wire: `estimate.package` → 02, 11, 13
   - Proof it happened: ACV package; adjuster owns the number's use
2. Agent 05: Request title, lienholder, and odometer documents per total-loss checklist.
   - Wire: `doc.received` → 02, 13
   - Proof it happened: title docs inventoried; lienholder named

**Phase 2 - Human settlement (swarm supports records only)**

3. Agent 04: Send human-approved settlement communications; NOTHING off-template.
   - Wire: `claimant.message.send`
   - Proof it happened: sends logged; any claimant counter routes verbatim to human
4. Agent 11: Execute settlement payment on signed authority; lienholder split per authority terms.
   - Wire: `payment.record` → 12, 13
   - Proof it happened: records carry the authority and the split
5. Agent 02: Closure package post-payment with salvage/title status stated.
   - Wire: `closure.package` → human, 13
   - Proof it happened: human closes; 13 logs

*It can stop early:*
- Claimant counter-offer: route verbatim to human; all settlement communication holds.
- Lienholder document conflict: hold payment execution; human resolves.

## P05 - Fraud Referral

*It starts when:* 09's aggregated signal score crosses the owner-ratified threshold on a claim.

**Phase 1 - Package (silent to the lifecycle)**

1. Agent 09: Assemble referral package: signals, sources, timeline from 13's chronology.
   - Wire: `record.request` → 13
   - Proof it happened: chronology attached
2. Agent 09: Route the package to the human SIU decision-maker.
   - Wire: `fraud.referral` → human, 13
   - Proof it happened: referral logged; decision is human

**Phase 2 - Human decision (swarm posture unchanged)**

3. Agent 13: Register the SIU decision as a record entry when the human supplies it.
   - Wire: (record entry)
   - Proof it happened: decision on file; handling changes only on explicit human direction

*It can stop early:*
- Any request to alter claim handling on suspicion: integrity.violation; the playbook itself never touches the lifecycle.

## P06 - Subrogation Handoff

*It starts when:* `subro.signal` matching the recovery-opportunity checklist at 10.

**Phase 1 - Preserve (immediate)**

1. Agent 10: Issue evidence-preservation requests the moment the opportunity is identified.
   - Wire: `doc.request` → 05
   - Proof it happened: preservation requests logged with spoliation-window basis
2. Agent 05: Execute preservation: custody flags on physical-evidence pointers, retention holds via 13.
   - Wire: `doc.received` → 02, 08, 13
   - Proof it happened: custody status inventoried

**Phase 2 - Package**

3. Agent 10: Assemble demand package: liability basis, damages support from 08, evidence inventory, statute dates (shortest theory governs).
   - Wire: `subro.package` → human, 13
   - Proof it happened: package delivered; pursuit decision is human

*It can stop early:*
- Preservation vs. habitability conflict: immediate human escalation; neither clock silently sacrificed.
- Third-party carrier contact received: route verbatim; assembly continues unless human holds.

## P07 - Payment & Closure Records

*It starts when:* Signed `payment.authority` envelope arrives at 11, or 02 determines all closure gates green.

**Phase 1 - Execute on authority**

1. Agent 11: Verify authority signature context, estimate version, payee details; execute; anomalies hold + re-confirm.
   - Wire: `payment.record` → 12, 13
   - Proof it happened: record with authority envelope_id
2. Agent 12: Register the financial event against the claim's clocks.
   - Wire: (clock update)
   - Proof it happened: clock state current

**Phase 2 - Closure package**

3. Agent 02: Assemble closure package: docs complete, estimate final, payments reconciled, clocks satisfied - ambers named.
   - Wire: `closure.package` → human, 13
   - Proof it happened: package delivered; the human closes
4. Agent 04: Send closure communications on the approved template after the human's closure decision.
   - Wire: `claimant.message.send`
   - Proof it happened: send logged with the human decision reference

*It can stop early:*
- Authority anomaly (stale estimate version, changed payee): hold + re-confirm; execution waits.
- Amber closure gate: package delivers with the amber named; closure is the human's call.

## P08 - DOI Inquiry Response

*It starts when:* `doi.inquiry` routed to 12 from any intake point (01 at FNOL, 04 from a reply, human forward).

**Phase 1 - Assemble (clock-led)**

1. Agent 12: Instantiate the response clock; alert at ratified lead-times.
   - Wire: `deadline.alert` → 02, 04, 14
   - Proof it happened: clock live, alerts armed
2. Agent 12: Pull the claim chronology and verbatim communications from the record.
   - Wire: `record.request` → 13
   - Proof it happened: chronology attached to the package
3. Agent 05: Collect any response-supporting documents not already on file.
   - Wire: `doc.received` → 02, 13 (support set)
   - Proof it happened: support docs inventoried

**Phase 2 - Human signature**

4. Agent 12: Deliver the signature-ready package; a certain shortfall is delivered early with the gap named.
   - Wire: `doi.response.package` → human, 13
   - Proof it happened: package delivered inside lead-time; human signs and files

*It can stop early:*
- Certain shortfall: deliver early with the gap named - a partial package on time beats a full one late.
- Regulator deadline ambiguity: conservatism rule; the earlier date governs.

## P09 - Morning Operations

*It starts when:* Scheduled daily start (owner-configured time) or owner command.

**Assemble (parallel, all to human review)**

1. Agent 14: Pull overnight intake and lifecycle exceptions from the record.
   - Wire: `record.request` → 13
   - Proof it happened: overnight section sourced
2. Agent 14: Pull today's clock alerts and lead-time exposures.
   - Wire: (from 12's `deadline.alert` stream)
   - Proof it happened: clock section current with lead-times
3. Agent 14: Assemble the inspection calendar and aging-claim exceptions.
   - Wire: (from record pulls)
   - Proof it happened: calendar + exceptions sections sourced

**Present**

4. Agent 14: Deliver the morning book; sections with unavailable sources marked absent.
   - Wire: `report.package` → human
   - Proof it happened: book delivered; the human directs, the book never self-executes

*It can stop early:*
- Record source down: section marked absent; book still delivers on time.

## P10 - End-of-Day Books

*It starts when:* Scheduled day end (owner-configured time) or owner command.

**Assemble**

1. Agent 14: Pull the day's full activity chronology.
   - Wire: `record.request` → 13
   - Proof it happened: activity section sourced with timestamps
2. Agent 14: Reconcile clocks: advanced, satisfied, at-risk, missed - misses quantified.
   - Wire: (from 12's alert stream + records)
   - Proof it happened: clock reconciliation complete
3. Agent 14: Missed-item sweep: every morning-book item without a day touch, named with its owner.
   - Wire: (sweep vs. P09 baseline)
   - Proof it happened: sweep list complete; no silent reassignment

**Present**

4. Agent 14: Deliver the EOD books.
   - Wire: `report.package` → human
   - Proof it happened: books delivered and logged; P10 completion event on the log for tomorrow's P09

*It can stop early:*
- Morning baseline absent: sweep names that first and proceeds on records alone.

## P11 - Representation Notice Halt

*It starts when:* `representation.notice` from any detection channel: FNOL language (01), claimant channel (04), or documents (05).

**Phase 1 - Halt (same turn)**

1. Agent 04: ALL direct claimant contact halts on the claim; pending outbound held.
   - Wire: (hold; `agent.status` → 14)
   - Proof it happened: held-message inventory exists
2. Agent 02: Claim posture set to represented; halt confirmed claim-wide.
   - Wire: `claim.assignment` update → 12, 13
   - Proof it happened: posture on the claim record

**Phase 2 - Package and re-anchor**

3. Agent 13: Claim file snapshot: notice verbatim, held messages, open items.
   - Wire: `record.response` → 02
   - Proof it happened: handoff package complete
4. Agent 12: Fair-claims-practice clocks re-checked for represented posture.
   - Wire: `deadline.alert` → 02, 14 (as needed)
   - Proof it happened: every contact-based deadline re-anchored
5. Agent 02: Deliver the posture package for human direction on the channel.
   - Wire: `closure.package`-style delivery → human, 13
   - Proof it happened: human direction requested with the full record

*It can stop early:*
- Notice authenticity uncertain (unsigned, unverifiable source): halt anyway; clarification to human - the conservative posture is the halt.
- Statutory contact required while halted (acknowledgment clocks): route to human with both obligations named - conflicts of law are human calls.

## P12 - Policy Change Mid-Claim

*It starts when:* `policy.change.notice` at 03 from re-verify or carrier feed, differing from the policy facts the claim was anchored on.

**Phase 1 - Blast radius**

1. Agent 03: Report the change with both fact sets and timestamps.
   - Wire: `policy.change.notice` → 02, 08, 12, 13
   - Proof it happened: old and new policy facts on record
2. Agent 13: Return every work product anchored on the prior facts.
   - Wire: `record.response` → 02, 08
   - Proof it happened: affected-item list with citations

**Phase 2 - Re-anchor**

3. Agent 08: Valuation re-anchored to corrected facts; both bases named.
   - Wire: `estimate.package` → 02, 11, 13
   - Proof it happened: delta shown as fact, not judgment
4. Agent 12: Statutory and contract clocks re-derived; conservatism rule.
   - Wire: `deadline.alert` → 02, 04, 14 (as needed)
   - Proof it happened: earlier date governs, on record
5. Agent 02: Human notified with the change package - determinations are licensed.
   - Wire: `clarification.request` → human
   - Proof it happened: human holds every coverage-adjacent call

*It can stop early:*
- Change implies retroactive cancellation/rescission: human immediately with the full record - rescission is a legal conversation.
- Carrier feed and policy system disagree: both reported with timestamps; the discrepancy is the fact (03's discrepancy doctrine).

## P13 - Salvage & Recovery Cascade

*It starts when:* `salvage.record` at 10 (from valuation 08 or posted proceeds 11), or an accepted `subro.package` returning as a recovery to execute.

**Phase 1 - Assemble**

1. Agent 10: Recovery package: subro facts, salvage values, netting arithmetic shown.
   - Wire: `subro.package` → human, 13
   - Proof it happened: every number carries its source
2. Agent 13: Claim-file support attached (existence/type/date/source).
   - Wire: `record.response` → 10
   - Proof it happened: file citations complete

**Phase 2 - Signed execution**

3. Agent 10: Demand issues / acceptance executes on signed authority only.
   - Wire: (await `recovery.authority` ← human)
   - Proof it happened: signed envelope on the chain first
4. Agent 11: Proceeds post; books reconcile to $0.00 variance.
   - Wire: `payment.record` + `salvage.record` → 12, 13
   - Proof it happened: reconciliation clean or exception raised

*It can stop early:*
- Counterparty disputes liability or amount: package the dispute verbatim for the human - the swarm never negotiates.
- Proceeds do not reconcile to the posted expectation: reconciliation.exception; the variance is named, never absorbed.

## P14 - Records Request Response

*It starts when:* External records request lands: claimant file access, examination, audit, or litigation discovery notice (which also fires P11 if it carries representation).

**Phase 1 - Clock and inventory**

1. Agent 12: Arm the response clock (regulatory default if none stated).
   - Wire: `deadline.alert` → 02, 14 (at lead-times)
   - Proof it happened: clock live
2. Agent 13: Disclosure inventory: existence, type, date, source per item.
   - Wire: `records.disclosure.package` → human, 12
   - Proof it happened: inventory delivered inside lead-time
3. Agent 05: Flag items with privilege/work-product markers or third-party content.
   - Wire: `doc.received` → 13 (marker references)
   - Proof it happened: flag status per item - flagged, not judged

**Phase 2 - Human release**

4. Agent 13: Record the human's release decision and what was disclosed.
   - Wire: `record.response` + `interaction.log`
   - Proof it happened: disclosure record: who, what, when, under whose approval
5. Agent 04/02: Transmit per the approved scope (claimant lane via 04 unless represented - then human-only).
   - Wire: `claimant.message.send` / human handoff
   - Proof it happened: transmission artifact on record

*It can stop early:*
- Scope ambiguous or overbroad: clarification to human before any work product leaves the swarm.
- Request is litigation discovery: human immediately - discovery response is counsel's lane, the swarm only inventories.
