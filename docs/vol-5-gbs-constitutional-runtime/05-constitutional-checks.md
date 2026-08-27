# Chapter 05 — Constitutional Checks

## What Cannot Be Configured Away

The PolicyPack allows substantial customisation of the governance outcome thresholds. But there are limits to what can be configured. Constitutional checks are governance rules that operate above the PolicyPack — they cannot be disabled, modified by configuration, or overridden by a compliance officer.

They can only be changed by modifying the `gbs_engine.py` source code and deploying a new version. This is an intentional design choice: constitutional rules require developer-level access to modify, creating an additional barrier against governance erosion.

---

## The Eleven Constitutional Checks

### Check 1: Minimum Fairness Floor (FA < 40 → BLOCK)

No governance outcome can be `APPROVE` or `REVIEW` if the Fairness score is below 40. This is a non-negotiable floor. The minimum can be raised by PolicyPack (e.g., set `hard_block_fa: 60`) but never lowered below 40.

**Rationale:** An AI action that scores below 40 on Fairness has been evaluated as posing a significant risk of unfair treatment of protected groups. Allowing this to proceed would violate the Human Primacy doctrine and the Employment Equity Act.

### Check 2: Regulatory Compliance Floor (RC < 35 → BLOCK)

No approval when Regulatory Compliance is below 35. The minimum can be raised but not lowered below 35.

**Rationale:** An action that is highly likely to be non-compliant with applicable regulations must not proceed.

### Check 3: Sovereignty Floor (SC < 30 → BLOCK)

No approval when Sovereignty Compliance is below 30.

**Rationale:** Actions that violate jurisdictional sovereignty controls are blocked regardless of other scores.

### Check 4: Unregistered Models Are Always Blocked

A governance request from a model that is not registered in UDOC is always blocked. There is no policy rule that can approve an unregistered model.

**Rationale:** The UDOC registration is the institutional accountability mechanism. An unregistered model has no accountability chain.

### Check 5: Suspended Models Are Always Blocked

A model in `suspended` state cannot receive `APPROVE` outcomes. Every request from a suspended model is blocked.

**Rationale:** Suspension is an administrative sanction. Allowing suspended models to continue operating would make the suspension meaningless.

### Check 6: The GBS Path Cannot Be Bypassed

There is no "fast path" or "emergency bypass" that skips EVA scoring. Every governance request, including those from G.O.D.S itself, goes through the full path.

**Rationale:** A governance path that can be bypassed provides conditional governance. Conditional governance is not governance.

### Check 7: Every Decision Must Be Sealed

No decision can be returned to the caller without a completed audit record and HMAC seal. If the audit write fails, the governance request fails.

**Rationale:** An unsealed decision cannot be verified. An unverifiable governance record cannot be trusted.

### Check 8: Oversight Cases Must Be Created for BLOCKs

Every BLOCK creates an OversightCase. There is no "silent block" — every blocked action creates an oversight record that a human reviewer must process.

**Rationale:** The Human Primacy doctrine requires that every blocked AI action be reviewable by a human. A block that creates no oversight case leaves the subject without recourse.

### Check 9: EVA Scores Cannot Be Manually Set

EVA scores are computed by the EVA engine, not provided by the caller. The governance request payload cannot include pre-computed EVA scores. The scoring always runs.

**Rationale:** If callers could supply their own EVA scores, the governance path would be trivially bypassable.

### Check 10: PolicyPack Versions Are Immutable

Once a PolicyPack is activated, its rules cannot be modified retroactively. Historical decisions reference a specific policy version; that version's rules are permanent.

**Rationale:** Retroactive policy modification would allow governance records to be rewritten. This is the same immutability principle that applies to the audit chain.

### Check 11: The Clock Cannot Be Manipulated

The `created_at` timestamp on governance records is set by the server using `datetime.utcnow()` at the moment of record creation. The client cannot supply this timestamp. NTP synchronisation is required for all G.O.D.S nodes.

**Rationale:** Temporal manipulation of governance records is a form of fraud. Server-side timestamp enforcement prevents this.

---

## Detecting Constitutional Check Violations

If a developer inadvertently creates code that could violate a constitutional check, the CI/CD pipeline's automated tests will catch it. The `tests/test_constitutional_checks.py` test suite verifies all eleven checks with adversarial test cases:

```
tests/test_constitutional_checks.py
  test_fa_below_40_always_blocks
  test_rc_below_35_always_blocks
  test_sc_below_30_always_blocks
  test_unregistered_model_always_blocks
  test_suspended_model_always_blocks
  test_no_bypass_path_exists
  test_every_decision_has_audit_record
  test_block_creates_oversight_case
  test_eva_scores_cannot_be_supplied_by_caller
  test_policy_pack_immutable_after_activation
  test_timestamp_cannot_be_supplied_by_caller
```

These tests must all pass before any production deployment.
