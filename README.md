# Aram Bagdasarian

Personal academic website at **https://arambagdasarian.github.io/**.
Built with Jekyll and Markdown. A push to `main` builds and deploys the site through GitHub Actions.

## Approved styling

Aram approved the current styling on September 17, 2026. Preserve the monochrome palette, Georgia typography, reading width, spacing, navigation, and plain research lists. Keep later additions consistent with this design; change the visual direction only when Aram requests it. Do not add a logo, favicon, or logo metadata. Do not use middle-dot separators anywhere on the website.

The homepage portrait is a 144px monochrome crop at `assets/images/aram-bagdasarian.jpg`. The original full-resolution photo stays local and is excluded from Git and the site build.

## Add an update

Create one file in `_posts/` named `YYYY-MM-DD-short-title.md`. You can do this on GitHub using **Add file > Create new file**, or in your local editor. Use the actual publication date and a short, stable filename. The homepage, archive, RSS feed, and sitemap update automatically.

The following is a syntax example only. Replace the title, date, summary, and body with your own update before committing it.

```markdown
---
title: "A short research update"
date: 2026-09-16 12:00:00 -0400
summary: "A one-sentence description of the update."
---
Write the update here using Markdown.

## More detail

Add paragraphs, links, images, and lists as needed.
```

The URL is `/updates/YYYY-MM-DD-short-title/`. Keep the filename and original date when editing a published post. To show a revision date, add `updated: YYYY-MM-DD` to the metadata. The summary is optional. Start body headings at `##`; the title is already the page's main heading.

The homepage shows the newest four updates and hides that section when there are none. Future posts and posts with `published: false` are excluded from builds. A future post appears on the first build after its date; to publish it then, run the workflow manually or push a change. Keep private drafts outside this public repository, since every committed file is public even when omitted from the website.

For site links in posts, use Jekyll's URL filter, for example `[CV]({{ site.cv_path | relative_url }})`.

## Edit the profile, research, or CV

- Edit `index.html` for the homepage introduction, Current work, and Outside Harvard. The separate Research page is `research/index.html`, published at `/research/`.
- Edit `_data/research.yml` for research entries. Use `status: "under_review"` for submissions displayed under Work under review and `status: "in_progress"` for projects displayed under Work in progress. Entries without either status appear under Workshop papers. Venue, year, and URL are optional for work under review. Omit venue details from the data when they should not be public. Format every author list with surnames and initials, retaining the supplied author order and using an ampersand before the final author. The template bolds `Bagdasarian, A.`.
- The chain-of-thought preview diagrams the paper's recorded arithmetic-corruption trial (Section 5.1): edit the notebook cost from $12 to $15, obtain $25 when following the changed reasoning, and $28 when solving from scratch. The labels, example, and problem caption come from the supplied paper. It replaces the earlier abstract Higgsfield clip and does not present aggregate results. The 3.5-second animation preloads and starts on hover or keyboard focus; its final-result poster is shown whenever playback stops, including with reduced motion. Clicking opens the shared closable viewer, with the paper's original problem text. The citation title still links to OpenReview; the no-JavaScript viewer is `/research/chain-of-thought/`. `visual.style: "diagram"` uses the same 232px width as the network preview. The reference PDF stays local and is excluded from Git and site output.
- The adaptation-networks paper uses a minimal derivative of `trajectory_comparison.mp4`, rendered from the same full-sample network data. It preserves the four observed periods, node identities, edges, and smooth transitions, with seven selected labels and a monochrome palette. The optimized video is `assets/video/trajectory-comparison.mp4`; its still is `assets/images/trajectory-network.webp`. `visual.style: "network"` provides a slightly wider preview for label legibility. Clicking opens a video dialog with a Back to research button; Escape and clicking the backdrop also close it. Closing pauses playback and returns focus to the preview. Without JavaScript, `visual.page` opens `/research/network/`, a player page with a Back to research link. The original two-panel source is preserved outside this public repository.
- The network loop starts moving immediately, uses 1.5-second transitions and 0.375-second pauses, and lasts 5.625 seconds. Its small video preloads and restarts on hover or keyboard focus to avoid resuming in a pause. Reduced-motion preferences still keep the preview static. Versioned asset URLs prevent the former long pauses from persisting in browser caches.
- Replace `assets/cv/Aram_Bagdasarian_CV.pdf` to update every CV link without changing its address.
- The public CV's editable source is `cv-source/Aram_Bagdasarian_CV.tex`; the matching supplied PDF is `cv-source/Aram_Bagdasarian_CV.pdf`. When both are supplied, inspect and copy that PDF unchanged to the stable asset path. For source-only updates, compile with XeLaTeX into a temporary directory and inspect the result before replacing both PDF copies. Update the `cv_path` version query in `_config.yml` when replacing the PDF so returning visitors receive the latest version. The site build does not require LaTeX.
- Edit `_layouts/default.html` for the plain-text email displayed in the header. Keep it out of the navigation and footer.
- Edit `_config.yml` for the site description, profile links (`github_url`, `google_scholar_url`, and `orcid_url`), and hosting URL. `baseurl` is empty because this is an account site.

## Google Search

The homepage includes `WebSite`, `ProfilePage`, and `Person` structured data identifying Aram Bagdasarian and linking the existing GitHub, Google Scholar, and ORCID profiles. The description uses the opening sentence supplied for the homepage. Canonical URLs, crawlable HTML, `robots.txt`, and the generated `sitemap.xml` support discovery. No logo or favicon is added.

To set up Search Console, add `https://arambagdasarian.github.io/` as a URL-prefix property and choose HTML-tag verification. Copy only the tag's `content` value into `google_site_verification` in `_config.yml`, publish, then click Verify in Search Console. Submit `sitemap.xml` and use URL Inspection to request indexing of the homepage. Keep the verification value in place after verification. Google controls indexing and ranking; publishing or submitting a request does not guarantee either.

## Preview locally

Use Ruby 3.4.10, Bundler, and Python 3. On this Mac, Homebrew Ruby is installed at `/opt/homebrew/opt/ruby@3.4/bin`. Run these exports in the terminal first; the Xcode setting selects the compiler needed when installing native gems.

```sh
export PATH="/opt/homebrew/opt/ruby@3.4/bin:$PATH"
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
```

Then, from the repository folder:

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open **http://127.0.0.1:4000/**. Content edits rebuild automatically. Restart the server after editing `_config.yml`. Use `--port 4001` if port 4000 is occupied.

## Verify and deploy

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter --trace
python3 scripts/check_site.py
python3 scripts/check_updates.py
```

The update check creates synthetic posts in a temporary copy outside the repository and removes that copy afterward. It checks recent-post ordering, the archive, Markdown rendering, dates, nested URLs, a nonempty base path, and exclusion of drafts and future posts.

Commit the intended public files and push to `main`. The **Build and deploy site** workflow validates the generated output before deploying. Pull requests build without deploying. GitHub Pages must use **GitHub Actions** as its publishing source under **Settings > Pages**.

No analytics or external font services are used. The core site works without JavaScript; a small script on the Research page adds animation playback to the static project preview.
