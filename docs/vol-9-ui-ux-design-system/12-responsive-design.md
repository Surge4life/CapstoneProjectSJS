# Chapter 12 — Responsive Design

## Responsive Design Strategy

G.O.D.S frontends use a **mobile-first, progressive enhancement** approach. The base CSS targets mobile screens; larger screens progressively unlock richer layouts.

This is not just a technical choice. It reflects the reality of the user base: learners on SETHS, employers in the field, and investors travelling use mobile devices as their primary access point.

---

## Layout System

All layouts use CSS Grid and Flexbox via Tailwind CSS. The grid system:

```css
/* Default: 4-column grid on mobile */
.gods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

/* 8 columns on tablet (md:) */
@media (min-width: 768px) {
  .gods-grid { grid-template-columns: repeat(8, 1fr); }
}

/* 12 columns on desktop (lg:) */
@media (min-width: 1024px) {
  .gods-grid { grid-template-columns: repeat(12, 1fr); }
}
```

Components declare their column spans at each breakpoint:

```tsx
<div className="col-span-4 md:col-span-8 lg:col-span-6">
  {/* Full width on mobile, full tablet, half desktop */}
</div>
```

---

## Layout Transformations by Screen Size

### Navigation

| Screen | Layout |
|--------|--------|
| Mobile (< 1024px) | Bottom tab bar (4 tabs) |
| Tablet (768–1023px) | Bottom tab bar (5 tabs, wider) |
| Desktop (≥ 1024px) | Left sidebar (collapsible) |

### Data Tables

| Screen | Layout |
|--------|--------|
| Mobile | Card list (one row per card, key fields only) |
| Tablet | Horizontal scroll table (pinned first column) |
| Desktop | Full table with all columns |

### Forms

| Screen | Layout |
|--------|--------|
| Mobile | Single-column, full-width fields |
| Tablet | Two-column for short fields |
| Desktop | Two or three-column layout |

### Dashboard Widgets

| Screen | Layout |
|--------|--------|
| Mobile | Stacked single column |
| Tablet | 2×2 grid |
| Desktop | 4-column or custom dashboard grid |

---

## Specific Responsive Rules

### The Kanban Board (SETHS Employer)

The full kanban (5 columns) cannot fit on mobile. Mobile shows:
- Single-column view with status filter dropdown
- "Column" header shows current filter
- Swipe left/right to navigate between columns

On tablet: 2–3 columns visible, horizontal scroll for the rest.
On desktop: all 5 columns visible side by side.

### The EVA Score Chart

On mobile: compact bar list (horizontal bars, all 6 dimensions + overall)
On desktop: hexagonal radar chart

Both views show the same data. The chart is a visual enhancement for larger screens, not a replacement for the data.

### The Decision Inspector

On mobile: stacked layout — EVA scores → reasoning → audit info → actions
On desktop: two-column — EVA chart left, reasoning + audit right

---

## Images and Media

**Hero images:** Served at multiple resolutions using `srcset`. The smallest version is loaded on mobile:
```html
<img
  src="hero-800.webp"
  srcset="hero-800.webp 800w, hero-1200.webp 1200w, hero-1600.webp 1600w"
  sizes="(max-width: 800px) 100vw, 800px"
  alt="Description"
  loading="lazy"
/>
```

**Icons:** SVG throughout — scale perfectly at all sizes with no quality loss.

**Brand logo:** SVG for all screen sizes.

---

## Responsive Testing Checklist

Before any release, test at these viewports:

| Device | Width | Notes |
|--------|-------|-------|
| iPhone SE | 375px | Minimum supported |
| iPhone 14 Pro | 393px | Most common iPhone |
| Samsung Galaxy S21 | 360px | Common Android |
| iPad | 768px | Tablet portrait |
| iPad Pro | 1024px | Tablet landscape |
| Laptop | 1280px | Standard laptop |
| Desktop | 1440px | Common desktop |
| Large desktop | 1920px | Wide screen |

Testing is done with real devices for the mobile breakpoints and browser DevTools for laptop/desktop.

---

## Print Styles

Governance reports and audit records can be printed directly from the browser. Print styles:
- Hide navigation, sidebars, action buttons
- Show full page width
- Include G.O.D.S entity notation and page numbers
- Expand all collapsed sections
- Show governance seals/references that may be visually hidden in the UI
