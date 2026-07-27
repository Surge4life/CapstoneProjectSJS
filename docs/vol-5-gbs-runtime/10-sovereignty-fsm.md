# Chapter 10 — Sovereignty Finite State Machine

## The Model Lifecycle as a State Machine

Every AI model registered with UDOC exists in one of a defined set of states. Transitions between states are governed — they require authorised actions and are permanently recorded. The sovereignty FSM is the mechanism by which the G.O.D.S ecosystem maintains the full lifecycle history of every registered AI model.

---

## States

```
pending_review          Model submitted, awaiting UDOC registration review
active                  Model is registered and operational
probationary            Model is active but under enhanced scrutiny
suspended               Model is operationally halted (administrative sanction)
revoked                 Model registration permanently revoked
expired                 Model certification has lapsed
decommissioned          Model intentionally retired by the operator
```

---

## State Transition Diagram

```
                          ┌──────────────────┐
                          │   pending_review  │
                          └────────┬─────────┘
                                   │ APPROVE_REGISTRATION (compliance)
                                   ▼
               ┌────────────────── active ───────────────────┐
               │                     │                        │
               │CERTIFY              │PLACE_PROBATION         │SUSPEND
               ▼                     ▼                        ▼
         [active,              probationary            suspended
          certified]               │                        │
                                   │LIFT_PROBATION           │LIFT_SUSPENSION
                                   ▼                        ▼
                                 active ←─────────────── active
                                   │
                                   │REVOKE (compliance)
                                   ▼
                                revoked
                                   
active/probationary ─EXPIRE_CERT──▶ expired
                                   │
                                   │RENEW_CERT (operator)
                                   ▼
                                 active

active/probationary ─DECOMMISSION (operator)──▶ decommissioned
```

---

## Transition Specifications

| Transition | From State | To State | Who Can Trigger | Required |
|-----------|-----------|---------|----------------|---------|
| `APPROVE_REGISTRATION` | `pending_review` | `active` | compliance | Conformance scan pass, governance review |
| `REJECT_REGISTRATION` | `pending_review` | `revoked` | compliance | Documented reason |
| `CERTIFY` | `active` | `active` (certified flag) | compliance | Re-evaluation |
| `PLACE_PROBATION` | `active` | `probationary` | compliance | Documented reason + probation plan |
| `LIFT_PROBATION` | `probationary` | `active` | compliance | Review period complete, criteria met |
| `SUSPEND` | `active`, `probationary` | `suspended` | compliance, gods_admin | Documented reason |
| `LIFT_SUSPENSION` | `suspended` | `active` | compliance | Review complete, remediation confirmed |
| `REVOKE` | Any non-revoked | `revoked` | compliance, gods_admin | Documented reason; permanent and irreversible |
| `EXPIRE_CERT` | `active`, `probationary` | `expired` | System (automated) | Certification expiry date reached |
| `RENEW_CERT` | `expired` | `active` | compliance | Re-evaluation |
| `DECOMMISSION` | `active` | `decommissioned` | operator, compliance | Formal decommission request |

---

## The Probationary State

Probationary is a governance tool for models that have passed registration but where concerns have been raised. A model in probationary state:

- **Can continue operating** — it is not suspended
- **Receives elevated EVA scrutiny** — probationary models cannot be auto-approved; all decisions are at minimum `REVIEW`
- **Has a defined probation plan** — specific criteria that must be met to exit probation
- **Has a probation expiry** — if criteria are not met by the expiry date, the model is suspended

Probation is used when:
- Pattern of BLOCK outcomes suggests systematic governance issues
- Operator has received compliance warnings but not acted
- Conformance scan raised concerns that don't warrant immediate suspension
- A governance incident is under investigation

---

## FSM Implementation

```python
class ModelStateMachine:
    VALID_TRANSITIONS = {
        ("pending_review", "APPROVE_REGISTRATION"): "active",
        ("pending_review", "REJECT_REGISTRATION"): "revoked",
        ("active", "PLACE_PROBATION"): "probationary",
        ("active", "SUSPEND"): "suspended",
        ("active", "REVOKE"): "revoked",
        ("active", "EXPIRE_CERT"): "expired",
        ("active", "DECOMMISSION"): "decommissioned",
        ("probationary", "LIFT_PROBATION"): "active",
        ("probationary", "SUSPEND"): "suspended",
        ("probationary", "REVOKE"): "revoked",
        ("probationary", "EXPIRE_CERT"): "expired",
        ("suspended", "LIFT_SUSPENSION"): "active",
        ("suspended", "REVOKE"): "revoked",
        ("expired", "RENEW_CERT"): "active",
    }

    def transition(self, model: AIModel, action: str, actor: User, reason: str) -> AIModel:
        key = (model.status, action)
        if key not in self.VALID_TRANSITIONS:
            raise InvalidTransitionError(model.status, action)
        
        new_state = self.VALID_TRANSITIONS[key]
        
        # Create FSM event record
        fsm_event = ModelFSMEvent(
            model_id=model.id,
            from_state=model.status,
            action=action,
            to_state=new_state,
            actor_id=actor.id,
            reason=reason,
        )
        
        # Write to audit chain
        audit_ref = audit_writer.write(
            event_type=f"GOVERNANCE.MODEL_{action}",
            resource_id=model.id,
            actor_id=actor.id,
            event_summary={"from": model.status, "to": new_state, "reason": reason}
        )
        
        model.status = new_state
        return model
```

---

## Irreversibility of Revocation

`REVOKE` is the only state transition that is explicitly flagged as irreversible. A revoked model:

- Cannot be reinstated — if the operator wants to use a version of this model again, they must submit a new registration
- Cannot transition to any other state
- Has its certification permanently invalidated
- Remains in the registry as `revoked` forever (the record is never deleted)

This irreversibility is a deliberate governance tool. If an operator knows that governance violations can lead to permanent revocation (not just suspension), they have a stronger incentive to operate within bounds.
