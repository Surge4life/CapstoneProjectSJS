# Security Operations path (assessment gap #4)
Governance security is implemented (fail-closed, sealed verdicts, immutable audit, sovereignty).
Operational SOC/SIEM is a deployment activity requiring live tooling + an ops team:
- SIEM: Wazuh or Security Onion ingesting platform-core audit + host logs.
- Network: Suricata/Zeek on the ingress plane (spec §8 trust zones).
- IR: runbooks tied to oversight cases (Pillar VIII human-in-the-loop).
Honest status: specified + hookable, not a standing SOC (which needs real infrastructure/staff).
