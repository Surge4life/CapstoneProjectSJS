# Chapter 10 — Mobile UX

## Mobile-First Thinking

While the G.O.D.S division apps run on desktop browsers as PWAs, they are designed mobile-first. The primary users — learners, employers in the field, investors — frequently access these apps on mobile devices. The administrative interfaces (platform-web, platform-internal) are exceptions that are explicitly desktop-only.

---

## Mobile Breakpoints

```css
/* Breakpoints used across all division apps */
sm:  375px   /* Minimum supported — iPhone SE */
md:  768px   /* Tablet portrait */
lg:  1024px  /* Tablet landscape / small laptop */
xl:  1280px  /* Desktop */
2xl: 1536px  /* Large desktop */
```

All layouts are tested at 375px as the minimum. No horizontal scrolling is permitted on mobile.

---

## Mobile Navigation Pattern

Division apps use a bottom navigation bar on mobile:

```
┌────────────────────────────────────────┐
│                                        │
│           Page Content                 │
│                                        │
├────────┬─────────┬──────────┬──────────┤
│ Home   │Discover │   Apply  │ Profile  │
│  🏠    │   🔍    │    📋    │   👤    │
└────────┴─────────┴──────────┴──────────┘
```

On desktop (≥ 1024px), the bottom navigation is replaced by a left sidebar. This is handled by a single responsive navigation component that adapts to screen size.

---

## Touch Targets

All interactive elements meet WCAG 2.1 AA minimum touch target size:
- Minimum: 44×44px
- Preferred: 48×48px
- Spacing between targets: minimum 8px

This applies to buttons, links, form controls, list items with actions, and icon-only buttons (which must have visible tap affordance).

---

## Mobile-Specific UX Patterns

### Document Upload on Mobile

Mobile users need to photograph paper documents (qualification certificates, ID documents):

```
[Upload Document]
    ↓ Opens action sheet
[Take Photo] | [Choose from Library] | [Browse Files]
    ↓ Takes photo
[Preview + Crop] → [Confirm] → Upload starts
    ↓
[Upload complete — document sealed ✓]
```

The camera integration uses the Capacitor Camera plugin (native app) or `<input accept="image/*" capture="environment">` (PWA).

### Offline Application Drafts

SETHS learners often apply from areas with intermittent connectivity. Applications support offline drafts:

1. Learner starts an application
2. If connectivity drops, draft is saved to IndexedDB
3. Draft indicator shown: "Draft saved offline"
4. When connectivity restores: draft syncs automatically, submission completes
5. Learner notified: "Application submitted successfully"

### Pull-to-Refresh

All list views support pull-to-refresh. The pull gesture triggers a fresh data fetch. Visual feedback: pull indicator appears, spinning on refresh, disappears on complete.

---

## Mobile Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Contentful Paint | < 2s on 3G | Lighthouse |
| Time to Interactive | < 3s on 3G | Lighthouse |
| App size (initial JS) | < 300 KB gzipped | Bundle analysis |
| Image optimisation | WebP, lazy loaded | Manual review |

Code splitting is used throughout: each page is a lazy-loaded chunk. Only the authentication and connect screen code is included in the initial bundle.

---

## PWA Install Experience

On first visit, the browser shows an install prompt after the user has visited the app twice and spent at least 30 seconds:

```
[App Icon] Install SETHS?
           Add to your home screen
[ Not now ]  [ Install ]
```

After installation:
- App icon appears on home screen
- App opens in standalone mode (no browser chrome)
- Status bar colour matches division accent colour
- Splash screen shows during cold start

For Capacitor builds (Android APK / iOS IPA), the native install experience replaces the PWA install prompt.

---

## Gesture Navigation

Division apps support standard mobile gestures:
- Swipe right from left edge: navigate back (mirrors system back)
- Pull down from top: close a sheet/modal
- Swipe list items left: reveal actions (delete, archive)
- Long press on list items: select for bulk actions

Gestures are consistent across all division apps. Once a user learns the gesture system in one app, it transfers.
