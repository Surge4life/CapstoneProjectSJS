# Chapter 01 — Design Language & Brand System

## The G.O.D.S Visual Identity

The G.O.D.S design language is built on one principle: **governance is serious work, and the interface must communicate that seriousness without sacrificing usability**.

This is not a consumer app. It is governance infrastructure. The interface is used by compliance officers, employment practitioners, AI operators, and institutional investors. They are professionals. They need density, precision, and clarity — not playfulness.

---

## The Visual Concept: Sovereign Architecture

The G.O.D.S interface draws inspiration from the visual language of institutional architecture — the kind of buildings that are meant to outlast their builders. Dark, authoritative, precise. Gold as the accent of institutional trust. Clean lines. Deliberate hierarchy.

This concept guides every decision:
- **Backgrounds are dark navy** — authority, depth, permanence
- **Gold accents are sparse and meaningful** — trust, importance, action
- **Typography is clean and precise** — information, not decoration
- **Status colours are bold and unambiguous** — governance decisions must be instantly readable

---

## Brand Constants

Sourced from `branding/entity.json` and `BRAND_AND_ENTITY_CONSTANTS.md`.

### Entity

| Field | Value |
|-------|-------|
| Legal name | G.O.D.S Holdings (Pty) Ltd (proposed) |
| Status | Pre-registration — entity proposed, not yet registered |
| Founder | Sashin J. Singh |
| IP holder | Sashin J. Singh (pending trust transfer) |
| Jurisdiction | South Africa |
| Mark notation | ™ (not ® until CIPC registration) |

### Colour System

```css
:root {
  /* Brand Core */
  --color-navy:          #060E1C;  /* Primary background */
  --color-gold:          #C9A84C;  /* Primary accent */
  --color-white:         #FFFFFF;  /* Primary text on dark */
  
  /* Surfaces */
  --color-surface-1:     #0A1628;  /* Card, panel background */
  --color-surface-2:     #0D1A2E;  /* Nested card, code block */
  --color-surface-3:     #112035;  /* Hover state, selected */
  
  /* Borders */
  --color-border:        #1A2D4A;  /* Standard border */
  --color-border-strong: #243D5E;  /* Emphasis border */
  --color-border-gold:   rgba(201, 168, 76, 0.3);  /* Gold border, subtle */
  
  /* Status (governance outcomes) */
  --color-approve:       #22C55E;  /* APPROVE — green */
  --color-review:        #F59E0B;  /* REVIEW — amber */
  --color-escalate:      #F97316;  /* ESCALATE — orange */
  --color-block:         #EF4444;  /* BLOCK — red */
  
  /* Text */
  --color-text-primary:  #F1F5F9;  /* Main text */
  --color-text-secondary:#94A3B8;  /* Secondary text, labels */
  --color-text-muted:    #64748B;  /* Placeholder, disabled */
  --color-text-gold:     #C9A84C;  /* Gold text, emphasis */
  
  /* Semantic */
  --color-success:       #22C55E;
  --color-warning:       #F59E0B;
  --color-error:         #EF4444;
  --color-info:          #3B82F6;
}
```

### Typography Scale

```css
:root {
  --font-sans:     'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:     'JetBrains Mono', 'Fira Code', monospace;
  
  --text-xs:       0.75rem;    /* 12px — labels, captions, badges */
  --text-sm:       0.875rem;   /* 14px — secondary body, table data */
  --text-base:     1rem;       /* 16px — primary body */
  --text-lg:       1.125rem;   /* 18px — emphasis body */
  --text-xl:       1.25rem;    /* 20px — section subheading */
  --text-2xl:      1.5rem;     /* 24px — section heading */
  --text-3xl:      1.875rem;   /* 30px — page heading */
  --text-4xl:      2.25rem;    /* 36px — hero heading */
  
  --font-normal:   400;
  --font-medium:   500;
  --font-semibold: 600;
  --font-bold:     700;
  
  --leading-tight:  1.25;
  --leading-normal: 1.5;
  --leading-relaxed:1.75;
}
```

### Spacing Scale

```css
:root {
  --space-1:  0.25rem;   /* 4px */
  --space-2:  0.5rem;    /* 8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.25rem;   /* 20px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
}
```

### Border Radius

```css
:root {
  --radius-sm:   0.25rem;   /* 4px — inputs, small chips */
  --radius-md:   0.5rem;    /* 8px — cards, buttons */
  --radius-lg:   0.75rem;   /* 12px — panels */
  --radius-xl:   1rem;      /* 16px — modal, overlay */
  --radius-full: 9999px;    /* Pills, avatars */
}
```

---

## Division Accent Colours

Each division has a secondary accent colour used for visual differentiation in shared contexts (like the G.O.D.S Admin Console where all four divisions appear).

| Division | Accent | Usage |
|----------|--------|-------|
| UDOC Control | `#3B82F6` (blue) | Model registry, governance metrics |
| SETHS | `#22C55E` (green) | Workforce, learner progress |
| MADIBA | `#8B5CF6` (purple) | Capital, institutional finance |
| TS Industries | `#F97316` (orange) | Industrial projects, SPVs |

---

## Component Design Principles

### 1. Status at a Glance

Governance outcomes (`APPROVE`, `REVIEW`, `ESCALATE`, `BLOCK`) must be instantly distinguishable by colour and label without requiring the user to read the text. Use both colour and icon together — never colour alone (accessibility).

### 2. Dense, Not Cluttered

Professional users work with this interface all day. Prioritise data density over whitespace. A dashboard that requires 5 clicks to see key metrics is worse than a dense one that shows everything on one screen.

### 3. Confirmation for Consequential Actions

Actions that cannot be undone (suspend a model, close an oversight case, decommission a model) require a confirmation dialog that:
- Restates what will happen in plain language
- Shows the audit trail this action will create
- Requires the user to type a confirmation phrase for the most consequential actions

### 4. Audit Transparency

Every piece of data the user sees should have a "trace" affordance — a way to see where this data came from, who created it, and when. This is the governance UX principle: nothing should feel magic or unexplained.
