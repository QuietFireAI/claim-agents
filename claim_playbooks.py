# claim-agents playbooks P01-P10. Spliced with listing's gen_playbooks framework.
PB = [
 dict(num="P01", slug="fnol-to-assignment", name="FNOL to Assignment",
  desc="Swarm deployment: reported loss to verified, assigned, clock-instantiated claim. Agents 01, 02, 03, 12, 13. The speed-to-FNOL front door - acknowledgment and assignment SLAs run from first contact.",
  trigger="`claim.fnol` package lands at 02, any channel, any hour.",
  pre=["FNOL package carries provenance per field; unknowns marked unknown (01's capture rule).",
       "Assignment matrix and severity rubric are the owner-ratified versions on file."],
  phases=[
   ("Phase 1 - Verify and score (parallel)", [
    ("1","02","Score severity per ratified rubric; worst-case band on missing inputs, gap named","`policy.verify.request` → 03","score + gap list on the claim record"),
    ("2","03","Verify policy status/limits/endorsements on date of loss from live systems","`policy.verify.result` → 02, 13","result with system timestamps"),
    ("3","12","Instantiate jurisdiction clock set from assignment context","(internal; alerts arm)","clock set on record with lead-times"),
   ]),
   ("Phase 2 - Assign (gated on Phase 1)", [
    ("4","02","Assign per matrix; out-of-matrix combinations go to human queue","`claim.assignment` → 06, 12, 13","assignment envelope acked; lapse/mismatch facts routed to human if present"),
    ("5","02","Open document checklist for the line of business","`doc.request` → 05","checklist issued and logged"),
    ("6","02","Acknowledgment to claimant per statutory template","`claimant.message.request` → 04","send logged with disclosure set"),
   ]),
  ],
  gates=["Phase 2 does not start on an unverified policy - 'not found' holds in intake-verified state (02 tuple).",
         "Injury/fatality flags route the human notification inside the acknowledgment SLA, not after it."]),

 dict(num="P02", slug="property-claim-lifecycle", name="Property Claim Lifecycle",
  desc="Swarm deployment: assigned property claim through docs, inspection, estimate, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 12, 13. The human decides coverage and closure; the swarm keeps every gate visible.",
  trigger="`claim.assignment` with line of business = property.",
  pre=["P01 completed: verified policy, clocks live, checklist issued."],
  phases=[
   ("Phase 1 - Evidence (parallel)", [
    ("1","05","Collect checklist docs; chase on cadence; anomalies to 09 as observations","`doc.received` → 02, 08, 13","item-level inventory current"),
    ("2","06","Schedule inspection inside the severity SLA window; confirm access","`inspection.schedule` fulfilled; result → 08, 13","inspection result with verbatim findings"),
    ("3","07","Coordinate mitigation vendors as requested; verify deliverables landed","`vendor.status` → 02, 08, 13","artifact-verified milestones"),
   ]),
   ("Phase 2 - Valuation (gated on inspection + docs)", [
    ("4","08","Assemble estimate package, sources attached; variance report if estimates diverge","`estimate.package` → 02, 11, 13","package with methods, sources, variances"),
   ]),
   ("Phase 3 - Human decision support", [
    ("5","02","Assemble closure package when all gates green; amber gates named","`closure.package` → human, 13","package delivered; human decision logged by 13"),
    ("6","11","Execute payments/reserves ONLY on signed authority; records to 12/13","`payment.record`, `reserve.record`","records carry authority envelope_id"),
    ("7","04","Status updates on the playbook cadence throughout","`claimant.message.send`","every send logged verbatim"),
   ]),
  ],
  gates=["No figure leaves the swarm: 08's numbers are adjuster work product only.",
         "Payment execution without signed `payment.authority` is an integrity violation, not an error."]),

 dict(num="P03", slug="auto-claim-lifecycle", name="Auto Claim Lifecycle",
  desc="Swarm deployment: assigned auto claim through appraisal, valuation, rental coordination, to closure package. Agents 02, 04, 05, 06, 07, 08, 11, 13. Total-loss threshold checks fire as facts to the adjuster.",
  trigger="`claim.assignment` with line of business = auto.",
  pre=["P01 completed; listed-vehicle/driver facts from 03 attached to the assignment."],
  phases=[
   ("Phase 1 - Evidence (parallel)", [
    ("1","05","Collect photos, police report, repair estimates per auto checklist","`doc.received` → 02, 08, 13","inventory current; police-report fault facts also fire `subro.signal`"),
    ("2","06","Schedule appraisal (field or desk per severity band)","`inspection.result` → 08, 13","appraisal findings verbatim"),
    ("3","07","Rental coordination within policy terms from 03's verified limits","`vendor.status` → 02, 13","rental record with term basis attached"),
   ]),
   ("Phase 2 - Valuation", [
    ("4","08","Estimate package; run total-loss threshold per jurisdiction; within-margin reported as within-margin","`estimate.package` → 02, 11, 13","package with threshold comparison as fact"),
   ]),
   ("Phase 3 - Human decision support", [
    ("5","02","Closure package with all gates stated","`closure.package` → human, 13","human decision logged"),
    ("6","11","Authority-gated payment/reserve records","`payment.record` → 12, 13","authority envelope_id attached"),
   ]),
  ],
  gates=["Unlisted-driver or unlisted-vehicle facts route to the human as facts (03's rule) - the lifecycle continues unless the human holds it.",
         "Total-loss crossing triggers P04 on human direction, never automatically."]),

 dict(num="P04", slug="total-loss-handling", name="Total Loss Handling",
  desc="Swarm deployment: human-declared total loss through valuation support, title docs, and settlement records. Agents 02, 04, 05, 08, 11, 13. Every settlement conversation is human; the swarm handles paper and records.",
  trigger="Human declares total loss on a claim (signed direction referencing 08's threshold fact).",
  pre=["Human total-loss declaration on file; P02/P03 evidence base current."],
  phases=[
   ("Phase 1 - Valuation support", [
    ("1","08","Assemble ACV package: comparables, approved-table depreciation, jurisdiction fees/taxes - all sourced","`estimate.package` → 02, 11, 13","ACV package; adjuster owns the number's use"),
    ("2","05","Request title, lienholder, and odometer documents per total-loss checklist","`doc.received` → 02, 13","title docs inventoried; lienholder named"),
   ]),
   ("Phase 2 - Human settlement (swarm supports records only)", [
    ("3","04","Send human-approved settlement communications; NOTHING off-template","`claimant.message.send`","sends logged; any claimant counter routes verbatim to human"),
    ("4","11","Execute settlement payment on signed authority; lienholder split per authority terms","`payment.record` → 12, 13","records carry the authority and the split"),
    ("5","02","Closure package post-payment with salvage/title status stated","`closure.package` → human, 13","human closes; 13 logs"),
   ]),
  ],
  gates=["Negotiation is human end to end - a claimant counter-offer never gets a swarm response beyond the routing acknowledgment template.",
         "Lienholder payoff figures come from documents on file, never from phone summaries."]),

 dict(num="P05", slug="fraud-referral", name="Fraud Referral",
  desc="Swarm deployment: threshold-crossing signal record to SIU referral package. Agents 09, 13, plus contributing observers. The claim's normal lifecycle NEVER changes - delay-on-suspicion is the named illegal move.",
  trigger="09's aggregated signal score crosses the owner-ratified threshold on a claim.",
  pre=["Every contributing signal carries source and verbatim basis (09's intake rule)."],
  phases=[
   ("Phase 1 - Package (silent to the lifecycle)", [
    ("1","09","Assemble referral package: signals, sources, timeline from 13's chronology","`record.request` → 13","chronology attached"),
    ("2","09","Route the package to the human SIU decision-maker","`fraud.referral` → human, 13","referral logged; decision is human"),
   ]),
   ("Phase 2 - Human decision (swarm posture unchanged)", [
    ("3","13","Register the SIU decision as a record entry when the human supplies it","(record entry)","decision on file; handling changes only on explicit human direction"),
   ]),
  ],
  gates=["No agent's behavior on the claim changes at referral - schedules, payments-on-authority, and communications continue exactly per playbook.",
         "The referral's existence is need-to-know sealed (09's tuple); no cross-agent disclosure."]),

 dict(num="P06", slug="subrogation-handoff", name="Subrogation Handoff",
  desc="Swarm deployment: recovery signal to preserved evidence and demand package for human pursuit. Agents 10, 05, 08, 13. Preservation fires immediately; the pursuit decision waits for no artifact.",
  trigger="`subro.signal` matching the recovery-opportunity checklist at 10.",
  pre=["Signal carries the liability-basis evidence pointer (police report, inspection finding, vendor observation)."],
  phases=[
   ("Phase 1 - Preserve (immediate)", [
    ("1","10","Issue evidence-preservation requests the moment the opportunity is identified","`doc.request` → 05","preservation requests logged with spoliation-window basis"),
    ("2","05","Execute preservation: custody flags on physical-evidence pointers, retention holds via 13","`doc.received` → 02, 08, 13","custody status inventoried"),
   ]),
   ("Phase 2 - Package", [
    ("3","10","Assemble demand package: liability basis, damages support from 08, evidence inventory, statute dates (shortest theory governs)","`subro.package` → human, 13","package delivered; pursuit decision is human"),
   ]),
  ],
  gates=["Habitability/repair urgency versus preservation conflicts escalate immediately (10's tuple) - neither clock is silently sacrificed.",
         "No contact with the third party or their carrier originates from the swarm."]),

 dict(num="P07", slug="payment-and-closure-records", name="Payment & Closure Records",
  desc="Swarm deployment: signed authority to executed, reconciled, compliance-visible financial records and the closure package. Agents 11, 12, 02, 13. Records only - authority moves money, the swarm moves paper.",
  trigger="Signed `payment.authority` envelope arrives at 11, or 02 determines all closure gates green.",
  pre=["Authority references a current estimate version; payee details match the record (11's hold tuples otherwise)."],
  phases=[
   ("Phase 1 - Execute on authority", [
    ("1","11","Verify authority signature context, estimate version, payee details; execute; anomalies hold + re-confirm","`payment.record` → 12, 13","record with authority envelope_id"),
    ("2","12","Register the financial event against the claim's clocks","(clock update)","clock state current"),
   ]),
   ("Phase 2 - Closure package", [
    ("3","02","Assemble closure package: docs complete, estimate final, payments reconciled, clocks satisfied - ambers named","`closure.package` → human, 13","package delivered; the human closes"),
    ("4","04","Send closure communications on the approved template after the human's closure decision","`claimant.message.send`","send logged with the human decision reference"),
   ]),
  ],
  gates=["An amber gate in the closure package is presented amber - 02's no-rounding tuple.",
         "Deductible/coinsurance math carries its formula and source line in the record."]),

 dict(num="P08", slug="doi-inquiry-response", name="DOI Inquiry Response",
  desc="Swarm deployment: regulator inquiry to a signature-ready response package inside the statutory window. Agents 12, 13, 05, 04. The human signs everything that leaves; the swarm's job is a complete package early.",
  trigger="`doi.inquiry` routed to 12 from any intake point (01 at FNOL, 04 from a reply, human forward).",
  pre=["The inquiry document itself is on file verbatim; the response clock is instantiated from the regulator's date, conservatism rule applied."],
  phases=[
   ("Phase 1 - Assemble (clock-led)", [
    ("1","12","Instantiate the response clock; alert at ratified lead-times","`deadline.alert` → 02, 04, 14","clock live, alerts armed"),
    ("2","12","Pull the claim chronology and verbatim communications from the record","`record.request` → 13","chronology attached to the package"),
    ("3","05","Collect any response-supporting documents not already on file","`doc.received` → 02, 13 (support set)","support docs inventoried"),
   ]),
   ("Phase 2 - Human signature", [
    ("4","12","Deliver the signature-ready package; a certain shortfall is delivered early with the gap named","`doi.response.package` → human, 13","package delivered inside lead-time; human signs and files"),
   ]),
  ],
  gates=["Nothing goes to a regulator from the swarm - human signature always (12's legal line).",
         "Claimant communications pause on this claim only if the human directs; an inquiry is not a hold."]),

 dict(num="P09", slug="morning-operations", name="Morning Operations",
  desc="Swarm deployment: the claims desk's morning book. Overnight FNOLs, today's clocks, the inspection calendar, aging exceptions - assembled from records and presented for human review before the day starts. Agents 14, 13, 12.",
  trigger="Scheduled daily start (owner-configured time) or owner command.",
  pre=["EOD books from the previous day exist (P10 completion on the log); if absent, the book runs with the gap NAMED, never silently thinner."],
  phases=[
   ("Assemble (parallel, all to human review)", [
    ("1","14","Pull overnight intake and lifecycle exceptions from the record","`record.request` → 13","overnight section sourced"),
    ("2","14","Pull today's clock alerts and lead-time exposures","(from 12's `deadline.alert` stream)","clock section current with lead-times"),
    ("3","14","Assemble the inspection calendar and aging-claim exceptions","(from record pulls)","calendar + exceptions sections sourced"),
   ]),
   ("Present", [
    ("4","14","Deliver the morning book; sections with unavailable sources marked absent","`report.package` → human","book delivered; the human directs, the book never self-executes"),
   ]),
  ],
  gates=["A source unavailable at assembly time is a named absence - never yesterday's numbers backfilled (14's tuple)."]),

 dict(num="P10", slug="end-of-day-books", name="End-of-Day Books",
  desc="Swarm deployment: the closing books. Every claim touched, every clock advanced or missed, the missed-item sweep against the morning book. Agents 14, 13, 12. Gaps named; a clean-looking book with hidden gaps is the named failure.",
  trigger="Scheduled day end (owner-configured time) or owner command.",
  pre=["The morning book (P09) exists as the sweep baseline; if absent, the sweep names that first."],
  phases=[
   ("Assemble", [
    ("1","14","Pull the day's full activity chronology","`record.request` → 13","activity section sourced with timestamps"),
    ("2","14","Reconcile clocks: advanced, satisfied, at-risk, missed - misses quantified","(from 12's alert stream + records)","clock reconciliation complete"),
    ("3","14","Missed-item sweep: every morning-book item without a day touch, named with its owner","(sweep vs. P09 baseline)","sweep list complete; no silent reassignment"),
   ]),
   ("Present", [
    ("4","14","Deliver the EOD books","`report.package` → human","books delivered and logged; P10 completion event on the log for tomorrow's P09"),
   ]),
  ],
  gates=["The sweep never reassigns - it names (14's tuple). Reassignment is the human's morning decision."]),
]
