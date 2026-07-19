#!/usr/bin/env python3
"""Generate docs/JOB_DESCRIPTIONS.md, docs/PLAYBOOKS.md, docs/PLAY-BY-PLAY.md
from the single-source data files (AGENTS, PB). Never hand-edit the outputs -
regenerate here. Mirrors the listing-agents doc set."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
from claim_data import AGENTS, ROUTES
from claim_playbooks import PB
from gen_playbooks import CA
for _p in PB:
    if _p["num"] in CA and "completion" not in _p:
        _p["completion"], _p["abort"] = CA[_p["num"]]

DOCS = os.path.join(HERE, "docs")
os.makedirs(DOCS, exist_ok=True)

# ------------------------------------------------------ JOB_DESCRIPTIONS
out = ["# Job Descriptions - Insurance Claim Swarm",
       "",
       "One entry per agent: what it does all day, what it never does, and",
       "the doors it talks through. GENERATED from claim_data.py -",
       "regenerate with gen_docs.py, never hand-edit.",
       ""]
out += ["## Agent 00 - Dispatcher",
        "",
        "The hub. Validates every (from, intent, to) tuple against the",
        "closed track (identity/routes.json), verifies signatures on every",
        "authority intent, holds ambiguity in the clarification queue, and",
        "owns the hash-chained audit log. Nothing moves without it; nothing",
        "it moves is unrecorded.", ""]
for a in AGENTS:
    out.append(f"## Agent {a['num']} - {a['name']}")
    out.append("")
    out.append(f"**Type:** {a['type']}")
    out.append("")
    out.append(f"**Autonomy line:** {a['autonomy']}")
    out.append("")
    out.append(a["role"].strip())
    out.append("")
    out.append("**Day-to-day duties:**")
    for j in a["jobs"]:
        out.append(f"- {j}")
    out.append("")
    ins = [e for e in a["edges"] if e[0] == "IN"]
    outs = [e for e in a["edges"] if e[0] == "OUT"]
    out.append("**Talks through these doors (all via 00):**")
    for d, arrow, purpose, intent in outs:
        out.append(f"- OUT {arrow}: {purpose} ({intent})")
    for d, arrow, purpose, intent in ins:
        out.append(f"- IN {arrow}: {purpose} ({intent})")
    out.append("")
open(os.path.join(DOCS, "JOB_DESCRIPTIONS.md"), "w").write("\n".join(out))
print("JOB_DESCRIPTIONS.md:", len(AGENTS), "agents")

# ------------------------------------------------------ PLAYBOOKS (consolidated)
out = ["# Playbooks P01-P14 - Insurance Claim Swarm",
       "",
       "The consolidated catalog. Full per-playbook SKILL.md files live in",
       "playbooks/. GENERATED from claim_playbooks.py.", ""]
for p in PB:
    out.append(f"## {p['num']} - {p['name']}")
    out.append("")
    out.append(p["desc"])
    out.append("")
    out.append(f"**Trigger:** {p['trigger']}")
    out.append("")
    out.append("**HITL gates (hard stops):**")
    for g in p["gates"]:
        out.append(f"- {g}")
    out.append("")
    out.append(f"**Done means:** {p['completion']}")
    out.append("")
open(os.path.join(DOCS, "PLAYBOOKS.md"), "w").write("\n".join(out))
print("PLAYBOOKS.md:", len(PB), "playbooks")

# ------------------------------------------------------ PLAY-BY-PLAY
out = ["# Play-by-Play - What Actually Happens, Step by Step",
       "",
       "Every playbook narrated as hub traffic: who moves, what envelope",
       "carries it, and what proves the step happened. GENERATED from",
       "claim_playbooks.py. The e2e suite",
       "(tests_claim/test_playbooks_e2e_all.py) executes these exact",
       "sequences against the real hub - this document describes what the",
       "tests prove.", ""]
for p in PB:
    out.append(f"## {p['num']} - {p['name']}")
    out.append("")
    out.append(f"*It starts when:* {p['trigger']}")
    out.append("")
    for title, rows in p["phases"]:
        out.append(f"**{title}**")
        out.append("")
        for r in rows:
            step, agent, action, intent, proof = r
            out.append(f"{step}. Agent {agent}: {action}.")
            out.append(f"   - Wire: {intent}")
            out.append(f"   - Proof it happened: {proof}")
        out.append("")
    out.append("*It can stop early:*")
    for a in p["abort"]:
        out.append(f"- {a}")
    out.append("")
open(os.path.join(DOCS, "PLAY-BY-PLAY.md"), "w").write("\n".join(out))
print("PLAY-BY-PLAY.md:", len(PB), "playbooks")
