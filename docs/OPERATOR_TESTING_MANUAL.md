# Operator Testing Manual - Insurance Claim Swarm

A filmable, step-by-step script. Every step states what you type, what
you must see, and what it proves. No step asks you to trust a claim the
screen doesn't show. Written for a claims professional to run cold.

## Setup (once)

```
git clone https://github.com/QuietFireAI/claim-agents.git
cd claim-agents
pip install -r requirements.txt
```
**You must see:** pip finish without errors.
**Proves:** the bare-clone guarantee - no hidden environment.

## Test 1 - The whole suite

```
python -m pytest tests_claim/ -v
```
**You must see:** `17 passed`, including tests named for every playbook
P01-P14 and for the absolute lines (coverage statement blocked, unsigned
money rejected, representation halt from all three detectors, silent
fraud aggregation with signed ending, $0.00 tolerance, closed track).
**Proves:** the claims in the docs are executable, not aspirational.

## Test 2 - Watch one claim end to end

```
python3 tools/run_demo.py
```
**You must see, in order:**
1. ACT 1: assignment, `policy: in_force` labelled as a fact, inspection
   dispatched to the ratified panel vendor
2. ACT 2: sourced estimate; salvage $1,500 landing in the recovery lane
3. ACT 3: `channel halted: True` the same turn the attorney letter
   arrives; a status update `HELD, visible as a wait`; the claimant
   writing in anyway and `answered by swarm: False`
4. ACT 4: unsigned fraud disposition `ok=False`; the signed one
   `recorded: 'cleared'`; the referral carrying
   `handling_changed: False` on the record
5. ACT 5: unsigned $5,000 payment `ok=False, paid=0.0`; the signed
   payment posting at 4,999.99 and a ONE-CENT variance raising
   `reconciliation.exception`; a "you are covered" message attempt
   producing `integrity.violation` and `sent: nothing`
6. ACT 6: `verify_chain(): ok=True`, `dead letters: 0`
**Proves:** the five absolute lines under real hub traffic.

## Test 3 - Try to break the money lane (adversarial)

Open a Python shell in the repo root and paste:
```python
import sys; sys.path.insert(0, ".")
from tests_claim.test_playbooks_e2e_all import build_swarm
from dispatcher.core import Envelope
hub, signer, spokes, _ = build_swarm("/tmp/adv")
env = Envelope(from_agent="human", to_agent="11",
               intent="reserve.authority", client_context_id="adv-1",
               payload={"amount": 250000.0},
               provenance={"source": "human", "captured_at": "runtime",
                           "verbatim_available": True})
print(hub.send(env))
print(spokes["11"].ledger.get("adv-1"))
```
**You must see:** a rejection, and no reserve on the ledger - a forged
quarter-million-dollar reserve change going nowhere.
**Proves:** a claimed approver name is not a credential; the Ed25519
signature is. Reserves are money (line 2).

## Test 4 - Tamper with the log

```
python3 tools/run_demo.py            # note the log file path it prints
# edit any middle line of that .jsonl - change one character - then:
python3 - <<'PY'
from dispatcher.core import AuditLog
print(AuditLog("PASTE_THE_PATH_HERE").verify_chain())
PY
```
**You must see:** `ok: False` with the violation named by line number.
**Proves:** the audit file is the single source of truth because it is
tamper-EVIDENT, not tamper-proof-by-promise.

## Test 5 - The closed track

```
python -m pytest tests_claim/ -k closed_track -v
```
**You must see:** agent 09 (fraud signals) attempting to send
`payment.record` - a lane it does not own - and being rejected.
**Proves:** no agent can improvise a lane; in particular the fraud
agent structurally CANNOT touch money or handling. The track is the law.

## What to challenge next (for the skeptical reviewer)

- Ask where fair-claims state deadlines live -> statutory, per state,
  deployment content in the carrier rule table; the conservatism rule
  (earlier date wins) governs derivations.
- Ask about coverage analysis -> not here, on purpose; the closure
  package's coverage-statement field is hardcoded None.
- Ask who signed the signer registry -> a fictional test persona,
  declared in authority_signers.json itself; production replaces it
  (login TBA, owner decision C5 2026-07-18).
Nothing above is hidden. The gaps are in writing next to the strengths.
