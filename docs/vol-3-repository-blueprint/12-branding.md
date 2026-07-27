# Chapter 12 — branding

## What Lives Here

`branding/` contains the canonical brand assets and entity constants for the G.O.D.S ecosystem. All visual decisions (colours, logos, entity names) must be sourced from here.

---

## Directory Structure

```
branding/
├── assets/
│   └── G.O.D.S LOGO.jpeg        Official logo mark
├── entity.json                   Machine-readable entity constants
└── footer-disclaimer.html        Standard legal footer (copy into all HTML templates)
```

---

## `entity.json` — Machine-Readable Brand Constants

This file is the authoritative source for entity metadata used across the ecosystem.

```json
{
  "entity": {
    "legal_name": "G.O.D.S Holdings (Pty) Ltd",
    "status": "proposed",
    "registered": false,
    "registration_number": null,
    "founder": "Sashin J. Singh",
    "ip_holder": "Sashin J. Singh",
    "ip_transfer_target": "G.O.D.S IP Trust (proposed)",
    "jurisdiction": "South Africa",
    "email_domain": "gods.local",
    "mark_notation": "™"
  },
  "brand": {
    "primary_name": "G.O.D.S",
    "full_name": "Governance, Operations, Decisioning, and Sovereignty",
    "colours": {
      "navy": "#060E1C",
      "gold": "#C9A84C",
      "white": "#FFFFFF"
    },
    "divisions": {
      "udoc": {
        "name": "UDOC Control",
        "full_name": "Universal Declaration of Operations Compliance",
        "accent": "#3B82F6"
      },
      "seths": {
        "name": "SETHS",
        "full_name": "Skills, Employment, Training, and Human Services",
        "accent": "#22C55E"
      },
      "madiba": {
        "name": "MADIBA",
        "accent": "#8B5CF6"
      },
      "ts": {
        "name": "TS Industries",
        "accent": "#F97316"
      }
    }
  }
}
```

---

## `footer-disclaimer.html`

The standard legal footer used in all HTML templates. Content:

```html
<footer class="gods-footer">
  <p>
    G.O.D.S Holdings (Pty) Ltd is a <strong>proposed entity</strong> — not yet
    registered with CIPC. All intellectual property vests in Sashin J. Singh 
    pending formal registration and IP Trust establishment. All marks carry ™ 
    notice only; ® notation will only be used after confirmed CIPC registration 
    and trademark registration.
  </p>
</footer>
```

**This disclaimer must appear on all externally facing pages, reports, and marketing materials until CIPC registration is confirmed.**

---

## Logo Usage Rules

The `G.O.D.S LOGO.jpeg` is the official logo mark. Usage rules:

| Context | Allowed Usage |
|---------|-------------|
| Dark background (navy) | Full colour logo |
| Light background | Navy version of logo |
| Favicon | Icon mark only (no wordmark) |
| Watermarks | 20% opacity |
| Minimum size | 32px height |

**Do not:**
- Distort or skew the logo
- Apply effects (shadows, outlines, gradients) to the logo
- Use the logo on a background that reduces legibility
- Use the logo without the ™ notation in proximity on first use on a page

---

## Using Brand Assets in Code

Import the entity constants from `branding/entity.json` in any application:

```typescript
import entity from '../../../../branding/entity.json';

// Use the canonical values
const primaryColour = entity.brand.colours.navy;   // "#060E1C"
const goldAccent = entity.brand.colours.gold;       // "#C9A84C"
const divisionAccent = entity.brand.divisions.seths.accent; // "#22C55E"
```

Never hardcode brand colours or entity details in application code. Always import from this file.
