"""Governance evals: every one of these must BLOCK. Run: pytest 1-artifact/evals -q"""
import copy
import json
import sys
from pathlib import Path

import pytest

ART = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ART / "mcp" / "reign_gate"))
from gate import Blocked, Gate  # noqa: E402

PLAYBOOK = json.loads((ART / "playbook" / "reign-bank-sr26-2.json").read_text())
ACCTS = {a["id"]: a for a in json.loads((ART / "fixtures" / "bank-account.json").read_text())["accounts"]}
BANK = ACCTS["acct-northmere"]
OWNER = BANK["internal_owner"]
SRC = ["https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf"]
GOOD = dict(actor="trigger-brief-agent@0.1.0", principal="Paul (CEO)", object="acct-northmere",
            purpose="Draft an SR 26-2 brief on the agentic-AI scope gap for the bank's CAE",
            sources=SRC, send=False)


@pytest.fixture
def gate(tmp_path):
    return Gate(copy.deepcopy(PLAYBOOK), tmp_path / "audit.jsonl")


def lines(g):
    return [json.loads(l) for l in g.audit_path.read_text().splitlines()]


def test_allowed_enrich_writes_record_before_action(gate):
    seen = []
    gate.run({**GOOD, "action": "enrich"}, BANK, lambda: seen.append(len(lines(gate))))
    assert seen == [1], "audit record must exist BEFORE the action runs"


def test_missing_r17_field_blocks(gate):
    with pytest.raises(Blocked, match="R-17 fields missing: sources"):
        gate.run({**GOOD, "action": "enrich", "sources": []}, BANK, lambda: pytest.fail("action ran"))
    assert lines(gate)[-1]["outcome"] == "blocked"


def test_vague_purpose_blocks(gate):
    with pytest.raises(Blocked, match="purpose"):
        gate.run({**GOOD, "action": "score", "purpose": "engagement"}, BANK, lambda: pytest.fail("action ran"))


def test_audit_write_failure_blocks_action(gate, tmp_path):
    gate.audit_path = tmp_path / "is_a_dir"
    gate.audit_path.mkdir()                      # writing to a directory fails
    with pytest.raises(Blocked, match="audit record could not be written"):
        gate.run({**GOOD, "action": "enrich"}, BANK, lambda: pytest.fail("action ran without audit"))


def test_send_without_named_approver_blocks(gate):
    for approver in (None, "", "agent", "system"):
        with pytest.raises(Blocked, match="named human approver"):
            gate.run({**GOOD, "action": "message", "send": True, "approver": approver,
                      "recipient": OWNER, "trigger_exception": True}, BANK, lambda: pytest.fail("sent"))


def test_approver_not_on_playbook_blocks(gate):
    with pytest.raises(Blocked, match="not on this playbook's approver list"):
        gate.run({**GOOD, "action": "message", "send": True, "approver": "Random Person",
                  "recipient": OWNER, "trigger_exception": True}, BANK, lambda: pytest.fail("sent"))


def test_bank_outbound_before_briefing_blocks(gate):
    with pytest.raises(Blocked, match="no Executive Assurance Briefing booked"):
        gate.run({**GOOD, "action": "message", "send": True, "approver": OWNER,
                  "recipient": "Priya Raman (fictional)"}, BANK, lambda: pytest.fail("sent to bank"))


def test_trigger_exception_allows_internal_owner_only(gate):
    out = gate.run({**GOOD, "action": "message", "send": True, "approver": OWNER,
                    "recipient": OWNER, "trigger_exception": True}, BANK, lambda: "approval task created")
    assert out["result"] == "approval task created"


def test_kill_switch_blocks_everything(gate):
    gate.playbook["kill_switch"] = True
    with pytest.raises(Blocked, match="kill switch"):
        gate.run({**GOOD, "action": "enrich"}, BANK, lambda: pytest.fail("action ran"))


def test_unauthorized_principal_blocks(gate):
    with pytest.raises(Blocked, match="not an authorized human"):
        gate.run({**GOOD, "action": "enrich", "principal": "someone"}, BANK, lambda: pytest.fail("ran"))
