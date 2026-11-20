"""Refresh the news ticker in index.html with the latest Washington Sun headlines.

Run by .github/workflows/update-ticker.yml every hour. If the feed can't be
fetched or read, the script leaves index.html unchanged.
"""
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://www.washingtonsun.com/all-notus-stories.rss"
MAX_ITEMS = 10
PAGE = Path(__file__).resolve().parents[2] / "index.html"
START = "<!-- TICKER:START -->"
END = "<!-- TICKER:END -->"
INDENT = "          "


def fetch_items():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "personal-site-ticker/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title and link.startswith("https://"):
            items.append((title, link))
        if len(items) == MAX_ITEMS:
            break
    return items


def render(items):
    lis = "".join(
        f'{INDENT}  <li><a href="{html.escape(link)}">{html.escape(title, quote=False)}</a></li>\n'
        for title, link in items
    )
    # Scroll speed stays steady (~55px per second) however long the headlines are.
    chars = sum(len(t) for t, _ in items) + 8 * len(items)
    seconds = max(30, round(chars * 8 / 55))
    return (
        f'{START}\n'
        f'{INDENT}<div class="ticker-track" style="--ticker-duration: {seconds}s">\n'
        f'{INDENT}<ul>\n{lis}{INDENT}</ul>\n'
        f'{INDENT}<ul aria-hidden="true">\n{lis.replace("<a ", "<a tabindex=\"-1\" ")}{INDENT}</ul>\n'
        f'{INDENT}</div>\n'
        f'{INDENT}{END}'
    )


def main():
    try:
        items = fetch_items()
    except Exception as exc:  # network or feed problem: keep the current headlines
        print(f"Could not read feed, leaving ticker unchanged: {exc}")
        return 0
    if not items:
        print("Feed had no usable items, leaving ticker unchanged.")
        return 0
    page = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(page):
        print("Ticker markers not found in index.html")
        return 1
    updated = pattern.sub(lambda _: render(items), page, count=1)
    if updated != page:
        PAGE.write_text(updated, encoding="utf-8")
        print(f"Ticker updated with {len(items)} headlines.")
    else:
        print("Headlines unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
