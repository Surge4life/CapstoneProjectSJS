# Volume III — Repository Blueprint
## Every Folder. Every Responsibility.

> This volume is the map of the codebase. Before writing code, read this volume to understand where everything lives, what each directory owns, and what the boundaries are between modules.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-root-structure.md) | Root Structure |
| [02](02-platform-core.md) | platform-core — The Backend |
| [03](03-governance-engines.md) | governance-engines |
| [04](04-frontend-apps.md) | Frontend Applications (Web PWAs) |
| [05](05-mobile-builds.md) | Mobile Builds (Capacitor) |
| [06](06-desktop-builds.md) | Desktop Builds |
| [07](07-platform-web.md) | platform-web — Admin Console |
| [08](08-platform-internal.md) | platform-internal |
| [09](09-edge-components.md) | Edge Components (agent, gateway, edge, sidecar) |
| [10](10-infra.md) | infra — Docker, Kubernetes, Terraform |
| [11](11-hw-bringup.md) | hw-bringup — Hardware Initialisation |
| [12](12-branding.md) | branding — Brand Assets & Entity Constants |
| [13](13-tools.md) | tools — Developer Utilities |
| [14](14-naming-conventions.md) | Naming Conventions |

---

## Ownership Model

Each top-level directory in this monorepo has a single **owner domain**. No code crosses domain boundaries without an explicit interface contract. This is enforced by convention and documented here.

| Domain | Owner | Crosses Into |
|--------|-------|-------------|
| `platform-core` | Backend services | Governance engines via service calls |
| `governance-engines` | EVA, GIS, UDOC, G.O.D.S | Platform-core via bridge |
| `*-app` | Division web PWAs | Platform-core API only |
| `*-mobile` | Capacitor wrappers | Respective web app |
| `udoc-*` | Edge governance | Platform-core via mTLS |
| `infra` | Infrastructure | All services for deployment |
| `hw-bringup` | Hardware init | udoc-agent, platform-core |
