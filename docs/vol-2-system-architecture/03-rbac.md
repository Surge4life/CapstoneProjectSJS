# Chapter 03 — Role-Based Access Control (RBAC)

## Purpose

The RBAC system is the access control layer of the G.O.D.S ecosystem. It determines what every authenticated user can do — which endpoints they can call, which records they can read, which operations they can perform. The RBAC system is the enforcement mechanism for the Human Primacy doctrine and the Jurisdictional Sovereignty pillar.

---

## Location

- **Router:** `platform-core/app/routers/rbac.py`
- **Service:** `platform-core/app/services/rbac.py`
- **Dependency:** `platform-core/app/core/dependencies.py` — `require_permission()`
- **Models:** `platform-core/app/db/models/user.py` — `Role`, `RoleAssignment`, `Permission`

---

## Role Architecture

G.O.D.S uses **attribute-based role composition**. Roles are not inherited hierarchically (no "admin inherits operator"). Instead, each role is a named bundle of permissions. `gods_admin` has all permissions not because it inherits from every role, but because it was explicitly granted every permission.

This design makes security audits straightforward: the permissions of any role are always explicitly enumerable.

---

## System Roles Reference

### `gods_admin`

**Scope:** All divisions, all tenants  
**Description:** Full platform control. Reserved for the platform operator. Should have maximum two accounts per deployment.  
**Permissions:** All permissions in the system  
**Audit:** Every action by a `gods_admin` user generates a `GODS_ADMIN_ACTION` audit event, separate from normal action audit records.

---

### `division_admin`

**Scope:** One division (set at role assignment)  
**Description:** Full control within the assigned division. Cannot access other divisions or platform-level configuration.  
**Key permissions:**
- `{division}:*` — all actions within assigned division
- `users:read` — read user records within division scope
- `rbac:assign_within_division` — assign division roles to users

---

### `compliance`

**Scope:** All divisions (read), compliance actions (write)  
**Description:** Compliance officers reviewing governance outcomes and policy compliance.  
**Key permissions:**
- `decisions:read:all` — read all governance decisions
- `oversight:read:all` — read all oversight cases
- `oversight:assign` — assign oversight cases to reviewers
- `oversight:resolve` — resolve oversight cases
- `models:certify` — certify AI models
- `models:suspend:any` — suspend any model
- `policy:read` — read policy rules
- `bias:read:all` — read all bias reports

---

### `sovereignty`

**Scope:** All divisions (read), sovereignty actions (write)  
**Description:** Sovereignty officers managing jurisdictional declarations and cross-border authorisations.  
**Key permissions:**
- `sovereignty:read:all`
- `sovereignty:declare_jurisdiction`
- `sovereignty:authorise_cross_border`
- `decisions:read:all` (for sovereignty analysis)

---

### `supervisor`

**Scope:** One division  
**Description:** Supervisors reviewing oversight cases within their division.  
**Key permissions:**
- `oversight:read:division`
- `oversight:review:division` — review and add notes to cases
- `decisions:read:division`
- `{division}:read`

---

### `operator`

**Scope:** Own AI models and governance records  
**Description:** External AI operators who have registered models with UDOC.  
**Key permissions:**
- `models:register`
- `models:view_own`
- `models:suspend:own`
- `decisions:create` — submit governance requests
- `decisions:read:own`
- `audit:read:own`

---

### `analyst`

**Scope:** One division (read-only analytics)  
**Description:** Data analysts reviewing governance and operational metrics.  
**Key permissions:**
- `analytics:read:division`
- `decisions:read:division` (aggregate only, no PII)
- `bias:read:division`

---

### `learner`

**Scope:** Own SETHS records only  
**Description:** Individuals enrolled in the SETHS system.  
**Key permissions:**
- `seths:read:own`
- `seths:apply`
- `documents:upload:own`
- `documents:read:own`
- `oversight:challenge` — initiate a governance challenge on own records

---

### `employer`

**Scope:** Own employer records and posted opportunities  
**Description:** Employers posting opportunities and managing applications.  
**Key permissions:**
- `seths:employer:read:own`
- `opportunities:create`
- `opportunities:manage:own`
- `applications:read:own_opportunities`
- `applications:update_status:own_opportunities`

---

### `investor`

**Scope:** Own MADIBA records  
**Key permissions:**
- `madiba:read:own`
- `madiba:milestones:read`

---

### `external_auditor`

**Scope:** All (read-only)  
**Description:** Third-party auditors with time-limited read access to governance records.  
**Key permissions:**
- `audit:read:all`
- `decisions:read:all`
- `oversight:read:all` (resolved cases only)
- Role is always time-limited — `expires_at` is required on assignment

---

## Permission Enforcement

The `require_permission()` FastAPI dependency enforces RBAC on every protected endpoint:

```python
@router.patch("/{model_id}/suspend")
async def suspend_model(
    model_id: UUID,
    request: SuspendRequest,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("models:suspend:own"))
):
    # The dependency has already verified the permission.
    # If the user doesn't have it, a 403 was returned before this line.
    ...
```

For "own" scoped permissions, the service layer checks ownership after the RBAC check:

```python
# Service layer — after RBAC has passed
if not current_user.has_permission("models:suspend:any"):
    if model.operator_id != current_user.id:
        raise InsufficientPermissionsError("You can only suspend your own models.")
```

---

## RBAC Audit Trail

Every RBAC event is permanently recorded:
- Role assignment (who assigned, to whom, which role, expiry if any)
- Role revocation (who revoked, why)
- Permission check failure (which permission, which user, which endpoint)

Permission check failures are rate-monitored — a burst of failures from one user is a security signal.
