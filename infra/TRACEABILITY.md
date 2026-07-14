# Architecture Traceability Matrix (the assessment's "biggest missing item")
Requirement → Patent Claim → System Component → API → Database → Test

| Requirement | Patent claim area | Component | API | DB table | Test |
|---|---|---|---|---|---|
| Every AI decision governed & sealed | Lorentz/governance sealing | governance_bridge | POST /decisions | decisions | smoke[4], pytest test_register_and_decide_approve |
| Bias/fairness blocking | EVA disparate-impact | governance_bridge | POST /decisions | decisions | pytest test_biased_blocks |
| Sovereignty non-bypassable | sovereignty SVS=min | governance_bridge | POST /decisions | decisions | pytest test_sovereignty_breach_blocks |
| Immutable audit | hash-chain + Merkle | audit_writer | GET /audit/chain/* | audit_refs | pytest test_audit_chain_intact |
| Human oversight (Pillar VIII) | HITL override logging | oversight router | /oversight/* | oversight_cases | smoke (oversight) |
| Workforce reintegration | SETHS process | seths + portal_student | /seths, /portal/student | students, seths_learners | portal lifecycle test |
| Placement → employment | SETHS→TS loop | portal_employer | /portal/employer/.../offer | employees, applications | portal lifecycle test |
| Capital recycle >50% | MADIBA Pillar 2 | madiba router | /madiba/allocate | madiba_cycles | analytics kpis test |
| Data record & analytics | UDOC analytics | analytics_engine | /analytics/* | division_records | smoke[6b] |
| Boot validates hardware | self-test/fail-closed | udoc-selftest | (boot) | (run report) | boot_sequence emulation |
| Signed air-gap release | offline update authority | release-tooling | (CLI) | (manifest) | smoke[8] |
