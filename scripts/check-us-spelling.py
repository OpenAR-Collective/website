"""Flag British spelling variants in site source and content.

Usage:
    python scripts/check-us-spelling.py               # scans src/ and public/
    python scripts/check-us-spelling.py src _Scratch  # scans the given paths

Exits 1 when anything is found, so it can gate a merge later.

Foundation materials use US English throughout. Note that the files under
src/content/policies are quoted verbatim from Board-adopted documents: if a
variant is ever reported there, raise it rather than editing, because changing
it would make the published page diverge from the adopted document.
"""

import pathlib
import re
import sys

# Stems where any trailing letters are still the British form:
# colour/colours/coloured, organis/organise/organisation, and so on.
STEMS = [
    # -our
    "armour", "behaviour", "colour", "endeavour", "favour", "flavour", "harbour",
    "honour", "humour", "labour", "neighbour", "odour", "parlour", "rumour",
    "saviour", "splendour", "vapour", "vigour",
    # -re
    "calibre", "centre", "fibre", "litre", "lustre", "meagre", "metre", "sombre",
    "spectre", "theatre", "kilometre", "millimetre",
    # -ence / -ise verb forms
    "defence", "offence", "pretence", "licenc", "practis",
    # -ise / -isation
    "analys(e|ed|es|ing)", "apologis", "authoris", "categoris", "centralis",
    "civilis", "criminalis", "decentralis", "emphasis(e|ed|es|ing)", "formalis",
    "harmonis", "legalis", "maximis", "memoris", "minimis", "modernis",
    "normalis", "optimis", "organis", "paralys", "penalis", "prioritis",
    "publicis", "realis(e|ed|es|ing)", "recognis", "specialis", "stabilis",
    "standardis", "summaris", "utilis", "visualis",
    # doubled consonant before a suffix
    "cancell(ed|ing)", "counsell", "fuelled", "levelled", "marvellous",
    "modell(ed|ing)", "signall(ed|ing)", "totalled", "travell(ed|ing)",
    # misc
    "acknowledgement", "aeroplane", "aluminium", "instalment", "jewellery",
    "judgement", "manoeuvre", "pyjamas", "sceptic", "skilful", "smoulder",
    "speciality", "sulphur", "whilst", "wilful",
]

# Exact words only: a prefix match would catch correct US words such as
# programmer, annexed, greyhound, or discount.
WHOLE = [
    "amongst", "annexe", "axe", "cheque", "cosy", "disc", "draught", "enrol",
    "fulfil", "fulfils", "fulfilment", "gaol", "grey", "kerb", "labelled",
    "labelling", "maths", "mould", "plough", "programme", "programmes",
    "storey", "towards", "tyre",
]

# Correct US English that the stem patterns would otherwise catch.
ALLOW = {
    "advertise", "advertised", "advertises", "advertising", "advise", "advised",
    "advises", "advising", "arise", "arises", "arising", "comprise", "comprised",
    "comprises", "comprising", "compromise", "compromised", "concise", "devise",
    "devised", "disguise", "exercise", "exercised", "exercises", "exercising",
    "expertise", "franchise", "improvise", "incise", "merchandise", "noise",
    "otherwise", "practice", "practices", "precise", "premise", "premises",
    "promise", "promised", "promises", "raise", "raised", "revise", "revised",
    "rise", "rises", "supervise", "supervised", "supervising", "surprise",
    "surprised", "televise", "wise",
    # HTML and ARIA vocabulary, not prose.
    "labelledby", "aria-labelledby",
}

SKIP_DIRS = {"node_modules", "dist", ".git", ".astro"}
SKIP_FILES = {"OFL.txt", "OFL-DMSans.txt", "OFL-DMSerifDisplay.txt", "LICENSE"}
EXTS = {".astro", ".css", ".htm", ".html", ".js", ".json", ".md", ".mjs", ".ts",
        ".txt", ".webmanifest"}

PATTERN = re.compile(
    r"\b(?:" + "|".join(f"(?:{s})[a-z]*" for s in STEMS) + "|"
    + "|".join(f"(?:{w})" for w in WHOLE) + r")\b",
    re.I,
)


def files(roots):
    for root in roots:
        for path in pathlib.Path(root).rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTS:
                continue
            if path.name in SKIP_FILES:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            yield path


def main():
    roots = sys.argv[1:] or ["src", "public"]
    hits = []
    for path in files(roots):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.split("\n"), 1):
            for match in PATTERN.finditer(line):
                word = match.group(0)
                # aria-labelledby arrives as "labelledby" after the word break.
                if word.lower() in ALLOW:
                    continue
                hits.append((path, number, word, line.strip()[:110]))

    for path, number, word, line in hits:
        print(f"{path}:{number}: {word}\n    {line}")

    if hits:
        print(f"\n{len(hits)} British variant(s) found.")
        return 1
    print(f"Clean: no British variants in {', '.join(roots)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
