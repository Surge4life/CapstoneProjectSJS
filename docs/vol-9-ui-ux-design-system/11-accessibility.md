# Chapter 11 — Accessibility

## Accessibility Standard

All G.O.D.S frontends target **WCAG 2.1 Level AA** compliance as a minimum. This is not a stretch goal — it is a baseline requirement. The G.O.D.S system serves users across diverse contexts, including individuals with visual, motor, cognitive, and hearing impairments.

The SETHS learner portal in particular must be accessible — it serves individuals who may be from disadvantaged backgrounds, who may use older assistive technologies, and for whom this system may represent a significant life opportunity.

---

## Colour Contrast

The navy/gold/white palette meets WCAG 2.1 AA contrast requirements:

| Combination | Contrast Ratio | WCAG AA (Text) | WCAG AA (Large Text) |
|------------|---------------|---------------|----------------------|
| White on Navy (#060E1C) | 16.3:1 | ✓ Pass | ✓ Pass |
| Gold on Navy (#C9A84C on #060E1C) | 5.2:1 | ✓ Pass | ✓ Pass |
| White on Surface (#0D1A2E) | 12.4:1 | ✓ Pass | ✓ Pass |
| Navy on White | 16.3:1 | ✓ Pass | ✓ Pass |

Division accent colours on navy are checked individually and must meet 4.5:1 minimum:
- UDOC Blue (#3B82F6 on navy): 4.7:1 ✓
- SETHS Green (#22C55E on navy): 4.9:1 ✓
- MADIBA Violet (#8B5CF6 on navy): 4.6:1 ✓
- TS Orange (#F97316 on navy): 4.8:1 ✓

---

## Keyboard Navigation

All interactive elements are keyboard accessible:

- **Tab order** follows logical reading order (left to right, top to bottom)
- **Visible focus ring** — all focused elements have a clearly visible gold outline (2px, 2px offset)
- **Skip link** — "Skip to main content" visible on first Tab press (helps screen reader users)
- **Modal trapping** — when a modal/dialog opens, focus is trapped within it until closed
- **Escape key** — closes all modals, drawers, and dropdowns
- **Arrow keys** — navigate within menus, tab panels, and data tables

---

## Screen Reader Support

All components are tested with NVDA (Windows) and VoiceOver (macOS/iOS):

| Element | ARIA Implementation |
|---------|-------------------|
| Navigation | `<nav aria-label="Main navigation">` |
| Page headings | Proper `<h1>` → `<h6>` hierarchy, one `<h1>` per page |
| Buttons | Descriptive `aria-label` on icon-only buttons |
| Status indicators | `role="status"` for live notifications; `aria-live="polite"` |
| Forms | `<label>` for every input; `aria-describedby` for error messages |
| Tables | `<caption>` for every table; `scope` on `<th>` elements |
| Modals | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Loading states | `aria-busy="true"` on loading regions |
| EVA score chart | Text alternative describing scores (for chart components) |
| Governance badges | Text content (not just colour) conveys meaning |

---

## Colour-Independent Design

Governance outcomes are never conveyed by colour alone:

```
✓ APPROVE  (checkmark + text + green — three signals)
⏳ REVIEW  (clock icon + text + amber)
↑ ESCALATE (arrow icon + text + orange)
✗ BLOCK    (x icon + text + red)
```

Similarly, EVA score bars include the numeric score in addition to the colour indicator.

---

## Cognitive Accessibility

The G.O.D.S system uses complex governance terminology. Cognitive accessibility measures:

1. **Plain language** for user-facing messages — governance outcomes are explained in plain language, not just codes
2. **Consistent navigation** — the same actions are always in the same place
3. **Error prevention** — confirmations before destructive actions; clear error messages that describe what went wrong and how to fix it
4. **Progressive disclosure** — technical detail (EVA scores, audit seals) is available on demand, not mandatory to read
5. **Reading level** — user-facing text targets Grade 8 reading level (Flesch-Kincaid)

---

## Automated Accessibility Testing

Automated testing is integrated into the CI pipeline:

```bash
# Run axe-core accessibility tests against built app
npm run test:a11y

# Test with cypress + axe
cy.checkA11y({
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa']
  }
})
```

Automated tests catch approximately 30–40% of accessibility issues. Manual testing with screen readers is required before major releases.

---

## Accessibility Statement

Each deployed G.O.D.S application includes an accessibility statement accessible from the footer:
- Which standard we target (WCAG 2.1 AA)
- Known exceptions (with planned fix dates)
- How to report accessibility issues
- Alternative access methods (if applicable)
