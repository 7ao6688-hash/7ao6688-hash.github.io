"""Wrap page.html (shared with the preview) into a standalone v1.html (the classic layout, kept alongside the new home page)."""
from pathlib import Path

here = Path(__file__).parent
head, body = (here / "page.html").read_text(encoding="utf-8").split("<!--BODY-->", 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head}</head>\n<body>\n{body}</body>\n</html>\n")
(here / "v1.html").write_text(html, encoding="utf-8")
print(f"v1.html written ({len(html) // 1024} KB)")
