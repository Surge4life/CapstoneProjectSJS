#!/usr/bin/env python3
"""UDOC Edge Node — autonomous local governance with a registry mirror; syncs when online."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "udoc-agent"))
from udoc_agent import UDOCAgent
from app_local_eva import local_decide   # local fallback engine

class EdgeNode(UDOCAgent):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.local_registry = {}
    def govern(self, model_id, **sig):
        v = super().govern(model_id, **sig)
        if "unreachable" in " ".join(v.get("block_reasons", [])):
            # autonomous local decision when core is unreachable
            return local_decide(model_id, sig)
        return v

if __name__ == "__main__":
    print("UDOC edge node ready; autonomous local governance + sync-on-connect.")
