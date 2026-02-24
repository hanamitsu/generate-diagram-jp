# Method Diagram Aesthetics Guide

## 1. The Look

The system supports three style modes on a spectrum from academic to graphic recording:

| Mode | Concept | Use Case |
| --- | --- | --- |
| **academic** | Minimal Structure, Friendly Icons | Paper submissions, conference presentations |
| **balanced** (default) | Structured Graphic Note | Tech blogs, presentations, explainer articles |
| **graphic-note** | Visual Graphic Recording | Social media, internal docs, concept overviews |

All modes share the same spatial composition rules (Section E). The modes
differ in color usage, line treatment, decoration, and icon style.

---

## 2. Detailed Style Options

### **A. Color Palettes**

**academic mode:**
* Pure white background. No colored zone fills.
* Boxes: white fill with thin dark grey borders only. No pastel fills.
* The ONLY color comes from icons and pictograms.

**balanced mode:**
* White or very light cream background.
* Boxes use soft-tone colorful fills (soft sky blue, soft peach, soft mint,
  soft lavender, soft warm yellow). Use 4–5 colors for visual rhythm.
* Lines and arrows: hand-drawn style, bold strokes with natural waviness.

**graphic-note mode:**
* White or very light cream background.
* Boxes use soft-tone colorful fills (soft sky blue, soft peach, soft mint,
  soft lavender, soft warm yellow). Use 4–5 colors for visual rhythm.
* Lines and arrows: hand-drawn style, bold strokes with natural waviness.

### **B. Shapes & Containers**

*Design Philosophy: Clean geometry, generous padding.*

* **Process Nodes:** Rounded rectangles with generous internal padding.
  - academic: white fill, thin dark grey border.
  - balanced: soft-tone colorful fill, hand-drawn style dark grey border.
  - graphic-note: soft-tone colorful fill, hand-drawn style border.
* **Grouping:** Thin dashed dark grey borders on white background (all modes).
  In balanced and graphic-note modes, may also use light colored background regions.

### **C. Lines & Arrows**

* academic: Thin dark grey or black. Small subtle arrow heads.
  Curved/Bezier preferred. No colored lines.
* balanced: Hand-drawn style bold strokes with natural waviness.
  Arrow heads are prominent. Flow emphasis through line weight variation.
* graphic-note: Hand-drawn style bold strokes. Arrow heads are prominent
  and expressive. Flow emphasis through line weight variation.
* All modes: Dashed lines for auxiliary/secondary flows.

### **D. Typography & Icons**

**Typography**
* academic: Clean sans-serif (Noto Sans JP, Arial, Helvetica).
  Bold for headers, Regular for details.
* balanced: Hand-written style rounded font feel. Headings are pop
  and bold, details are readable regular.
* graphic-note: Hand-written style rounded font feel. Headings are pop
  and bold, details are readable regular.
* All modes: Text color is black or very dark grey only.

**Icons & Pictograms**
* All modes use **soft pastel color fills** for icons — warm, friendly style.
* academic: 2D vector style, moderate size, neatly detailed.
* balanced: Hand-drawn illustration style, large, visually prominent.
  No characters or mascots. Icons limited to abstract pictograms
  (gears, folders, shields, stars, etc.).
* graphic-note: Hand-drawn illustration style, large, visually dominant.
  No characters or mascots by default. Only when explicitly requested
  by the user may cute deformed characters (robots, animal mascots) be used.
* All modes: Icons anchor to the left of or above their label. Never floating.

### **D2. Decoration Elements**

*Only in balanced and graphic-note modes.*

* **Banner headings:** Ribbon-banner or flag-style labels for phase titles.
  - balanced: hand-drawn ribbon banners or flag-style headings.
  - graphic-note: hand-drawn ribbon banners or flag-style headings.
* **Speech bubbles:** Hand-drawn style callouts for annotations.
  - balanced: used for key annotations, various shapes (round, cloud, etc.).
  - graphic-note: freely used, various shapes (round, cloud, etc.).
* **Marker highlights:** Marker-pen style background on key terms.
  - balanced: multiple highlights in soft yellow, soft pink markers.
  - graphic-note: multiple highlights in soft yellow, soft pink, soft green.
* **Numbered steps:** Hand-drawn circled numbers (balanced and graphic-note).
* **Decorative dividers:** Wavy or hand-drawn separator lines (graphic-note only).

### **E. Layout & Composition**

*Design Philosophy: The diagram must read like a well-designed poster.
These rules apply to ALL modes.*

* **Flow direction:** Left-to-right or top-to-bottom. Pick one and
  commit. Never mix flows in the same diagram.
* **Generous whitespace** — the gap between groups should be noticeably
  wider than the gap between items within a group.
* **Grid alignment:** All elements must snap to an implicit grid.
* **Balance:** Distribute visual weight evenly across the canvas.
* **Element count:** Prefer fewer, larger boxes over many small ones.
* **Spatial hierarchy:** The most important concept occupies the
  largest area or the most central position.
* **Readability at a glance:** Main flow understood within two seconds.
* **Consistent sizing:** Boxes at the same logical level should be
  the same width and height.
* **Icon placement:** Place icons to the left of or above their
  associated label, never floating.

---

## 3. Common Pitfalls (What to Avoid)

* **Heavy outlines** — Keep all strokes appropriately weighted for the mode.
* **Dense layouts** — When in doubt, add more whitespace.
* **Too many elements** — Simplify and consolidate.
* **Uneven box sizes** — Boxes at the same level must match in size.
* **Ambiguous flow** — If the viewer cannot trace the main path in
  two seconds, the layout has failed.
* **Floating icons** — Every icon must be anchored next to its label.
* **Excessive colors** — Even in graphic-note mode, limit to 4–5 soft tones.
  Avoid saturated or clashing colors.
* **Mode inconsistency** — Don't mix academic monochrome structure with
  graphic-note decorations. Stay within the chosen mode.
* **Dull monochrome icons** — Icons must have soft pastel color fills in all modes.

---

## 4. Summary Rule

**All modes share structured spatial composition. They differ in visual warmth:**
- **academic:** Monochrome structure + pastel icons only.
- **balanced:** Colorful soft-tone structure + hand-drawn touch + rich decorations (no characters).
- **graphic-note:** Colorful soft-tone structure + hand-drawn touch + rich decorations (characters only on request).
