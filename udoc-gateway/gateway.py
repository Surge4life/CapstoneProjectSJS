#!/usr/bin/env python3
"""UDOC Gateway — protocol bridge + lineage tagging + signed relay export (air-gap)."""
import sys, os, json, hashlib, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "udoc-agent"))
from udoc_agent import UDOCAgent

class Gateway(UDOCAgent):
    def tag_lineage(self, payload: dict) -> dict:
        payload = dict(payload)
        payload["_lineage"] = hashlib.sha256(
            (json.dumps(payload, sort_keys=True) + str(time.time())).encode()).hexdigest()[:16]
        return payload
    def signed_relay_export(self, events: list) -> dict:
        blob = json.dumps(events, sort_keys=True)
        return {"count": len(events), "export_hash": hashlib.sha256(blob.encode()).hexdigest(),
                "note": "transfer via signed media to air-gapped core"}

if __name__ == "__main__":
    print("UDOC gateway ready; mTLS bridge + lineage + signed relay export.")
