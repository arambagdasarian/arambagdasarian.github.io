"""Check built pages, local links, anchors, metadata, and the CV asset."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import argparse


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.h1, self.canonical = set(), [], 0, None
        self.lang = None
        self.description = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "meta" and attrs.get("name") == "description":
            self.description = bool(attrs.get("content"))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag in ("a", "link", "img", "script", "source"):
            value = attrs.get("href") if tag in ("a", "link") else attrs.get("src")
            if value is not None:
                self.links.append(value)


def check(root, origin, baseurl):
    root = root.resolve()
    pages = {}
    for path in root.rglob("*.html"):
        text = path.read_text()
        assert "{{" not in text and "{%" not in text, f'Unrendered template in {path}'
        assert "\u2014" not in text, f'Em dash in {path}'
        page = Page(text)
        assert page.h1 == 1 and page.lang and page.description, f'Page structure in {path}'
        relative = path.relative_to(root).as_posix()
        route = "/" + relative.removesuffix("index.html")
        if relative != "404.html":
            assert page.canonical == origin + baseurl + route, f'Canonical URL in {path}'
        pages[path] = page
    assert len(pages) >= 3, "Missing homepage, archive, or 404 page"
    for path, page in pages.items():
        document_url = origin + baseurl + "/" + path.relative_to(root).as_posix()
        for href in page.links:
            assert href and href != "#", f'Placeholder link in {path}'
            parsed = urlsplit(urljoin(document_url, href))
            if parsed.scheme not in ("http", "https") or parsed.netloc != urlsplit(origin).netloc:
                continue
            route = unquote(parsed.path)
            assert route.startswith(baseurl + "/"), f'Link ignores base path: {href}'
            target = (root / route[len(baseurl):].lstrip("/")).resolve()
            assert target.is_relative_to(root), f'Link escapes site: {href}'
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f'Broken link in {path}: {href}'
            if parsed.fragment and target in pages:
                assert unquote(parsed.fragment) in pages[target].ids, f'Missing anchor: {href}'
    for path in root.rglob("*"):
        if path.is_file():
            assert path.suffix in {".html", ".css", ".svg", ".jpg", ".jpeg", ".png", ".webp", ".pdf", ".xml", ".txt"}, f'Unexpected output: {path}'
    cv = root / "assets/cv/Aram_Bagdasarian_CV.pdf"
    assert cv.read_bytes().startswith(b"%PDF-"), "Missing or invalid CV"
    for name in ("sitemap.xml", "feed.xml", "robots.txt"):
        assert (root / name).is_file(), f'Missing {name}'
    print(f'Checked {len(pages)} pages, internal links and anchors, metadata, and CV.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default="_site", type=Path)
    parser.add_argument("--origin", default="https://arambagdasarian.github.io")
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()
    check(args.directory, args.origin.rstrip("/"), args.baseurl.rstrip("/"))
