"""Check that the HTML rendering of the architecture decision brief shows the brief's version.

Run from the repository root:  python3 tests/docs/check_report_version.py [brief.md page.html]
With no arguments it compares docs/architecture/architecture-decision-brief.md with
reports/architecture-decision-brief.html.

The version is read from the Markdown brief's header line ("Draft vX.Y.Z", before the first
"## " heading) and from the text of the HTML element with id="brief-version".
Exit status 0 if the two versions match; 1, with a message, if they differ or either
version cannot be found. Python 3 standard library only.
"""
import html.parser
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BRIEF = ROOT / "docs" / "architecture" / "architecture-decision-brief.md"
PAGE = ROOT / "reports" / "architecture-decision-brief.html"
TARGET_ID = "brief-version"
MD_VERSION = re.compile(r"\bDraft v(\d+\.\d+\.\d+)\b")
HTML_VERSION = re.compile(r"\bv?(\d+\.\d+\.\d+)\b")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def brief_version(path: pathlib.Path):
    """Return the X.Y.Z of "Draft vX.Y.Z" in the brief's header (lines before the first section)."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        match = MD_VERSION.search(line)
        if match:
            return match.group(1)
    return None


class _ElementText(html.parser.HTMLParser):
    """Collect the text of every element whose id attribute is TARGET_ID."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []  # one text string per matching element
        self.depth = 0   # open elements inside the current match; 0 means outside any match

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        if self.depth:
            self.depth += 1
        elif dict(attrs).get("id") == TARGET_ID:
            self.found.append("")
            self.depth = 1

    def handle_startendtag(self, tag, attrs):
        pass  # a self-closing tag neither opens nor closes the element being read

    def handle_endtag(self, tag):
        if self.depth and tag not in VOID:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.found[-1] += data


def page_texts(path: pathlib.Path):
    parser = _ElementText()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return [" ".join(text.split()) for text in parser.found]


def main(argv) -> int:
    if len(argv) not in (0, 2):
        print("usage: python3 tests/docs/check_report_version.py [brief.md page.html]")
        return 1
    brief, page = (pathlib.Path(a) for a in argv) if argv else (BRIEF, PAGE)
    for path in (brief, page):
        if not path.is_file():
            print(f"FAIL: file not found: {rel(path)}")
            return 1

    expected = brief_version(brief)
    if expected is None:
        print(f'FAIL: no "Draft vX.Y.Z" on the header line of {rel(brief)}')
        return 1

    texts = page_texts(page)
    if not texts:
        print(f'FAIL: {rel(page)} has no element with id="{TARGET_ID}"')
        return 1
    if len(texts) > 1:
        print(f'FAIL: {rel(page)} has {len(texts)} elements with id="{TARGET_ID}"; ids must be unique')
        return 1
    match = HTML_VERSION.search(texts[0])
    if match is None:
        print(f'FAIL: the id="{TARGET_ID}" element in {rel(page)} shows no version (its text: "{texts[0]}")')
        return 1

    shown = match.group(1)
    if shown != expected:
        print(
            f"FAIL: version mismatch. {rel(brief)} is Draft v{expected}, but {rel(page)} "
            f'shows v{shown} (id="{TARGET_ID}"). Regenerate the HTML rendering from the Markdown brief.'
        )
        return 1
    print(f"OK: {rel(page)} shows v{shown}, matching Draft v{expected} in {rel(brief)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
