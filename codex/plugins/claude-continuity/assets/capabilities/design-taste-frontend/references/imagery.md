# Imagery

Detail for SKILL.md §6.6. Adapted from Leonxlnx/taste-skill v2.1.5 `references/imagery.md` (MIT,
(c) 2026 Leonxlnx); the upstream search script is not used here.

## 1. Decide what imagery exists

Find out what is real before planning any slot. In order of preference:

1. **The project's own images.** Product shots, real screenshots, the place, the people, the work. Even
   ordinary photographs of the real thing beat beautiful photographs of something else. Look in the
   repository and ask.
2. **Images you can generate** with an image tool in this session. Write prompts as a photographer's
   brief: subject, angle, light, background, crop ratio, "no text". Generate the hero first and make the
   rest match its light.
3. **Real pictures of the subject's world from open collections** (section 2): its city and street in
   old photographs, maps, its materials, its trade in engravings, museum objects of its kind. Honest
   means nobody could take it for the client's own product, room, dish, person or team.
4. **Pictures drawn in code from the subject itself** (section 5), for what no honest picture exists of.
   In testing, pages that drew their subject with care beat pages that borrowed unrelated photographs
   every time, and beat pages that showed nothing.
5. **Type and colour alone,** done on purpose (section 6).

Never a random placeholder-photo service, never a grey box or "image here", never a photograph of
something else standing in for the subject.

## 2. Real pictures from open collections

No API key is needed. Both endpoints answer directly (checked 2026-11):

```bash
# Openverse (Flickr, Wikimedia, museums, libraries); license_type=commercial keeps CC0, PDM, BY, BY-SA
curl -s 'https://api.openverse.org/v1/images/?q=azulejo&license_type=commercial&page_size=20'
# Wikimedia Commons file search with URL, size, licence and author
curl -s 'https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrsearch=lisbon%20old%20map&gsrlimit=20&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=LicenseShortName|Artist'
```

**What to search for.** The inventory (SKILL.md §0.B), not the category: "bakery" finds other
people's bakeries. Search its place (old postcards, aerial photographs), its maps, its materials close
up, its trade's history (engravings, patent drawings), museum objects of its kind, scientific plates.
Use the place's own words (azulejo, not "blue tile"), add a medium or a decade, try two or three
queries per idea.

**What makes a good find.** It belongs to this subject's world and would not fit the nearest
competitor's page; it reads at the crop the slot needs (look at the file, a title is not a picture);
it is about twice as wide as it is shown; it belongs to one family with the other pictures (all
engravings, or all photographs of one era); no watermark, burned-in text, scanner edge, or
recognisable living person who could pass for staff or customers.

If two or three honest queries per idea find nothing, draw (section 5). If no source can be reached,
draw, and say so in the report.

## 3. Stay honest: licences, credits, files

- **A found picture is never the client's own.** It may show the client's city, materials, history
  or the kind of thing it makes; never its product, room, dish, person, team or customers.
- **Licences:** CC0, public domain, CC BY, CC BY-SA only. No NC or ND for a client's site. CC BY-SA:
  an altered version must be shared under the same licence.
- **Download, do not hotlink.** Save each picture into the project's assets at the width it needs.
- **Credit every picture** in one line in the footer (title, creator, licence link, source link), at
  body size and full contrast. Captions say what the picture is, as the archive describes it; never a
  caption that ties it to the client, never a sentence about where the pictures come from.
- **List them in the report:** file, title, creator, licence, source page, where the credit sits.

## 4. Showing software

- Build a real fragment of the interface in HTML at its true size, with believable content, instead of
  a shrunken screenshot or a mock-up of grey bars. Crop to the part that makes the point: one control,
  one row, one panel.
- Believable means real labels, numbers that add up, one item hovered or selected, proper alignment.
  The data inside a fragment is sample data; say so in the report.
- Put the fragment directly on the page or on one flat stage colour. No laptop or browser frame; a
  phone app may sit in a plain rounded rectangle.
- Inside a fragment the product's own conventions apply (its small radii, 1px control borders, a
  shadow on an open menu). The page around it keeps the page's rules.
- If the user supplies real screenshots, show them large and uncropped at least once.

## 5. Drawing the subject

- **Draw the subject's own things,** not decoration: the stool's three legs and the grain of its seat,
  the sign over the door, the invoice the tool produces, the festival's stage. If you cannot name what
  a drawing depicts in the subject's world, it is decoration; cut it.
- **One graphic language:** flat filled shapes, no outlines or one consistent stroke weight, one curve
  vocabulary, drawn in the palette's real colours at full strength, never grey placeholders.
- **Three levels of detail:** big shapes that read at a glance, middle shapes that describe the thing,
  small details that reward a second look. Light from flat tone steps, not gradients. Jurors called
  simple drawings "basic" every time.
- **Draw large and let it carry the idea:** the hero's dominant element, a full-width band, a motif
  that returns at different scales. Small doodles scattered around read as filler.
- **Honesty:** if a drawing could be taken for a real product, say plainly near it or in the footer
  that pictures are drawn until photographs exist; list the drawings in the report.
- **Not this:** 3D-looking gradient blobs, isometric clip art, line illustrations of people at laptops,
  abstract floating shapes, icons in tinted squares.

## 6. Type and colour alone

A legitimate design, not a gap to disguise: one statement at 10-14vw, a list at 5vw, numerals at
display size, colour at scale (a full field, an inverted section, a two-field split). Do not add icons
in squares, abstract gradients, dot grids, wave dividers, floating shapes, emoji, or an empty box where
a picture "will go".

## 7. Cropping, placing, treatment

- A small set of ratios, used throughout (for example 4:5, 16:10, 1:1). Random ratios look like a dump.
- Go large: one picture at full width or half the screen at full height beats six small ones.
- `object-fit: cover` with an `object-position` chosen per picture.
- One radius for every picture (square by default), no frames, borders, device mock-ups or shadows.
- One treatment for the whole page: untouched, greyscale for every picture, or `mix-blend-mode:
  multiply` on a light field. No colour washes, duotone, blur, grain or vignettes.
- Text on a photograph gets a neutral scrim under the text only (40-55% black). Nothing lies on top of
  a headline.
- Always `width`/`height` or `aspect-ratio`; `loading="lazy"` except the hero (`fetchpriority="high"`);
  `alt` says what the picture shows.

## 8. Logos and social proof

- A logo wall shows **real customers the brief names**, with their own logo files or permission. Never
  real company names or marks the brief did not supply, and never a mark invented for a fake customer.
- No real proof supplied: leave the section out. If the brief explicitly asks for the section, build it
  with plainly fictional sample names (no real companies, no real people) and list it in the report as
  content to replace before launch.
- When a real logo wall exists: logos only, no category label under each, one colour treatment that
  works in light and dark, under the hero, never inside it.
