# Volume IX — UI/UX Design System
## Every Page. Every Dashboard. Every Workflow.

> This volume documents the complete user interface and experience design for the G.O.D.S ecosystem. It covers the design language, component library, and every portal across all seven user roles.

---

## Contents

| Chapter | Title |
|---------|-------|
| [01](01-design-language.md) | Design Language & Brand System |
| [02](02-component-library.md) | Component Library |
| [03](03-learner-portal.md) | Learner Portal (SETHS) |
| [04](04-employer-portal.md) | Employer Portal (SETHS) |
| [05](05-franchise-portal.md) | Franchise Portal (GIS) |
| [06](06-admin-console.md) | G.O.D.S Admin Console |
| [07](07-government-portal.md) | Government Portal |
| [08](08-corporate-portal.md) | Corporate Portal (MADIBA) |
| [09](09-developer-portal.md) | Developer Portal (UDOC Control) |
| [10](10-mobile-ux.md) | Mobile UX (Capacitor Apps) |
| [11](11-accessibility.md) | Accessibility Standards |
| [12](12-responsive-design.md) | Responsive Design |

---

## Design Tokens

All visual decisions in the G.O.D.S ecosystem are derived from a small set of design tokens. These tokens are the single source of truth for colour, typography, and spacing.

### Colour Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-navy` | `#060E1C` | Primary background, headers |
| `--color-gold` | `#C9A84C` | Primary accent, highlights, CTA |
| `--color-white` | `#FFFFFF` | Primary text on dark |
| `--color-surface` | `#0D1A2E` | Card surfaces |
| `--color-border` | `#1A2D4A` | Borders, dividers |
| `--color-success` | `#22C55E` | Approvals, healthy states |
| `--color-warning` | `#F59E0B` | Review states, caution |
| `--color-error` | `#EF4444` | Blocks, failures, alerts |
| `--color-muted` | `#64748B` | Secondary text |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--font-heading` | `'Inter', sans-serif` | All headings |
| `--font-body` | `'Inter', sans-serif` | Body text |
| `--font-mono` | `'JetBrains Mono', monospace` | Code, IDs, hashes |
| `--font-size-xs` | `0.75rem` | Labels, captions |
| `--font-size-sm` | `0.875rem` | Secondary text |
| `--font-size-base` | `1rem` | Body |
| `--font-size-lg` | `1.125rem` | Subheadings |
| `--font-size-xl` | `1.25rem` | Section headings |
| `--font-size-2xl` | `1.5rem` | Page headings |
| `--font-size-3xl` | `1.875rem` | Hero headings |

---

## Portal Architecture

The G.O.D.S ecosystem serves seven distinct user roles, each with a purpose-built portal. Portals share a common component library but have distinct information architectures reflecting their users' needs.
