# Chapter 02 — Component Library

## Design System Foundation

All G.O.D.S frontends share a component library built on the design tokens defined in Chapter 01. Components are implemented in React + TypeScript and styled with Tailwind CSS using the custom theme.

---

## Design Tokens (Quick Reference)

```css
/* Root tokens */
--color-navy:    #060E1C;   /* Primary background */
--color-gold:    #C9A84C;   /* Primary accent */
--color-white:   #FFFFFF;
--color-surface: #0D1A2E;   /* Card / panel background */
--color-border:  rgba(201,168,76,0.2);  /* Subtle gold border */

/* Division accents */
--color-udoc:    #3B82F6;   /* Blue */
--color-seths:   #22C55E;   /* Green */
--color-madiba:  #8B5CF6;   /* Violet */
--color-ts:      #F97316;   /* Orange */

/* Semantic */
--color-success: #22C55E;
--color-warning: #F59E0B;
--color-error:   #EF4444;
--color-info:    #3B82F6;

/* Typography */
--font-sans:     'Inter', system-ui, sans-serif;
--font-mono:     'JetBrains Mono', monospace;
```

---

## Core Components

### `<GodsButton />`

```tsx
interface GodsButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  icon?: ReactNode;
  children: ReactNode;
  onClick?: () => void;
}
```

**Variants:**
- `primary` — Gold background, navy text. Use for the single most important action.
- `secondary` — Gold border, transparent background, gold text.
- `ghost` — No border, muted text. Use for secondary actions.
- `danger` — Red background. Use for destructive actions with confirmation.

**Loading state:** Button shows a spinner and is disabled while `loading=true`.

---

### `<GovernanceBadge />`

Displays a governance outcome with appropriate colour coding.

```tsx
interface GovernanceBadgeProps {
  outcome: 'APPROVE' | 'REVIEW' | 'ESCALATE' | 'BLOCK' | 'PENDING';
  size?: 'sm' | 'md';
  showIcon?: boolean;
}
```

| Outcome | Colour | Icon |
|---------|--------|------|
| APPROVE | Green | ✓ |
| REVIEW | Amber | ⏳ |
| ESCALATE | Orange | ↑ |
| BLOCK | Red | ✗ |
| PENDING | Grey | ○ |

---

### `<EVAScoreCard />`

Displays the 6-dimensional EVA score breakdown.

```tsx
interface EVAScoreCardProps {
  scores: {
    ec: number; si: number; rc: number;
    fa: number; cc: number; sc: number; overall: number;
  };
  compact?: boolean;
  showLabels?: boolean;
}
```

Renders a hexagonal radar chart in compact mode, or a full dimension-by-dimension bar display in full mode. Each bar is colour-coded: green ≥ 80, amber 60–79, red < 60. Hard-block thresholds (FA < 40, RC < 35, SC < 30) are visually marked.

---

### `<AuditTrailItem />`

Single audit event display for timeline views.

```tsx
interface AuditTrailItemProps {
  event: AuditRecord;
  showDetails?: boolean;
}
```

Renders: event type (formatted), actor avatar + name, timestamp (relative + absolute on hover), expandable details panel.

---

### `<GodsDataTable />`

Feature-rich data table for administrative views.

```tsx
interface GodsDataTableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  loading?: boolean;
  pagination?: PaginationConfig;
  sorting?: SortingConfig;
  filtering?: FilterConfig;
  rowSelection?: RowSelectionConfig;
  onRowClick?: (row: T) => void;
}
```

Features: column sorting, multi-column filtering, pagination, row selection (for bulk actions), keyboard navigation, loading skeleton.

---

### `<ConnectScreen />`

The backend URL configuration screen shown on first launch of division apps.

```tsx
interface ConnectScreenProps {
  appName: string;
  division: 'udoc' | 'seths' | 'madiba' | 'ts';
  onConnect: (backendUrl: string) => void;
}
```

Shows: app logo, division accent colour, URL input with validation, connection test on submit (calls `/health` to verify), saves to localStorage on success.

---

### `<ConfidenceBadge />`

Displays an intelligence confidence tier.

```tsx
interface ConfidenceBadgeProps {
  tier: 'HIGH' | 'MEDIUM' | 'LOW' | 'INSUFFICIENT';
  score?: number;
  showScore?: boolean;
}
```

---

### `<GodsNotificationPanel />`

In-app notification feed (right-side drawer).

- Groups notifications by day
- Unread notifications highlighted
- Priority `critical` notifications shown with pulsing red indicator
- Action URL opens relevant record
- Mark all as read button

---

## Component Usage Rules

1. **Never hardcode colours** — always use design tokens or Tailwind theme classes
2. **Loading states are required** — every component that fetches data must handle the loading state
3. **Error states are required** — show a meaningful error state, not a blank component
4. **Empty states are required** — show a meaningful empty state with a call to action
5. **Responsive by default** — all components must work on mobile (375px) through desktop (1920px)
6. **Accessibility** — all interactive components must have ARIA labels; all images must have alt text; focus management must be correct
