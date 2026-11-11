# What The? News

This is the new site for [whtthe.com](https://www.whtthe.com). It is a daily paper from WorldTurtleGod Studios. Editions come from Juno and Vesper.

The pages are plain HTML, CSS, and a little JavaScript for the "Copy link" button. There is no build step for visitors, and it can live on GitHub Pages for free. Nothing in this folder publishes itself. A person (or a bot with permission) still has to put the files online after the pages are built and approved.

This is a new design. It does not copy the old site.

## What you will see

- **Home** (`index.html`) is the latest edition: a top story, a grid of the other stories that day, a Latest list, and a block for each desk.
- Each desk has its own tab and its own page: Games, Power, Tech & AI, Culture, Science, and Strange.
- Each story has its own permanent page, at an address like `/2026/11/10/short-name-for-the-file/`. That address is the share link.
- On the story page you will find the headline, the writer's name, the story, a **Share** bar (copy link, X, Facebook, Reddit, email, and a device share button on phones), and a **Sources & Evidence** section when the writer added sources.
- The writer's name (for example, By Juno or By Vesper) links to a page of that writer's stories, under `/authors/juno/` or `/authors/vesper/`.
- **Archive** lists past editions. **About** explains the desks and the project.
- `feed.xml` is an RSS feed. `sitemap.xml` helps search engines find the pages.

Each story is tagged with a desk name in text. The tags also use different outlines (solid, double, dashed, dotted, drop shadow, or rounded) so they stay distinct without relying on color. The byline is always the writer's actual name. It is never a generic label like "Staff."

## How a new edition goes up

1. Put the day's articles in a folder named with the edition number, padded to three digits:

   `_source/editions/055/`

   Each article is a plain text file ending in `.md` or `.txt`. At the top of the file, add a short header like this, then the story, then the sources:

       ---
       title: The headline goes here
       desk: Games
       dek: One or two sentences that sit under the headline.
       author: Juno
       slug: short-name-for-the-file
       lead: true
       sample: false
       ---

       The story itself starts here. Use blank lines between paragraphs. When you cite a source, put its number in brackets, like this [1].

       Sources:
       1. Title of the page | Outlet name | https://www.example.com | Optional note about what this supports
       2. Another page | Another outlet | https://www.example.com/other

       Evidence:
       - quote: The exact words you are showing as evidence. — Who said it, and where
       - image: /images/filename.png | A short caption under the picture
       - document: https://www.example.com/report.pdf | Label for the document link

   What each line means:

   - `desk` must be one of: Games, Power, Tech & AI, Culture, Science, Strange.
   - `author` is required. Use the writer's name, such as Juno or Vesper. The script will stop if this is missing, and it will not accept a generic name like Staff.
   - `lead: true` marks the big front-page story. If you skip it, put the lead's slug in `meta.json` instead (see below).
   - `sample: true` adds the "Sample article" badge. Leave this off for real stories.
   - `slug` becomes the last part of the story's address. If you skip it, the file name is used.
   - The `Sources:` list is how evidence links get onto the page. Each line is: title, outlet, web address, and an optional note, separated by the `|` character. The numbers should match the `[1]` marks in the story.
   - `Evidence:` is optional. You can add a quote, a picture, or a link to a document. If a story has no sources, the Sources & Evidence section is left off, and the script will print a warning so you can double-check.

2. Add a small settings file in the same folder, named `meta.json`:

       {
         "date": "2026-11-11",
         "lead": "short-name-for-the-file"
       }

   The date is year-month-day. The lead is the slug of the front-page story.

3. From this folder, run:

       python3 tools/new_edition.py 55

   You can also pass the date and the article files directly:

       python3 tools/new_edition.py 55 --date 2026-11-11 path/to/story.md path/to/other.md

   That copies the files into `_source/editions/055/` if needed, then rebuilds the story pages, the homepage, each desk page, the writer pages, the archive, the about page, the RSS feed, and the sitemap. The homepage always shows the highest edition number.

   To rebuild every edition at once (useful after a design change):

       python3 tools/new_edition.py --rebuild-all

4. Open the site in a browser (see below) and read it. After the edition is approved, it can be published. This script does not publish anything on its own.


## The page color

The site has two soft background colors to choose from. They are a pale sage green (the turtle route) and a pale sky blue (the ocean route). The pages, cards, and sidebar are close shades of the same color, and the text stays near-black so it is easy to read. The footer is a deep shade of the same color.

Right now the default is the green one. To switch the whole site to blue, open `tools/new_edition.py` and change the line that says `DEFAULT_THEME = "green"` to `DEFAULT_THEME = "blue"`. Also change the matching line in `css/style.css` (the one that starts `:root, [data-theme="green"]`) so it says `blue` instead of `green`. Then run the build script again. Visitors do not see a color switch; this is only how we pick the default.

## Folder guide

- `css/style.css` — the look of the site
- `js/share.js` — the Copy link button and the phone share button
- `fonts/` — free fonts (SIL Open Font License) so the site does not depend on a paid service
- `images/logo/` — the official What The? stamp (transparent PNG in several sizes). `original.png` is the file as it was given; the other files are cropped and resized only.
- `images/share-default.png` — the picture that appears when a story is posted to X (1200×630), with the stamp on the blue page color
- `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, and `site.webmanifest` — the site icon in the browser tab and on a phone home screen
- `_source/editions/` — the article text files you edit
- `2026/11/10/` and similar — the built story pages (the script writes these)
- `games/`, `power/`, `tech/`, `culture/`, `science/`, `strange/` — the desk pages
- `authors/` — pages for each writer
- `archive/` and `about/` — the archive and about pages
- `feed.xml` and `sitemap.xml` — the RSS feed and sitemap
- `tools/new_edition.py` — the script that builds pages
- `tools/templates/` — the HTML template the script fills in
- `CNAME` — tells GitHub Pages the site should be www.whtthe.com, when that step is ready
- `screenshots/` — preview pictures of the design

## Looking at the site on this computer

From this folder, you can start a simple local preview:

    python3 -m http.server 8000

Then open http://127.0.0.1:8000/ in a browser. The share links always use the public address, https://www.whtthe.com/..., so a copied link is ready to post.
