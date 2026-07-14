#!/usr/bin/env python3
"""UDOC Sidecar — buffers governance events locally, replays to core on reconnect."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "udoc-agent"))
from udoc_agent import UDOCAgent

class Sidecar(UDOCAgent):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.buffer = []
    def govern(self, model_id, **sig):
        v = super().govern(model_id, **sig)
        if "unreachable" in " ".join(v.get("block_reasons", [])):
            self.buffer.append({"model_id": model_id, **sig})   # buffer for replay
        return v
    def replay(self):
        pending, self.buffer = self.buffer, []
        return [super(Sidecar, self).govern(p.pop("model_id"), **p) for p in pending]

if __name__ == "__main__":
    print("UDOC sidecar ready; buffers on outage, replays on reconnect.")
