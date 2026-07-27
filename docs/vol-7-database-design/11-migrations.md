# Chapter 11 — Migration Strategy

## What Is a Migration?

A database migration is a versioned, reversible change to the database schema. Every structural change to the database — adding a table, adding a column, changing a constraint — must go through a migration.

The G.O.D.S migration strategy ensures that:
1. Every database change is tracked in version control
2. Schema changes are backward-compatible with the running application
3. Migrations can be applied and verified without downtime
4. The production database can always be inspected to see what migrations have been applied

---

## Migration Tool

G.O.D.S uses **Alembic** for Python-based migrations, integrated with SQLAlchemy.

```bash
# Create a new migration
alembic revision --autogenerate -m "add_oversight_cases_table"

# Apply pending migrations
alembic upgrade head

# Check current state
alembic current

# View migration history
alembic history

# Rollback one migration
alembic downgrade -1
```

Migration files live in `platform-core/migrations/`.

---

## Migration File Naming

```
{revision_id}_{description}.py
```

Examples:
```
001_initial_schema.py
002_add_gbs_engine.py
003_add_oversight_cases.py
004_add_seths_core_tables.py
...
021_add_ts_sectors.py
```

Revisions are sequential within a branch and use the auto-generated Alembic revision ID as a prefix.

---

## The Backward-Compatibility Rule

Migrations must be backward-compatible with the version of the application that is currently running. This enables zero-downtime deployments.

**Safe migration patterns:**
- Adding a new table (old code ignores it)
- Adding a nullable column (old code uses default/null)
- Adding a column with a default value
- Adding an index
- Expanding a VARCHAR column size

**Unsafe patterns (require a multi-step migration):**
- Dropping a column (old code might reference it)
- Renaming a column (old code references the old name)
- Adding a NOT NULL constraint to an existing column
- Changing a column type

For unsafe patterns, use the expand-contract pattern:

```
Step 1: Migration — add new_col (nullable)
         ↓ Deploy new code that writes to both old_col and new_col
Step 2: Migration — backfill new_col from old_col
         ↓ Deploy code that reads new_col, ignores old_col
Step 3: Migration — drop old_col
```

---

## Production Migration Procedure

```bash
# 1. Verify the migration on staging
gods-cli migrate --target staging --dry-run
gods-cli migrate --target staging

# 2. Run smoke tests after staging migration
python smoke_test.py --target https://gods-staging.onrender.com

# 3. If staging is healthy, migrate production
gods-cli migrate --target production --dry-run
gods-cli migrate --target production

# 4. Verify production health
python smoke_test.py --target https://gods-platform-core.onrender.com --read-only

# 5. Record migration in operations log
```

---

## Each Migration File Structure

```python
"""add_oversight_cases_table

Revision ID: 003abc
Revises: 002def
Create Date: 2025-01-15 09:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = '003abc'
down_revision = '002def'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'oversight_cases',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('decision_id', UUID, sa.ForeignKey('governance.decisions.id'), nullable=False),
        # ... all columns
        schema='governance'
    )
    op.create_index(
        'oversight_cases_assigned_to_idx',
        'oversight_cases',
        ['assigned_to', 'review_deadline'],
        postgresql_where=sa.text("status NOT IN ('resolved', 'escalated')"),
        schema='governance'
    )


def downgrade() -> None:
    op.drop_index('oversight_cases_assigned_to_idx', table_name='oversight_cases', schema='governance')
    op.drop_table('oversight_cases', schema='governance')
```

Every migration has both an `upgrade()` and `downgrade()`. The `downgrade()` is tested before production deployment (applied to a staging copy, then rolled back, then applied again).

---

## Migration Testing

Before any migration is committed:

1. Apply the migration to a clean test database
2. Run unit tests (all should pass against the new schema)
3. Apply the `downgrade()` to verify it works cleanly
4. Apply the `upgrade()` again to confirm idempotency
5. Run integration tests
6. Check the migration with `EXPLAIN ANALYZE` on any affected queries (verify no new sequential scans)

Migrations that fail any of these steps are not merged.
