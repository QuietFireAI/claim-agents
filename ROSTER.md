# DispatcherAgents Claim Swarm - Roster v0.1 (ratified 2026-07-11 - owner sign-off)

15 agents, hub-and-spoke via 00. All inter-agent communication is a logged
envelope through the Dispatcher; the route-space is closed (identity/routes.json).

| # | Agent | Type | Autonomy boundary |
|---|---|---|---|
| 00 | Dispatcher | Hub (transport, gates, audit) | Validates every (from, intent, to) tuple; holds ambiguity; owns the audit log |
| 01 | FNOL Intake Agent | Intake (first notice of loss) | Autonomous capture and acknowledgment; NEVER states coverage, fault, or claim value |
| 02 | Claim Triage & Severity Agent | Coordination (severity, assignment, lifecycle) | Autonomous severity scoring and routing recommendation; assignment executes on human-confirmed rules; NEVER determines coverage |
| 03 | Policy Verification Agent | Systems lookup (policy data) | Autonomous data lookup and factual reporting; verification is NOT coverage determination - it reports what the policy record says, never what it means for this loss |
| 04 | Claimant Communication Agent | Communication hub (claimant/insured-facing) | Autonomous sends from adjuster-approved templates; ANY off-template or coverage-adjacent message requires human approval before send |
| 05 | Document Collection Agent | Evidence pipeline (claim documents) | Autonomous request, receipt, inventory, and chase per playbook cadence; authenticity judgments are human |
| 06 | Inspection & Appraisal Scheduling Agent | Scheduling execution (inspections, appraisals) | Autonomous scheduling within adjuster availability rules; access commitments follow the insured's stated constraints, never pressure |
| 07 | Vendor Coordination Agent | Vendor execution (mitigation, repair, rental, IA firms) | Autonomous coordination with panel vendors under existing agreements; NEW vendors, rate changes, and scope increases are human-approved |
| 08 | Estimate & Valuation Data Agent | Analysis assembly (estimates, valuations) | Autonomous data assembly and calculation per approved methods; the NUMBER is a work product for the adjuster - never communicated outward, never a settlement position |
| 09 | Fraud Signals Agent | Pattern observation (SIU referral preparation) | Autonomous indicator aggregation and referral-package preparation; the referral DECISION and every accusation are human (SIU) only |
| 10 | Subrogation Agent | Recovery identification (subrogation preparation) | Autonomous opportunity identification and demand-package assembly; pursuit, waiver, and negotiation decisions are human |
| 11 | Payments & Reserves Records Agent | Financial records (payments, reserves) | RECORDS ONLY - every payment issuance and reserve change executes solely on a signed human `payment.authority` envelope; this agent moves no money on its own initiative, ever |
| 12 | Compliance & Regulatory Deadlines Agent | Regulatory engine (fair claims handling, DOI) | Autonomous clock tracking and alerting; regulatory responses and any external filing are human-signed |
| 13 | Claim File & Records Agent | System of record (claim file, audit) | Autonomous record keeping; the record is append-only - corrections are new entries that reference what they correct, never edits |
| 14 | Daily Operations Agent | Operations cadence (morning book, EOD books, surge) | Autonomous book assembly and presentation; the human reads the book and directs - the book never self-executes its own recommendations |

Human lanes (never automated): coverage determination, settlement and
negotiation, fraud referral decisions and any accusation, payments and
reserves (signed authority only), regulatory filings, represented-claimant
contact, medical-record content, claim closure.
