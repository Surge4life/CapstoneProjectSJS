#!/usr/bin/env python3
"""
UDOC Agent — lightweight host process (Windows/Linux servers & VMs).
Intercepts AI requests on the host and routes them through platform-core /decisions
before they execute. Fail-CLOSED for critical risk tiers (per hardware spec).
"""
import argparse
import json
import urllib.request

class UDOCAgent:
    def __init__(self, core_url="http://localhost:8000", token="", fail_closed=True):
        self.core_url = core_url.rstrip("/")
        self.token = token
        self.fail_closed = fail_closed

    def govern(self, model_id: str, **signals) -> dict:
        """Submit an AI request for governance; returns the verdict or fail-closed BLOCK."""
        body = json.dumps({"model_id": model_id, **signals}).encode()
        req = urllib.request.Request(f"{self.core_url}/decisions", data=body,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {self.token}"})
        try:
            with urllib.request.urlopen(req, timeout=2) as r:
                return json.load(r)
        except Exception as e:
            if self.fail_closed:
                return {"model_id": model_id, "decision": "BLOCK", "sovereign": False,
                        "block_reasons": [f"governance unreachable — fail-closed ({e})"]}
            return {"model_id": model_id, "decision": "REVIEW", "block_reasons": [str(e)]}

    def allow(self, verdict: dict) -> bool:
        return verdict.get("decision") == "APPROVE"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="UDOC host agent")
    ap.add_argument("--core", default="http://localhost:8000")
    ap.add_argument("--token", default="")
    ap.add_argument("--model", required=True)
    a = ap.parse_args()
    agent = UDOCAgent(a.core, a.token)
    v = agent.govern(a.model)
    print(json.dumps(v, indent=2))
    print("ALLOW" if agent.allow(v) else "DENY (fail-closed/blocked)")
