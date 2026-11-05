"""Check relative links and heading anchors in the repository's Markdown files.

Run from the repository root:  python3 tests/docs/check_links.py [files...]
With no arguments, every tracked-looking *.md file under the repository is checked.
Exit status 1 if any link target or anchor is missing.

Anchors follow GitHub's slug rules: lowercase; drop characters that are not letters,
digits, spaces, hyphens or underscores; spaces become hyphens; duplicates get -1, -2, ...
"""
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?<!!)\[(?:[^\[\]]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)          # inline HTML
    text = re.sub(r"`([^`]*)`", r"\1", text)     # code spans
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = text.replace("*", "").replace("_", "_")
    out = []
    for ch in text.lower():
        cat = unicodedata.category(ch)
        if ch in "-_ " or cat[0] in ("L", "N") or cat == "Mn":
            out.append(ch)
    return "".join(out).replace(" ", "-")


def anchors(path: pathlib.Path) -> set:
    seen, result, in_fence = {}, set(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        base = slug(m.group(2))
        n = seen.get(base, 0)
        result.add(base if n == 0 else f"{base}-{n}")
        seen[base] = n + 1
    for m in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', path.read_text(encoding="utf-8")):
        result.add(m.group(1))
    return result


def links(path: pathlib.Path):
    in_fence = False
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for m in LINK.finditer(line):
            yield no, m.group(1)


def check(files) -> int:
    cache, errors = {}, 0
    for f in files:
        for no, target in links(f):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):  # http:, https:, mailto:
                continue
            ref, _, frag = target.partition("#")
            dest = f if ref == "" else (f.parent / ref).resolve()
            if not dest.exists():
                print(f"{f.relative_to(ROOT)}:{no}: missing file {target}")
                errors += 1
                continue
            if frag and dest.suffix == ".md":
                if dest not in cache:
                    cache[dest] = anchors(dest)
                if frag not in cache[dest]:
                    print(f"{f.relative_to(ROOT)}:{no}: missing anchor #{frag} in {dest.relative_to(ROOT)}")
                    errors += 1
    return errors


def main(argv) -> int:
    if argv:
        files = [pathlib.Path(a).resolve() for a in argv]
    else:
        files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    errors = check(files)
    print(f"checked {len(files)} files: {errors} broken link(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
