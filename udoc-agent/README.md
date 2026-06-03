# UDOC Agent
Lightweight host process for VMs/bare-metal. Routes host AI requests through
platform-core `/decisions`, fail-CLOSED for critical tiers when governance is unreachable.
Run: `python3 udoc_agent.py --core http://core:8000 --token <jwt> --model model-001`
Attachment class per hardware spec §7 (host agent: 4–8 vCPU, 8–16 GB).
