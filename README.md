# What's in the Lab — Technology Showcase

Emerging Technologies and Creativity Research Laboratory · Learning, Design and Technology · Oklahoma State University · 007A Willard Hall

A static site for GitHub Pages. You do not need a build step to publish it: upload the files as they are.

## Files

```
index.html          home page: cover, gallery of the 15 technologies (alphabetical), how this works
lab.html            about the lab: photo, description, room, hours, contacts
collaborate.html    how collaboration works, contacts, embedded Google Form
tech/*.html         one page per technology
images/             photos (JPG, resized for the web)
techs.json          text of every technology page (source data)
links.json          "Learn and explore" links per technology
build_multi.py      regenerates every page from techs.json and links.json
```

## Publish on GitHub Pages

1. Create a public repository, for example `lab-showcase`.
2. Upload everything in this folder to the root of the repository. `index.html` must be at the root.
3. Go to Settings → Pages → Source: *Deploy from a branch*, choose branch `main`, folder `/ (root)`, and save.
4. After a minute or two the site is live at `https://USERNAME.github.io/lab-showcase/`.
   Each technology has its own address, for example `…/lab-showcase/tech/meta-quest-3.html`. You can use these addresses in QR codes.

## Edit content

- **Small text changes:** edit the HTML files directly.
- **Many changes, or adding a technology:** edit `techs.json` and `links.json`, then run `python3 build_multi.py` in this folder. The script regenerates every page, the gallery, the LAB codes (alphabetical) and the previous/next links.
- **Photos:** replace a file in `images/` and keep the same name.
- **Footer date:** update "Page updated …" in `build_multi.py`, or in every HTML file, whenever you publish changes.

The Google Form on `collaborate.html` is embedded with an `<iframe>`. If you change the form, paste the new embed code in the same place.
