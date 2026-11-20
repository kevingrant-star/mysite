# Instructions for Claude

This repository is a journalist's personal website. GitHub Pages publishes it from the main branch.

- Commit every change straight to main and push it, so the site updates. Don't open pull requests or leave work on other branches.
- Use my words exactly as I give them: my About text, headlines, outlet names and dates. Don't rewrite, shorten, summarize or add to them. If something is missing, leave a clearly marked spot and ask me.
- Never add facts about me that I didn't give you.
- Keep the site simple: one index.html with its styles inside it, and photos in an images folder. No build tools or frameworks.
- When you finish, tell me in plain words what changed, and that the live site can take a minute or two to update.

## Site style

Keep every change in this style, inspired by restofworld.org (the look only, never its logo or name):

- **Colors:** white background, near-black text (#111111), one deep purple accent (#4B1D8F) for labels, links and a 6px bar across the top of the page. Light grey rules (#CACACA) separate sections. No other colors, except the dashed yellow boxes that mark spots waiting for Kevin's text.
- **Type:** three fonts, loaded free from Google Fonts.
  - Name and story headlines: Inter, bold, large and tight.
  - Small labels (the beat line and section headings like About and Clips): IBM Plex Mono, uppercase, widely letter-spaced, in the purple accent, with a grey rule underneath. The uppercase comes from CSS; the words themselves stay as Kevin wrote them.
  - Long reading text (the About paragraph, story summaries): Georgia serif, about 1.15rem, with generous line spacing.
  - Small print (the contact line): Inter, grey.
- **Space:** one centered column about 48rem wide, with plenty of white space between sections (about 3.5rem). Clean and uncluttered, with no shadows, rounded cards or decoration.
- **Photos:** the headshot sits left of the About text on wide screens and above it on phones.
- Everything must work on phones. Long links wrap instead of running off the screen.
- **News ticker:** a slow, continuously scrolling line of the latest Washington Sun headlines sits directly under the beat line, between thin grey rules, in IBM Plex Mono. A small "The Washington Sun" label linking to washingtonsun.com sits on its left, and a small accent-colored dot comes before each headline. It pauses when someone hovers over it, and it stays still for visitors who have turned off motion in their device settings.
  - The headlines update automatically every hour. `.github/workflows/update-ticker.yml` runs `.github/scripts/update_ticker.py`, which reads the Sun's public feed (https://www.washingtonsun.com/all-notus-stories.rss), puts the 10 newest headlines between the `TICKER:START` and `TICKER:END` markers in index.html, and commits to main. Kevin approved this one automation as an exception to the no-build-tools rule.
  - Never edit between those markers by hand. Because this job commits to main every hour, always pull the latest main before making any change.
