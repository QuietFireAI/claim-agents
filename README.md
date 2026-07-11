# claim-agents - insurance claims vertical for the DispatcherAgents runtime

An **identity side-load**: everything vertical-specific for a 15-agent
property & casualty claims swarm, loadable into the content-neutral
[dispatcher-agents](https://github.com/QuietFireAI/dispatcher-agents) runtime.
The runtime never contains vertical text; this repo never contains transport
code. That split is the architecture.

**Status: v0.1 ratified 2026-07-11 - owner sign-off. Not runtime-hardened. No
licensed legal, regulatory, or insurance-practice review has been performed.**

## What this is for

Operations support for a licensed adjuster or claims desk: part intake
machine, part records engine, part clock-watcher. The swarm captures FNOLs,
verifies policy facts, schedules inspections, chases documents, coordinates
panel vendors, assembles estimate arithmetic, aggregates fraud signals,
prepares subrogation and regulatory packages, keeps the append-only claim
file, and delivers the morning and end-of-day books.

What it never does - the five absolute lines (identity/IDENTITY-insurance-claim-agent.md):

1. No coverage statement, ever - coverage is a licensed determination.
2. No unsigned money - payments and reserves move only on a signed human
   `payment.authority` envelope.
3. No accusation, no delay-on-suspicion - fraud signals aggregate silently
   for a human SIU decision; claim handling never changes on suspicion.
4. No regulator contact from the swarm - DOI packages are signature-ready
   work product; the human signs and files.
5. Represented claimants are human-only - attorney notice halts direct
   contact pending human direction.

## Layout

| Path | What it is |
|---|---|
| `identity/routes.json` | The closed track: 35 (intent, senders, receivers) routes - single source of truth |
| `identity/priority.json` | JIT playbook priority classes (ratified 2026-07-11) |
| `identity/IDENTITY-insurance-claim-agent.md` | The identity declaration |
| `00-dispatcher/ ... 14-daily-operations/` | 15 agent SKILL.md + DECISIONS.md (tuple layer) |
| `playbooks/P01 ... P10` | Deployment playbooks: FNOL front door through EOD books |
| `SWARM.md` | Framework manifest + swarm-level tuples |
| `MANNERS.md` | Conduct constants, hash-registered at boot attestation |
| `TUPLE_INDEX.md` | Generated drill-down: tuple → agent → playbooks |
| `generate_skills.py` / `gen_meta.py` / `gen_playbooks.py` / `gen_tuple_index.py` | Generators - data tables are the spec; files are build artifacts |
| `verify_swarm.py` | Enforcement: tuple legality, edge completeness, regression - exit 0 = clean |

## Verify

```bash
python3 verify_swarm.py    # 0 failures, 0 warnings expected
```

## Load into the runtime

```bash
git clone https://github.com/QuietFireAI/dispatcher-agents.git
git clone https://github.com/QuietFireAI/claim-agents.git
cd dispatcher-agents && pip install -e ".[pillars,crypto,dev]"
IDENTITY_DIR=../claim-agents python -m pytest tests/
```

The loader is fail-closed: no routes.json, no track, no load. It audits the
priority table's status on every load - never silently.

## Sibling identities

- [listing-agents](https://github.com/QuietFireAI/listing-agents) - real-estate listing vertical (ratified)
- reservation-agents - park/resort reservations vertical

## License

Proprietary - see LICENSE (placeholder pending legal review).
