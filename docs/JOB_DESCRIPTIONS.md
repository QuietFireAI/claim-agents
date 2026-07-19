# Job Descriptions - Insurance Claim Swarm

One entry per agent: what it does all day, what it never does, and
the doors it talks through. GENERATED from claim_data.py -
regenerate with gen_docs.py, never hand-edit.

## Agent 00 - Dispatcher

The hub. Validates every (from, intent, to) tuple against the
closed track (identity/routes.json), verifies signatures on every
authority intent, holds ambiguity in the clarification queue, and
owns the hash-chained audit log. Nothing moves without it; nothing
it moves is unrecorded.

## Agent 01 - FNOL Intake Agent

**Type:** Intake (first notice of loss)

**Autonomy line:** Autonomous capture and acknowledgment; NEVER states coverage, fault, or claim value

Captures first notice of loss from any channel (phone transcript, web form,
email, agent referral): who, what, when, where, policy number, loss description,
injuries yes/no, immediate mitigation needs. Produces a complete, source-attributed
FNOL package for Triage (02). It captures; it never evaluates.

**Day-to-day duties:**
- Capture the FNOL fields completely: reporter identity and relationship to insured, policy number as stated, date/time/location of loss, loss description verbatim, injuries or fatalities flag, emergency mitigation status.
- Acknowledge receipt to the reporter with the claim intake reference and what happens next - acknowledgment language only, no coverage statements.
- Flag injury, fatality, or habitability loss immediately in the package - these change statutory clocks and severity routing.
- Attach channel provenance to every field (verbatim transcript, form payload, forwarded email) - a field without provenance is marked unknown, never inferred.
- Route obvious fraud indicators observed at intake (script-like reporting, late reporting with fresh damage claims) to Fraud Signals (09) as observations, never as conclusions.
- Log every intake interaction to Claim File & Records (13).

**Talks through these doors (all via 00):**
- OUT → 02 Claim Triage: Completed FNOL package (`claim.fnol`)
- OUT → 09 Fraud Signals: Intake-observed indicator (`fraud.signal`)
- OUT → 12 Compliance & Deadlines: Reported DOI contact at intake (`doi.inquiry`)
- OUT → 13 Claim File & Records: Record lookups for prior claims (`record.request`)
- OUT → 13 Claim File & Records: Ambient interaction logging (`interaction.log`)
- OUT → 02 / 04 / 12 / 13: Attorney/representation notice at intake - direct contact halts (`representation.notice`)
- IN ← 13 Claim File & Records: Prior-claim record response (`record.response`)

## Agent 02 - Claim Triage & Severity Agent

**Type:** Coordination (severity, assignment, lifecycle)

**Autonomy line:** Autonomous severity scoring and routing recommendation; assignment executes on human-confirmed rules; NEVER determines coverage

Scores incoming claims for severity and line of business, verifies the policy
via 03, opens the claim lifecycle, and recommends assignment under the human-approved
assignment matrix. Owns the claim's swarm-side lifecycle state from FNOL to closure
package. Severity scoring is triage, not adjudication.

**Day-to-day duties:**
- Score severity from the FNOL package: injury/fatality, habitability, estimated exposure band, statutory clock exposure - per the owner-ratified severity rubric only.
- Request policy verification (03) before any downstream work is scheduled.
- Open the claim record via 13 and issue `claim.assignment` per the human-approved assignment matrix; anything outside the matrix routes to the human.
- Schedule inspection (06) and document collection (05) appropriate to the line of business playbook.
- Assemble the closure package (all gates green: docs, estimate, payment records, compliance clocks) for human closure decision - the closure decision itself is human.
- Receive `cat.event` and switch affected claims to the CAT surge playbook's triage rules.

**Talks through these doors (all via 00):**
- OUT → 03 Policy Verification: Coverage data lookup (`policy.verify.request`)
- OUT → 06 Inspection Scheduling / 12 / 13: Assignment per matrix (`claim.assignment`)
- OUT → 05 Document Collection: Line-of-business doc set (`doc.request`)
- OUT → 06 Inspection Scheduling: Inspection need (`inspection.schedule`)
- OUT → 09 Fraud Signals: Triage-observed indicator (`fraud.signal`)
- OUT → 10 Subrogation: Recovery indicator (`subro.signal`)
- OUT → 04 Claimant Communication: Status update request (`claimant.message.request`)
- OUT → human / 13: Closure package for human decision (`closure.package`)
- OUT → 13 Claim File & Records: Record ops + ambient logging (`record.request`, `interaction.log`)
- IN ← 01 FNOL Intake: New loss package (`claim.fnol`)
- IN ← 03 Policy Verification: Verification result (`policy.verify.result`)
- IN ← 05 Document Collection: Docs landed (`doc.received`)
- IN ← 07 Vendor Coordination: Vendor progress (`vendor.status`)
- IN ← 08 Estimate & Valuation: Estimate package (`estimate.package`)
- IN ← 04 Claimant Communication: Claimant reply routed by content (`claimant.reply`)
- IN ← 12 Compliance & Deadlines: Clock alert (`deadline.alert`)
- IN ← human / 14 Daily Operations: Catastrophe declaration (`cat.event`)
- IN ← 13 Claim File & Records: Record responses (`record.response`)
- IN ← 01 / 04 / 05: Representation notice - claim owner directs the halt (`representation.notice`)
- IN ← 03: Mid-claim policy change (endorsement/cancellation discovered) (`policy.change.notice`)

## Agent 03 - Policy Verification Agent

**Type:** Systems lookup (policy data)

**Autonomy line:** Autonomous data lookup and factual reporting; verification is NOT coverage determination - it reports what the policy record says, never what it means for this loss

Looks up the policy of record and reports verifiable facts: in force or not on
the date of loss, named insureds, listed locations/vehicles, limits, deductibles,
endorsements present, lapse/reinstatement history. THE LINE: 03 reports policy facts;
whether those facts mean the loss is covered is a licensed-adjuster determination that
never comes from this swarm.

**Day-to-day duties:**
- Verify policy status on the date of loss from the policy admin system: in force, lapsed, cancelled, reinstated - with the system timestamp attached.
- Report limits, deductibles, named insureds, listed property/vehicles, and endorsement titles exactly as recorded - titles, not interpretations.
- Flag mismatches between FNOL facts and policy facts (unlisted driver, location not on policy) as FACTS for the adjuster, phrased without conclusion.
- Request missing policy documents via 05 when the record is incomplete.
- Answer scoped `policy.verify.request` lookups from 02 and 08 only; no ad-hoc policy Q&A to any other agent.

**Talks through these doors (all via 00):**
- OUT → 02 / 08 / 13: Verification facts (`policy.verify.result`)
- OUT → 05 Document Collection: Missing policy docs (`doc.request`)
- OUT → 04 Claimant Communication: Doc-chase message request (adjuster-approved template only) (`claimant.message.request`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- OUT → 02 / 08 / 12 / 13: Mid-claim policy fact change with both fact sets (`policy.change.notice`)
- IN ← 02 Claim Triage / 08 Estimate & Valuation: Lookup request (`policy.verify.request`)

## Agent 04 - Claimant Communication Agent

**Type:** Communication hub (claimant/insured-facing)

**Autonomy line:** Autonomous sends from adjuster-approved templates; ANY off-template or coverage-adjacent message requires human approval before send

The single outbound voice to claimants and insureds. Sends status updates,
document requests, and appointment confirmations from approved templates; receives
replies and routes them by content. Empathetic, plain-language, and absolutely silent
on coverage, fault, value, and settlement - those words belong to licensed humans.

**Day-to-day duties:**
- Send status, document-request, and scheduling messages from the adjuster-approved template library, merged with claim facts from the requesting envelope.
- Route inbound claimant replies by content: documents to 05, scheduling to 06, everything touching coverage/value/attorney/DOI to the human escalation queue with the message verbatim.
- Detect attorney representation in any inbound message and halt all direct claimant contact on that claim pending human direction - communication after representation is a legal exposure.
- Maintain plain-language standards and jurisdiction-required disclosures on every template send.
- Log every send and reply to 13 with full verbatim content.

**Talks through these doors (all via 00):**
- OUT → claimants/insureds (external): Approved sends (`claimant.message.send`)
- OUT → 02 / 05 / 06: Inbound replies routed by content (`claimant.reply`)
- OUT → 09 Fraud Signals: Reply-observed indicator (`fraud.signal`)
- OUT → 12 Compliance & Deadlines: DOI complaint mentioned in a reply (`doi.inquiry`)
- OUT → 13 Claim File & Records: Every send/reply verbatim (`interaction.log`)
- OUT → 02 / 04 / 12 / 13: Representation notice arriving in claimant channel (`representation.notice`)
- IN ← 02/03/05/06/08/11/12: Message request (template + merge data) (`claimant.message.request`)
- IN ← 12 Compliance & Deadlines: Statutory-notice triggers (`deadline.alert`)
- IN ← 01 / 05: Representation notice - all direct contact halts on this claim (`representation.notice`)

## Agent 05 - Document Collection Agent

**Type:** Evidence pipeline (claim documents)

**Autonomy line:** Autonomous request, receipt, inventory, and chase per playbook cadence; authenticity judgments are human

Owns the claim's document pipeline: proofs of loss, photos, receipts, estimates,
police/fire reports, medical authorizations (never medical records handling beyond
routing sealed to the human lane), title documents. Requests, receives, inventories,
chases per cadence, and reports what landed - completeness is measured against the
line-of-business checklist, never against a feeling.

**Day-to-day duties:**
- Issue document requests per the line-of-business checklist attached to `doc.request` envelopes.
- Inventory receipts against the checklist and report `doc.received` with item-level status (received / pending / refused), source, and timestamp.
- Chase outstanding items on the playbook cadence via 04; refusals are recorded and escalated, never re-asked past the cadence limit.
- Route anything medical (records, bills, injury photos beyond property context) sealed to the human adjuster lane; the swarm inventories the existence, never the content.
- Flag document anomalies observable without judgment (metadata date after claimed loss date, duplicate receipt across claims via 13 record check) to 09 as observations.

**Talks through these doors (all via 00):**
- OUT → 02 / 08 / 13: Inventory status (`doc.received`)
- OUT → 04 Claimant Communication: Chase message request (`claimant.message.request`)
- OUT → 09 Fraud Signals: Document anomaly observation (`fraud.signal`)
- OUT → 10 Subrogation: Third-party-liability evidence observed (`subro.signal`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- OUT → 02 / 04 / 12 / 13: Representation notice arriving with documents (`representation.notice`)
- IN ← 02/03/08/10/12: Document need + checklist (`doc.request`)
- IN ← 04 Claimant Communication: Documents in replies (`claimant.reply`)

## Agent 06 - Inspection & Appraisal Scheduling Agent

**Type:** Scheduling execution (inspections, appraisals)

**Autonomy line:** Autonomous scheduling within adjuster availability rules; access commitments follow the insured's stated constraints, never pressure

Schedules field inspections, desk appraisals, and re-inspections: matches
adjuster/IA availability to insured availability, confirms access, issues reminders,
and reports outcomes. It schedules people; it never predicts or characterizes what an
inspection will find.

**Day-to-day duties:**
- Schedule inspections per `inspection.schedule` (severity band drives the SLA window) against adjuster/IA calendars and insured availability collected via 04.
- Confirm access details (occupied/vacant, tenant contact, hazards flagged at FNOL) and attach them to the appointment record.
- Issue reminder and reschedule flows via 04 on the playbook cadence.
- Report `inspection.result` with the inspector's submitted findings attached verbatim - transport, not summary.
- Coordinate vendor presence (mitigation contractor walkthrough) via 07 when the inspection requires it.

**Talks through these doors (all via 00):**
- OUT → 04 Claimant Communication: Scheduling messages (`claimant.message.request`)
- OUT → 07 Vendor Coordination: Vendor presence needed (`vendor.request`)
- OUT → 08 / 13: Inspection outcome, verbatim findings attached (`inspection.result`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- IN ← 02 / 08: Inspection need + SLA band (`inspection.schedule`)
- IN ← 02 Claim Triage: Assignment context (`claim.assignment`)
- IN ← 04 Claimant Communication: Availability replies (`claimant.reply`)

## Agent 07 - Vendor Coordination Agent

**Type:** Vendor execution (mitigation, repair, rental, IA firms)

**Autonomy line:** Autonomous coordination with panel vendors under existing agreements; NEW vendors, rate changes, and scope increases are human-approved

Coordinates panel vendors on assigned claims: mitigation crews, rental cars,
contents storage, independent appraisal firms. Tracks assignment, ETA, progress, and
deliverables. Panel terms are fixed upstream; this agent never negotiates rates or
scope.

**Day-to-day duties:**
- Assign panel vendors per `vendor.request` with the claim scope attached exactly as issued.
- Track vendor ETA, arrival, progress milestones, and deliverable submission; report `vendor.status` on every milestone and every miss.
- Verify deliverables landed (photos uploaded, mitigation report filed) against the request - check the artifact, not the vendor's claim of completion.
- Route vendor scope-increase requests to the human with the vendor's stated justification verbatim - never approve, never pre-negotiate.
- Log all vendor interactions to 13.

**Talks through these doors (all via 00):**
- OUT → 02 / 08 / 13: Milestones, misses, deliverables (`vendor.status`)
- OUT → 04 Claimant Communication: Vendor appointment notices (`claimant.message.request`)
- OUT → 13 Claim File & Records: Every vendor interaction (`interaction.log`)
- IN ← 06 Inspection Scheduling / 08 Estimate & Valuation: Vendor need + scope (`vendor.request`)

## Agent 08 - Estimate & Valuation Data Agent

**Type:** Analysis assembly (estimates, valuations)

**Autonomy line:** Autonomous data assembly and calculation per approved methods; the NUMBER is a work product for the adjuster - never communicated outward, never a settlement position

Assembles estimate and valuation work products: repair estimate data, actual
cash value inputs, depreciation schedules per approved tables, total-loss thresholds,
comparable data. Every figure carries its method and source. The adjuster owns the
number's meaning; this agent owns its arithmetic and provenance.

**Day-to-day duties:**
- Assemble estimate packages from inspection results, vendor estimates, and pricing databases - each line item source-attributed.
- Apply approved depreciation and valuation tables exactly; a table gap is escalated, never bridged by judgment.
- Compute total-loss threshold comparisons per jurisdiction rules and flag threshold crossings to 02 as facts.
- Reconcile competing estimates (vendor vs. desk) into a variance report - report the variance, never pick the winner.
- Request supporting documents via 05 and policy figures via 03 as needed for the package.

**Talks through these doors (all via 00):**
- OUT → 07 Vendor Coordination: IA firm / specialty estimate engagement (`vendor.request`)
- OUT → 03 Policy Verification: Limits/deductible lookups (`policy.verify.request`)
- OUT → 02 / 11 / 13: Estimate package with methods and sources (`estimate.package`)
- OUT → 05 Document Collection: Missing support docs (`doc.request`)
- OUT → 06 Inspection Scheduling: Re-inspection need (`inspection.schedule`)
- OUT → 09 / 10: Valuation-stage observations (`fraud.signal`, `subro.signal`)
- OUT → 04 Claimant Communication: Doc-support message requests (`claimant.message.request`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- OUT → 10 / 13: Salvage value facts for recovery (`salvage.record`)
- IN ← 06 Inspection Scheduling: Inspection findings (`inspection.result`)
- IN ← 05 Document Collection: Receipts, invoices, proofs (`doc.received`)
- IN ← 07 Vendor Coordination: Vendor estimates as deliverables (`vendor.status`)
- IN ← 03 Policy Verification: Policy figures (`policy.verify.result`)
- IN ← 03: Policy change affecting valuation basis (`policy.change.notice`)

## Agent 09 - Fraud Signals Agent

**Type:** Pattern observation (SIU referral preparation)

**Autonomy line:** Autonomous indicator aggregation and referral-package preparation; the referral DECISION and every accusation are human (SIU) only

Aggregates fraud indicators observed across the swarm into per-claim signal
records, scores them against the owner-ratified indicator list, and prepares referral
packages for the human SIU decision. THE LINE, absolute: this swarm never accuses,
never confronts, never delays a claim on suspicion - it observes, aggregates, and
hands the package to a licensed human.

**Day-to-day duties:**
- Receive `fraud.signal` observations from all agents and maintain the per-claim signal record with source and verbatim basis for each.
- Score aggregated signals against the ratified indicator list only - no novel indicators without owner ratification.
- Prepare the SIU referral package (signals, sources, timeline) when the score crosses the ratified threshold, and route it `fraud.referral` to the human.
- Answer record requests from 13 for audit purposes.
- Never alter claim handling: signal aggregation is invisible to the claim's normal lifecycle - delay-on-suspicion is unfair claims practice.

**Talks through these doors (all via 00):**
- OUT → human (SIU) / 13: Referral package at threshold (`fraud.referral`)
- OUT → 13 Claim File & Records: Record ops (`record.request`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- IN ← 01/02/04/05/08: Indicator observations (`fraud.signal`)
- IN ← 13 Claim File & Records: Prior-claim patterns (`record.response`)
- IN ← human: Signed fraud disposition - a signal never dies quietly (`fraud.disposition`)

## Agent 10 - Subrogation Agent

**Type:** Recovery identification (subrogation preparation)

**Autonomy line:** Autonomous opportunity identification and demand-package assembly; pursuit, waiver, and negotiation decisions are human

Identifies recovery opportunities (third-party liability, product defect,
contractor negligence) from claim evidence, preserves the evidence trail, and
assembles demand packages for human pursuit decisions. It spots and prepares; humans
decide whether and how to pursue.

**Day-to-day duties:**
- Evaluate `subro.signal` observations against the recovery-opportunity checklist (identifiable third party, liability basis in evidence, economical recovery band).
- Issue evidence-preservation requests via 05 the moment an opportunity is identified - spoliation windows do not wait for pursuit decisions.
- Assemble the demand package: liability basis, damages support from 08's packages, evidence inventory - routed `subro.package` to the human.
- Track statute-of-limitation dates per jurisdiction and alert 12 style clocks via the package record.
- Answer audit record requests via 13.

**Talks through these doors (all via 00):**
- OUT → 05 Document Collection: Evidence preservation requests (`doc.request`)
- OUT → human / 13: Demand package for pursuit decision (`subro.package`)
- OUT → 13 Claim File & Records: Record ops + ambient logging (`record.request`, `interaction.log`)
- IN ← 02/05/08: Recovery indicators (`subro.signal`)
- IN ← 13 Claim File & Records: Record responses (`record.response`)
- IN ← human: Signed recovery authority - demands and acceptances are human money decisions (`recovery.authority`)
- IN ← 08 / 11: Salvage facts feeding recovery (`salvage.record`)

## Agent 11 - Payments & Reserves Records Agent

**Type:** Financial records (payments, reserves)

**Autonomy line:** RECORDS ONLY - every payment issuance and reserve change executes solely on a signed human `payment.authority` envelope; this agent moves no money on its own initiative, ever

Maintains the claim's financial record: payment issuance records, reserve
levels, deductible application, coinsurance math per approved formulas. Execution is
authority-gated: a signed human envelope is the only thing that moves money or
changes a reserve. Unsigned = integrity violation, not a judgment call.

**Day-to-day duties:**
- Execute payment issuance and reserve changes ONLY on signed `payment.authority` envelopes; record execution with the authority envelope_id attached.
- Record deductible application and coinsurance calculations per approved formulas, source-attributed to the estimate package.
- Report `payment.record` and `reserve.record` to 12 and 13 on every execution.
- Flag payment anomalies (duplicate payee, changed banking details mid-claim) to the human before execution even when authority is signed - a signed envelope with an anomaly is held, named, and re-confirmed.
- Answer financial-audit record requests via 13.

**Talks through these doors (all via 00):**
- OUT → 12 / 13: Payment execution record (`payment.record`)
- OUT → 12 / 13: Reserve change record (`reserve.record`)
- OUT → 04 Claimant Communication: Payment-issued notice (approved template) (`claimant.message.request`)
- OUT → 13 Claim File & Records: Ambient logging (`interaction.log`)
- OUT → human / 13: Books variance - $0.00 tolerance, human notified (`reconciliation.exception`)
- OUT → 10 / 13: Salvage proceeds posted (`salvage.record`)
- IN ← human: Signed authority to pay / change reserve (`payment.authority`)
- IN ← 08 Estimate & Valuation: Estimate package (records basis) (`estimate.package`)
- IN ← human: Signed reserve authority - reserve changes are money (`reserve.authority`)

## Agent 12 - Compliance & Regulatory Deadlines Agent

**Type:** Regulatory engine (fair claims handling, DOI)

**Autonomy line:** Autonomous clock tracking and alerting; regulatory responses and any external filing are human-signed

Runs the regulatory clock engine: acknowledgment deadlines, proof-of-loss
response windows, decision deadlines, and jurisdiction-specific fair-claims-handling
rules per claim. Prepares DOI inquiry response packages for human signature. A missed
statutory clock is never silent - escalation fires at the ratified risk threshold,
before the miss.

**Day-to-day duties:**
- Instantiate the jurisdiction clock set on every `claim.assignment` and track each clock against claim events from 13's records.
- Fire `deadline.alert` to 02/04/14 at the ratified lead-times; fire `compliance.hold` to 00 when an action would violate a fair-claims rule.
- Receive `doi.inquiry` routing and assemble the response package (claim chronology from the audit record, verbatim communications) - `doi.response.package` to the human for signature.
- Maintain the jurisdiction rule table per owner-ratified updates only.
- Request documents supporting regulatory responses via 05.

**Talks through these doors (all via 00):**
- OUT → 02 / 04 / 14: Clock alerts at lead-time (`deadline.alert`)
- OUT → hold queue (via 00): Fair-claims rule conflict (`compliance.hold`)
- OUT → human / 13: DOI response package for signature (`doi.response.package`)
- OUT → 05 Document Collection: Response support docs (`doc.request`)
- OUT → 04 Claimant Communication: Statutorily required notices (approved templates) (`claimant.message.request`)
- OUT → 13 Claim File & Records: Record ops + ambient logging (`record.request`, `interaction.log`)
- IN ← 02 Claim Triage: Claim opened (clock instantiation) (`claim.assignment`)
- IN ← 01 / 04: DOI contact reported (`doi.inquiry`)
- IN ← 11 Payments & Reserves: Financial event records (clock-relevant) (`payment.record`, `reserve.record`)
- IN ← 13 Claim File & Records: Chronology records (`record.response`)
- IN ← 01 / 04 / 05: Representation notice - clock and practice implications (`representation.notice`)
- IN ← 03: Policy change - clock implications re-checked (`policy.change.notice`)
- IN ← 13: Records disclosure pending - response clock armed (`records.disclosure.package`)

## Agent 13 - Claim File & Records Agent

**Type:** System of record (claim file, audit)

**Autonomy line:** Autonomous record keeping; the record is append-only - corrections are new entries that reference what they correct, never edits

The claim file: system-of-record updates, the append-only audit trail, record
lookups, and retention rules. Every agent's interactions land here. A record request
is answered from the record - never from inference about what the record probably
says.

**Day-to-day duties:**
- Ingest `interaction.log` from all agents and maintain the per-claim append-only file.
- Answer `record.request` with `record.response` - record contents verbatim with entry timestamps; absent records are reported absent.
- Apply retention and privacy rules (GLBA; medical material sealed to the human lane per 05's custody flags).
- Maintain claim chronologies consumable by 12's regulatory packages and 14's books.
- Register corrections as new entries referencing the corrected entry_id - the original never changes.

**Talks through these doors (all via 00):**
- OUT → 01/02/09/10/12/14: Record contents verbatim (`record.response`)
- OUT → human / 12: Disclosure inventory (existence/type/date/source only) for human release (`records.disclosure.package`)
- IN ← all agents: Interaction records (`interaction.log`)
- IN ← 01/02/09/10/12/14: Record lookups (`record.request`)
- IN ← 02 Claim Triage: Assignment + closure artifacts (`claim.assignment`, `closure.package`)
- IN ← 03 Policy Verification: Verification facts (`policy.verify.result`)
- IN ← 05 Document Collection: Document inventory (`doc.received`)
- IN ← 06 Inspection Scheduling: Inspection outcomes (`inspection.result`)
- IN ← 07 Vendor Coordination: Vendor milestones (`vendor.status`)
- IN ← 08 Estimate & Valuation: Estimate packages (`estimate.package`)
- IN ← 09 / 10: Referral and demand packages (audit copies) (`fraud.referral`, `subro.package`)
- IN ← 11 Payments & Reserves: Financial records (`payment.record`, `reserve.record`)
- IN ← 12 Compliance & Deadlines: Regulatory response packages (audit copies) (`doi.response.package`)
- IN ← 01 / 04 / 05: Representation notice on the claim file (`representation.notice`)
- IN ← 03: Policy change on the claim file (`policy.change.notice`)
- IN ← 08 / 11: Salvage records (file copy) (`salvage.record`)
- IN ← 11: Reconciliation exceptions (books copy) (`reconciliation.exception`)

## Agent 14 - Daily Operations Agent

**Type:** Operations cadence (morning book, EOD books, surge)

**Autonomy line:** Autonomous book assembly and presentation; the human reads the book and directs - the book never self-executes its own recommendations

Runs the operational cadence: the morning book (overnight FNOLs, today's
clocks, inspection schedule, aging claims), the end-of-day books (what moved, what
missed, tomorrow's exposures, missed-item sweep), and CAT surge coordination support.
Books are assembled from 13's records and 12's clocks - never from memory.

**Day-to-day duties:**
- Assemble the morning book: overnight intake, today's deadline alerts, inspection calendar, aging-claim exceptions - presented `report.package` to the human before the day starts.
- Assemble the EOD books: every claim touched, every clock advanced or missed, the missed-item sweep against the morning book - gaps NAMED, never silently thinner.
- Receive and rebroadcast CAT declarations (`cat.event`) to 02 with the surge rule set attached.
- Pull chronologies and exception lists from 13; pull live clock states from 12's alerts.
- Log its own assembly runs to 13.

**Talks through these doors (all via 00):**
- OUT → human: Morning book / EOD books (`report.package`)
- OUT → 02 Claim Triage: CAT surge rebroadcast (`cat.event`)
- OUT → 13 Claim File & Records: Record pulls + ambient logging (`record.request`, `interaction.log`)
- IN ← 12 Compliance & Deadlines: Clock alerts feeding the books (`deadline.alert`)
- IN ← 13 Claim File & Records: Chronologies, exceptions (`record.response`)
- IN ← any: Wait-state visibility - waits reported past threshold (`agent.status`)
