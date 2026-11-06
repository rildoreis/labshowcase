# What's in the Lab — Technology Showcase

Static site for GitHub Pages. No build step is required to publish: upload these files as they are.

## Files

```
index.html          home: cover, gallery of technologies, about, link to Collaborate
collaborate.html    booking, project-idea form, quick poll
lab.html            who we are, where, house rules (fill in the placeholders)
tech/*.html         one page per technology (11)
images/             photos (JPG, resized for the web)
FORMS.md            questions and settings for every Google Form
techs.json          the text of every technology page (source data)
links.json          the "Learn and explore" links per technology
```

## Publish on GitHub Pages

1. Create a public repository (for example `lab-showcase`).
2. Upload everything in this folder to the repository root (`index.html` must be at the root).
3. Settings → Pages → Source: *Deploy from a branch* → branch `main`, folder `/ (root)` → Save.
4. After a minute or two the site is live at `https://USERNAME.github.io/lab-showcase/`.
   Each technology has its own address, e.g. `…/lab-showcase/tech/meta-quest-3.html` — handy for QR codes next to the equipment.

## Add the interactive blocks

Every page has dashed placeholders. Each one has an HTML comment just above it saying what to paste:

- **Demo video** — YouTube → Share → Embed → copy the `<iframe>` → replace the placeholder `<div class="placeholder">…</div>`.
- **I'm interested** — Google Form (see FORMS.md, Form 1) → Send → `< >` → copy the `<iframe>`. Use a pre-filled link per technology.
- **Idea wall** — Padlet → Share → *Embed in your blog or website* → copy the `<iframe>`.
- **Book a demo / Propose a project / Quick poll** — on `collaborate.html`, same procedure (FORMS.md, Forms 2–4, or a Google Calendar appointment schedule).

Remove the placeholder `<div>` and paste the `<iframe>` in its place; the surrounding `<div class="embed">` sizes it.

## Edit or add technologies

Either edit the HTML pages directly, or edit `techs.json` / `links.json` and run `python3 build_multi.py` in this folder to regenerate every page, including the gallery and the previous/next links.

To add a technology by hand: copy any file in `tech/`, rename it, change the text and the image, and add a card to the gallery in `index.html`.

## Placeholders to fill in

- Lab name, institution and coordinator contact (hero on `index.html`, `collaborate.html`, footer).
- Photos: `images/` already holds the lab's own photos; replace a file to update a page.

## Things only you can fill in (marked with [brackets] or HTML comments)

- `lab.html`: the paragraph about the lab, the team list, the room photo (`images/lab-room.jpg`).
- Every technology page: the **Used so far** box — one to three lines of real history.
- Footer: "kept by [name]" and the update date.
- Replace inventory photos with photos of the equipment in use when you have them (same file names).
