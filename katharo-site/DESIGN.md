---
name: Katharo Cleaning
description: The caretaker's lobby of an interwar Bucharest apartment building, kept immaculate, in black lacquer with gold and cream with bronze.
colors:
  lacquer: "#100d0a"
  lacquer-2: "#1a150f"
  lacquer-line: "#34291b"
  on-lacquer: "#efe5d4"
  on-lacquer-muted: "#b3a48d"
  gold: "#cda45e"
  gold-hi: "#e9cf96"
  gold-deep: "#9a7334"
  brass-frame: "#b48a46"
  brass-hairline: "#6e5328"
  cream: "#f1e6d6"
  cream-2: "#e6d6c0"
  bronze: "#85602c"
  bronze-ink: "#3a2a14"
  engraved-ink: "#281a0c"
typography:
  display:
    fontFamily: "Josefin Sans, Work Sans, system-ui, sans-serif"
    fontSize: "48px"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "0.06em"
  headline:
    fontFamily: "Work Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "2.95cqw"
    fontWeight: 460
    lineHeight: 1.12
    letterSpacing: "0.01em"
  signage:
    fontFamily: "Josefin Sans, Work Sans, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "0.1em"
  title:
    fontFamily: "Josefin Sans, Work Sans, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "0.06em"
  numeral:
    fontFamily: "Josefin Sans, Work Sans, system-ui, sans-serif"
    fontSize: "56px"
    fontWeight: 300
    lineHeight: 1
    fontFeature: "lnum"
  body:
    fontFamily: "Work Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  body-lead:
    fontFamily: "Work Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Work Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.02em"
rounded:
  frame: "3px"
  field: "4px"
  note: "6px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "48px"
  xl: "64px"
  section: "96px"
  gutter: "24px"
  container: "1240px"
components:
  button-primary:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.lacquer}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "13px 26px"
  button-primary-hover:
    backgroundColor: "{colors.gold-hi}"
    textColor: "{colors.lacquer}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.on-lacquer}"
    rounded: "{rounded.pill}"
    padding: "0 16px"
    height: "40px"
  button-outline-hover:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.lacquer}"
  button-intercom:
    backgroundColor: "#2a1c0c"
    textColor: "{colors.gold-hi}"
    rounded: "{rounded.pill}"
    height: "50px"
  input:
    backgroundColor: "{colors.lacquer}"
    textColor: "{colors.on-lacquer}"
    rounded: "{rounded.field}"
    padding: "12px 14px"
  brass-panel:
    backgroundColor: "{colors.lacquer-2}"
    textColor: "{colors.on-lacquer}"
    rounded: "{rounded.frame}"
    padding: "40px"
  directory-board:
    backgroundColor: "#120f0b"
    textColor: "{colors.gold-hi}"
    rounded: "{rounded.frame}"
    padding: "40px 44px 28px"
  cream-room:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.bronze-ink}"
    padding: "96px 0"
---

# Design System: Katharo Cleaning

## Overview

**Creative North Star: "The Caretaker's Lobby"**

Katharo is the caretaker of a fine interwar Bucharest apartment building, and the site is that building's entrance and lobby, kept spotless. Every piece of interface is an object you would find there: the quote starter is the brass intercom beside the door, the house rules are set into the terrazzo floor, the services are names on the lobby's tenant directory board, and the full quote form is the concierge desk. The visitor scrolls, the double doors swing open, the view walks into the lobby, and the page continues inside.

The world is built from two colourways and nothing else: black lacquer with polished logo gold for the dark rooms, warm cream with bronze for the light rooms. Materials carry the mood: lacquer walls, brass trim with a double frame line, cream terrazzo with bronze and black chips, frosted glass in the doors. Density is calm and roomy; sections breathe at 96px and type is set large and sparingly. Josefin Sans supplies the geometric Deco lettering of a building's signage; Work Sans does all the reading.

As built, the first viewport is the entrance (door surround, frosted-glass headline, intercom, terrazzo floor with the rules) and the tenant directory board appears once you are inside the lobby. This differs from the direction contract, which placed the directory board in the first viewport; the build is the record.

**Key Characteristics:**
- Diegetic interface: controls live on building objects (intercom, floor plaque, directory board, concierge desk).
- Two colourways only: lacquer + gold, cream + bronze.
- Brass-framed lacquer panels with a 3px brass border and an inset hairline.
- Josefin Sans for building lettering, Work Sans for reading.
- Scroll-driven entrance: doors open, then the view moves into the lobby.
- Generated illustration plates and one photographic lobby plate, used as atmosphere only.

## Colors

A warm, near-monochrome palette of lacquer blacks, brass golds and terrazzo creams; every value sits on the same 60 to 75 degree warm hue.

### Primary
- **Logo Gold** (`gold`): the brand gold of the K mark. Primary button fill, logo colour, outline-button border, focus ring family, the sparkle in every deco rule on dark, `::selection`.
- **Lit Brass** (`gold-hi`): the highlight of polished brass. Headings on lacquer (desk, board title, legal pages), links on lacquer, primary button hover, the global focus outline.
- **Shadowed Brass** (`gold-deep`): brass in shade. Scrollbar thumb; reserved for brass in low light.
- **Brass Frame** (`brass-frame`): the 3px outer border of every framed lacquer panel (directory board, step plaques, concierge desk, phone quote bar).
- **Brass Hairline** (`brass-hairline`): the inner 1px line of the double frame, and the rule under the directory board's header.

### Secondary
- **Terrazzo Cream** (`cream`): the light rooms (How we work, FAQ). Also the frosted-glass wash behind the hero headline.
- **Cream Shadow** (`cream-2`): the second cream step for tonal layering on light rooms.
- **Bronze** (`bronze`): the accent on cream. Deco rules on cream, FAQ plus/minus, FAQ hover text.
- **Bronze Ink** (`bronze-ink`): body text on cream; the frosted-glass copy and hero rule.
- **Engraved Ink** (`engraved-ink`): the darkest bronze, for Deco headings set on cream and on the terrazzo floor, as if cut into stone.

### Neutral
- **Black Lacquer** (`lacquer`): the page ground, header, concierge desk section, field backgrounds.
- **Raised Lacquer** (`lacquer-2`): the concierge desk panel surface, one step up from the ground.
- **Lacquer Seam** (`lacquer-line`): section borders and the footer top line on dark.
- **Lamplit Cream** (`on-lacquer`): primary text on lacquer.
- **Aged Cream** (`on-lacquer-muted`): secondary text on lacquer (descriptions, form hints, footer links, legal body).

### Named Rules
**The Two Colourways Rule.** Black lacquer with logo gold, or cream with bronze. No other hue enters the system; the owner pinned this. Gold belongs to dark rooms and bronze to cream rooms.

**The Lit Brass Rule.** On lacquer, headings and links take `gold-hi`, never flat `gold`; flat `gold` is for fills, borders, the logo and small stars.

## Typography

**Display Font:** Josefin Sans (with Work Sans, system-ui), self-hosted, weights 300 to 600.
**Body Font:** Work Sans (with Segoe UI, system-ui), self-hosted, weights 300 to 700.

**Character:** Josefin Sans is the geometric Deco lettering of a 1930s building's brass name and directory; Work Sans is the quiet, even reading voice of the caretaker. The pairing stays in one sans family of feeling, so the Deco face reads as material rather than costume.

### Hierarchy
- **Display** (Josefin 400, 48px, 1.1, +0.06em; 34px under 760px): section names on cream and at the desk ("Cum lucrăm", "Întrebări", "Solicită o ofertă").
- **Headline** (Work Sans 460, 2.95cqw of the entrance frame, 1.12, +0.01em): the one sentence-length headline, set on the frosted door glass in Bronze Ink.
- **Signage** (Josefin 400, 20px, 1.3, +0.1em, uppercase): tenant names on the directory board. The board's own title runs at 40px, +0.14em, uppercase.
- **Title** (Josefin 400, 22px, 1.25, +0.06em): step plaque headings.
- **Numeral** (Josefin 300, 56px, 1, lining figures): step numbers in gold.
- **Body** (Work Sans 400, 17px, 1.6): all reading text, about 62ch at most in the FAQ, 30 to 34ch in intros.
- **Body Lead** (Work Sans 400, 19 to 20px, 1.5): section intros and the lobby note.
- **Label** (Work Sans 600, 14px, +0.02em): form labels; optional markers drop to 400 in Aged Cream.

### Named Rules
**The Lettering Rule.** Josefin Sans is building lettering: section names, directory entries, numerals, the rules title. Anything read as a sentence (the hero headline, body, labels, buttons, FAQ questions) is Work Sans.

## Layout

Two layout modes coexist. The entrance is a fixed composition: a single frame with the aspect ratio of the plates (2688 / 1520), sized to cover the viewport (`--fw`), with every object (doors, glass copy, intercom, rules) placed in percentages and `cqw` of that frame so they stay registered to the illustration. The header's logo, links and CTA are positioned the same way, on the door lintel. Below the entrance the page is a conventional flow: a 1240px container with 24px gutters (respecting safe-area insets), two-column grids (0.7/1.3 for FAQ, 0.8/1.2 for the desk, 640px board plus note in the lobby) and a three-up step row.

Vertical rhythm: rooms are padded 96px (lobby 120/96, desk 112), dropping to 64px on phones. Internal gaps step through 8, 16, 24, 48 and 64px.

Responsive: at 900px and below, all two- and three-column grids collapse to one column. At 760px and below, the header becomes a 64px bar with logo and CTA only, the entrance frame is cropped to the doors (frame width 214vw), the in-frame intercom and floor rules are hidden and replaced by a docked quote bar at the foot of the entrance, then a full intercom and a stacked rules list on terrazzo below it.

## Elevation & Depth

Depth is material, not floating cards. Lacquer panels sit in brass frames and cast one long, soft shadow, as a heavy object on a wall would. Cream rooms are flat, with depth from the terrazzo texture under a 55% cream wash. The header is transparent over the lintel and turns solid lacquer (92%, 8px blur) with a soft drop once scrolled.

### Shadow Vocabulary
- **Brass frame** (`box-shadow: inset 0 0 0 6px <panel>, inset 0 0 0 7px #6e5328, 0 30px 60px -20px rgba(0,0,0,0.8)`): the double brass frame plus hanging shadow, on the directory board and desk (desk shadow `-24px`, `0.7`).
- **Plaque on terrazzo** (`inset 0 0 0 5px #15110b, inset 0 0 0 6px #6e5328, 0 18px 36px -18px rgba(40,26,8,0.6)`): step plaques on cream, a warmer, shorter shadow.
- **Header solid** (`0 8px 24px -12px rgba(0,0,0,0.6)`): only once the page has scrolled.
- **Field focus** (`0 0 0 3px rgba(205,164,94,0.2)`): a soft gold halo on focused fields.

### Named Rules
**The Brass Frame Rule.** A framed panel is a 3px Brass Frame border, a 5 to 6px gap in the panel's own colour, then a 1px Brass Hairline, at 3px corners. Never a single thin border, never a rounded card.

## Shapes

Architectural and mostly square: framed panels at 3px corners, fields at 4px, notes at 6px. Pills (999px) are reserved for buttons, echoing brass push plates. Circles appear as the rule medallions (a dark ring with an inner light hairline around a line icon) and the brass rivets at the top corners of step plaques. Dividers are the deco rule: a hairline, a four-point sparkle from the logo, a hairline.

## Components

### Buttons
Brass hardware, confident and tactile.
- **Shape:** full pill (999px).
- **Primary (concierge desk send):** Logo Gold fill, lacquer text, 600 weight, 13px 26px padding, trailing arrow icon; hover lifts to Lit Brass; active presses down 1px; disabled at 60% opacity.
- **Outline (header CTA "Solicită o ofertă"):** 1px gold border, cream text, transparent; hover fills gold with lacquer text.
- **Intercom call ("Cere oferta fixă"):** dark bronze (#2a1c0c) fill, gold text, a gold ring border plus an outer dark ring and a faint top highlight, phone glyph in gold; hover warms the fill to #3a2911; active presses 1px.
- **Transitions:** colour 300ms, press 150ms, on the house ease-out.

### Intercom (signature component)
The working quote starter, drawn as a brass building intercom plate. Five radio rows, each a generated brass push button plus a label ("Locuință", "Apartament", "Birou", "Depozit", "După renovare"); the area field is a recessed bronze well with light text; the call button sits at the foot. Hover grows a button 4%; a checked button presses in to 90% with a warm glow and its label goes bold and underlined. Submitting carries the choices down to the concierge desk form and focuses the name field. All type on the plate is engraved ink on brass.

### Directory Board (signature component)
The services list, as a lobby tenant board: near-black felt with faint horizontal ruling, Brass Frame, a Josefin uppercase title in Lit Brass, a "Locatari" header strip in tracked gold caps ruled off with a Brass Hairline, then rows of a gold sparkle plus a Josefin uppercase tenant name and a Work Sans description, divided by dark brass lines.

### Cards / Containers (step plaques, concierge desk)
- **Corner Style:** 3px.
- **Background:** lacquer (#15110b plaques, Raised Lacquer desk).
- **Shadow Strategy:** Brass frame or Plaque on terrazzo (see Elevation).
- **Border:** the double brass frame; step plaques add two brass rivets at the top corners.
- **Internal Padding:** 36px 32px 32px plaques, 40px desk (22px on phones).

### Inputs / Fields
- **Style:** lacquer ground, 1px dark brass stroke (#4a3a22), 4px radius, 12px 14px padding, Lamplit Cream text, gold caret.
- **Focus:** border turns Logo Gold with a 3px gold halo at 20%.
- **Error:** the build marks invalid fields with a terracotta border and message text; that colour is outside the colourways and is not a system token (see Do's and Don'ts).
- **Labels:** Label style above the field; optional parts in Aged Cream at 400.

### Navigation
Work Sans 500, about 13 to 14px, in warm cream (#eadfca) on the door lintel, no underline; hover turns Lit Brass over 300ms. The outline CTA sits at the right. Under 760px the links are hidden and the bar keeps only the logo and the CTA. The footer repeats the links in Aged Cream at 15px, hovering to Lamplit Cream.

### House Rules Medallions
Each rule is a circular medallion (dark ring, inner light hairline, line icon at 55%) above a short Work Sans 500 label, set into the terrazzo floor and separated by thin bronze verticals. On phones they become a list: 52px medallion, bold label, small description, bronze hairline between rows.

### FAQ Disclosure
Native details/summary on cream, rows ruled with a pale bronze line (#cdb795). Questions are Work Sans 500 at 21px (18px on phones); the plus/minus is drawn in Bronze and rotates closed over 400ms. Answers are Body in a softened bronze, 62ch.

### Deco Rule
Hairline, logo sparkle, hairline. Bronze on cream, gold on lacquer, Bronze Ink on glass and floor. Sits under section names, 320px wide or 70% at most.

### Motion
- **Easing:** one house curve, `cubic-bezier(0.16, 1, 0.3, 1)`, for every state change; the scroll choreography uses a cubic ease-out in script.
- **Entrance:** over a 210vh pinned track (160vh on phones), the doors swing open on hinges to 78 degrees and dim by 45% during the first 55% of the scroll while the lobby plate behind settles from 112% to 100%; from 45% the whole frame scales up to 2.3x into the door opening; the glass copy fades out as the doors start to move.
- **Reduced motion:** the track is unpinned, the doors stay closed, and all transitions collapse to 1ms.

## Do's and Don'ts

### Do:
- **Do** keep every colour inside the two colourways: lacquer + gold, cream + bronze.
- **Do** put interface on building objects (intercom, floor plaque, directory board, concierge desk) when a new surface needs controls.
- **Do** frame lacquer panels with the double brass frame (3px Brass Frame, inset gap, 1px Brass Hairline, 3px corners).
- **Do** set section names, directory entries and numerals in Josefin Sans, and everything read as a sentence in Work Sans.
- **Do** use generated plates as atmosphere only: decorative (`alt=""`), uncaptioned, and carrying their generation prompt in the file's `impeccable:prompt` metadata.
- **Do** separate sections with the deco rule (hairline, logo sparkle, hairline) in the room's accent colour.
- **Do** use the house ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) and honour reduced motion with a static, closed entrance.

### Don't:
- **Don't** present generated imagery as real client work, real staff, real premises, or before/after proof; no captions, names or locations on plates.
- **Don't** add a hue outside the colourways, including blues, greens or a separate red.
- **Don't** use flat gold for text on lacquer; headings and links take Lit Brass.
- **Don't** lift the directory board's tracked-caps header strip into a general label above section headings; it belongs to the board.
- **Don't** replace the brass frame with a soft rounded card or a lone 1px border.
