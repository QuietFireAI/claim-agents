# Start Here - 60 Seconds

**What this is:** a 14-agent P&C insurance-claim swarm on a closed track.
One hub routes everything; only pre-approved (sender, intent, receiver)
tuples are legal; every action lands on a hash-chained, tamper-evident
audit log.

**What it does:** FNOL intake, triage/assignment, policy facts,
claimant communication, documents, inspections, vendor dispatch,
sourced estimates, fraud-signal aggregation, subrogation preparation,
payments and reserves, fair-claims clocks and DOI responses, the claim
file, and the daily books - across 14 playbooks P01-P14.

**What it never does:** state coverage, move unsigned money (payments,
reserves, recovery), change handling on suspicion, let a clock or a
fraud signal die quietly, or contact a represented claimant. Each line
is enforced in code and proven by a test.

**See it work (2 minutes):**
```
git clone https://github.com/QuietFireAI/claim-agents.git
cd claim-agents && pip install -r requirements.txt
python3 tools/run_demo.py        # one claim, six acts, real hub
python -m pytest tests_claim/    # every playbook, every gate
```

**Read next:** WHAT_SUCCESS_MEANS.md -> PLAY-BY-PLAY.md ->
JOB_DESCRIPTIONS.md -> OPERATOR_TESTING_MANUAL.md -> TUNING_MANUAL.md.
