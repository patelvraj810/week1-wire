"""HubSpot adapter that sits BEHIND the gate. The agent never calls this directly.

If HUBSPOT_TOKEN is set: accounts, contacts and briefing status come from HubSpot,
briefs are saved as notes on the company, sends become tasks for the approver.
If not: everything falls back to fixtures/bank-account.json and crm_outbox/ (same as before).

Token lives only in your shell (`export HUBSPOT_TOKEN=...`), never in the repo.
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from urllib.error import HTTPError

API = "https://api.hubapi.com"


def enabled() -> bool:
    return bool(os.getenv("HUBSPOT_TOKEN"))


def _call(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {os.environ['HUBSPOT_TOKEN']}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        raise RuntimeError(f"HubSpot {method} {path} -> {e.code}: {e.read().decode()[:300]}") from e


def find_company(name: str) -> dict | None:
    """Look up the company by exact name and return it with the fields the gate needs."""
    res = _call("POST", "/crm/v3/objects/companies/search", {
        "filterGroups": [{"filters": [{"propertyName": "name", "operator": "EQ", "value": name}]}],
        "properties": ["name", "numberofemployees", "briefing_booked", "has_risk_committee"],
        "limit": 1})
    if not res.get("results"):
        return None
    c = res["results"][0]
    p = c["properties"]
    contacts = _call("GET", f"/crm/v4/objects/companies/{c['id']}/associations/contacts?limit=20").get("results", [])
    people = []
    for a in contacts:
        cp = _call("GET", f"/crm/v3/objects/contacts/{a['toObjectId']}?properties=firstname,lastname,jobtitle")["properties"]
        people.append({"name": f"{cp.get('firstname', '')} {cp.get('lastname', '')}".strip(),
                       "title": cp.get("jobtitle")})
    return {"hubspot_id": c["id"], "name": p.get("name"),
            "employees": int(p.get("numberofemployees") or 0),
            "briefing_booked": (p.get("briefing_booked") or "").lower() == "true",
            "has_risk_committee": None if p.get("has_risk_committee") is None
            else (p.get("has_risk_committee") or "").lower() == "true",
            "contacts": people}


def add_note(company_id: str, body: str) -> str:
    """Brief -> note on the company (association type 190 = note to company, HubSpot-defined)."""
    note = _call("POST", "/crm/v3/objects/notes", {
        "properties": {"hs_timestamp": int(time.time() * 1000), "hs_note_body": body[:65000]},
        "associations": [{"to": {"id": company_id},
                          "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 190}]}]})
    return f"hubspot:note:{note['id']}"


def add_task(company_id: str, subject: str, body: str) -> str:
    """Send request -> task for the approver (association type 192 = task to company). Never sends email."""
    task = _call("POST", "/crm/v3/objects/tasks", {
        "properties": {"hs_timestamp": int(time.time() * 1000), "hs_task_subject": subject[:250],
                       "hs_task_body": body[:65000], "hs_task_status": "NOT_STARTED",
                       "hs_task_priority": "HIGH"},
        "associations": [{"to": {"id": company_id},
                          "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 192}]}]})
    return f"hubspot:task:{task['id']}"
