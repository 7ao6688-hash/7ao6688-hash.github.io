"""Wrap page.html (shared with the preview) into a standalone index.html for GitHub Pages."""
from pathlib import Path

here = Path(__file__).parent
head, body = (here / "page.html").read_text(encoding="utf-8").split("<!--BODY-->", 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head}</head>\n<body>\n{body}</body>\n</html>\n")
(here / "index.html").write_text(html, encoding="utf-8")
print(f"index.html written ({len(html) // 1024} KB)")
