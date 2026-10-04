# Personal website

Plain HTML and CSS, no build step. GitHub Pages serves the files exactly as they are.

## Files

- `index.html`: home page (bio, contact line, portrait)
- `research.html`: papers (a commented-out "Code & other projects" section holding the thesis is ready to restore once the degree is approved)
- `cv.html`: CV headlines, one line per entry
- `style.css`: all styling, including the mobile layout
- `script.js`: the mobile menu
- `phase-mixing.svg`: the header drawing (level sets of a free-transport solution)
- `portrait.jpg`: the photo on the home page (currently 716 by 895 pixels, used as supplied)
- `favicon.svg`: browser-tab icon
- `sitemap.xml` and `robots.txt`: for search engines (list the three pages; update `lastmod` when a page changes)

## Putting it on GitHub Pages

1. On GitHub, create a new public repository called `marniersmith.github.io`,
   using your GitHub username. Do not add a README or licence there.
2. In a terminal, from this folder:

       git remote add origin git@github.com:marniersmith/marniersmith.github.io.git
       git push -u origin main

3. On the repository page go to Settings, then Pages. Under "Build and
   deployment" choose Source: "Deploy from a branch", Branch: `main`, folder
   `/ (root)`, and save.
4. After a minute or two the site is live at `https://marniersmith.github.io`.

Every later `git push` to `main` updates the site.

## Editing

- To add a paper: copy one `<li>` block in `research.html` and edit it. The
  list is newest first.
- The bio is the three paragraphs inside `<div class="bio">` in `index.html`.
- The email is written as `name "at" domain "dot" com` to keep it off
  scraper lists; change it in `index.html`.
- Colours and fonts are at the top of `style.css`.
- To regenerate the header drawing with different parameters, see
  `tools/phase-mixing.py`.
