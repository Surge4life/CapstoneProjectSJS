# Chapter 13 — tools

## What Lives Here

`tools/` contains developer utilities, CLI tools, and scripts that support development and operations but are not part of the runtime application.

---

## Directory Structure

```
tools/
├── gods-cli/               Command-line tool for deployment and operations
├── dev-setup/              Development environment setup scripts
└── schema-export/          Database schema export utilities
```

---

## `gods-cli/`

The G.O.D.S command-line tool. Used for deployment, database operations, audit chain verification, and policy management.

**Installation:**
```bash
cd tools/gods-cli
npm install -g .
# or for development (no global install)
node tools/gods-cli/index.js <command>
```

**Full command reference:** See Volume X, Chapter 18 (Deployment Engine).

**Key command groups:**

| Group | Commands |
|-------|---------|
| `health-check` | Check service health |
| `deploy` | Deploy to target environment |
| `migrate` | Database migrations |
| `verify-chain` | Audit chain integrity verification |
| `policy` | PolicyPack management |
| `export-config` | Configuration export/import |
| `verify-bundle` | Air-gap update bundle verification |

---

## `dev-setup/`

Scripts that automate the development environment setup described in Volume VI, Chapter 01.

```bash
# Set up the complete development environment
./tools/dev-setup/setup.sh

# Start all development services
./tools/dev-setup/start-all.sh

# Stop all development services
./tools/dev-setup/stop-all.sh

# Reset development database (destructive)
./tools/dev-setup/reset-db.sh
```

---

## `schema-export/`

Utilities for exporting the database schema in various formats:

```bash
# Export schema as SQL
node tools/schema-export/export-sql.js > schema.sql

# Export schema as markdown (for documentation)
node tools/schema-export/export-md.js > docs/schema-reference.md

# Export schema as JSON (for tooling)
node tools/schema-export/export-json.js > schema.json
```

The markdown export is used to keep the database documentation in Volume VII up-to-date. Run it whenever a migration adds or changes tables, and update the relevant chapter.

---

## Adding New Tools

When adding a new tool to `tools/`:

1. Create a new subdirectory with a descriptive name
2. Include a `README.md` explaining what the tool does, how to install it, and how to use it
3. Add an entry to this chapter (Chapter 13 of Volume III)
4. If the tool is used in CI/CD, add it to `infra/ci/scripts/`
5. If the tool requires installation, document the installation in Volume VI (environment setup)

Tools should be self-contained — do not depend on application code from `platform-core` unless absolutely necessary. This keeps tools usable even when the main application cannot run.
