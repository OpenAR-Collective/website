"""Convert the adopted governance documents into the policies content collection.

Reads the .docx files from _Scratch/Governance via pandoc, strips the adoption
signature block (the page template renders adoption from frontmatter instead),
demotes headings one level so the page title is the only h1, and converts the
annexed form's blank rules into styled fields.
"""

import re
import subprocess
from pathlib import Path

REPO = Path(r"C:\Projects\OpenARCollective_Website")
SRC = REPO / "_Scratch/Governance"
OUT = REPO / "src/content/policies"

# slug, source stem, title, category, order, description
DOCS = [
    (
        "bylaws",
        "Bylaws",
        "Bylaws",
        "Governing document",
        1,
        "The Foundation's governing document: purpose, Board composition and independence requirements, officers, committees, indemnification, and amendment.",
    ),
    (
        "conflicts-of-interest",
        "Conflicts_of_Interest_Policy",
        "Conflicts of Interest Policy",
        "Board and organizational governance",
        2,
        "Disclosure, recusal, and review procedures for conflicts involving directors, officers, and related parties.",
    ),
    (
        "anti-capture",
        "Anti-Capture_Policy",
        "Anti-Capture Policy",
        "Board and organizational governance",
        3,
        "Structural limits on funder and employer influence, including revenue concentration limits and board eligibility restrictions.",
    ),
    (
        "anti-nepotism",
        "Anti-Nepotism_Policy",
        "Anti-Nepotism Policy",
        "Board and organizational governance",
        4,
        "Restrictions on hiring, contracting, and appointing family members of directors and officers.",
    ),
    (
        "antitrust",
        "Antitrust_Policy",
        "Antitrust Policy",
        "Board and organizational governance",
        5,
        "Competition law compliance for Foundation meetings, community spaces, and standards work.",
    ),
    (
        "whistleblower",
        "Whistleblower_Policy",
        "Whistleblower Policy",
        "Board and organizational governance",
        6,
        "Protections for people who report suspected legal or policy violations in good faith, and how reports are received and investigated.",
    ),
    (
        "document-retention",
        "Document_Retention_and_Destruction_Policy",
        "Document Retention and Destruction Policy",
        "Board and organizational governance",
        7,
        "Retention periods by record type, destruction procedures, and legal hold obligations.",
    ),
    (
        "gift-acceptance",
        "Gift_Acceptance_Policy",
        "Gift Acceptance Policy",
        "Board and organizational governance",
        8,
        "Which gifts the Foundation accepts, which it declines, and how gifts are reviewed, valued, and acknowledged.",
    ),
    (
        "volunteer-and-expense-reimbursement",
        "Volunteer_and_Expense_Reimbursement_Policy",
        "Volunteer and Expense Reimbursement Policy",
        "Board and organizational governance",
        9,
        "Volunteer engagement and the substantiation, approval, and reimbursement of expenses.",
    ),
    (
        "community-programs-and-standards",
        "Community_Programs_and_Standards_Policy",
        "Community Programs and Standards Policy",
        "Programs, community, and intellectual property",
        10,
        "The membership and Mission Supporter programs, community standards, moderation, and the terms of participation.",
    ),
    (
        "open-source",
        "Open_Source_Policy",
        "Open Source Policy",
        "Programs, community, and intellectual property",
        11,
        "License selection for Foundation software and documentation, and the Developer Certificate of Origin contribution model.",
    ),
    (
        "trademark",
        "Trademark_Policy",
        "Trademark Policy",
        "Programs, community, and intellectual property",
        12,
        "Permitted and restricted uses of the Foundation's Marks, fork and distribution naming, and enforcement.",
    ),
]

# Everything from these markers to the end of the document is the adoption
# signature block, which the page template renders from frontmatter. Addendum A
# reproduces a blank disclosure form, which is not published.
CUT_MARKERS = (
    "Adopted by the Board of Directors of The Open Accounts Receivable",
    "**CERTIFICATE OF ADOPTION**",
    "# ADDENDUM A:",
)

# Article VIII of the Conflicts policy cross-references Addendum A, so the
# omission is noted rather than left dangling.
ADDENDUM_NOTE = (
    '\n\n<p class="editorial-note">Addendum A, which reproduces the form of the Annual '
    "Disclosure Statement, is not published on this website. The form is approved and "
    "amended by the Board of Directors as a separate instrument.</p>"
)

BLANK_RUN = re.compile(r"(?:\\_){3,}_*")
NBSP_LINE = re.compile(r"^[\s\u00a0]+$")


def convert(stem: str) -> str:
    src = SRC / f"OpenAR_Collective_-_{stem}_2026-08-09.docx"
    return subprocess.run(
        ["pandoc", "-t", "markdown", "--wrap=none", str(src)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout


def strip_signature_block(text: str) -> str:
    cut = len(text)
    for marker in CUT_MARKERS:
        i = text.find(marker)
        if i != -1:
            cut = min(cut, i)
    return text[:cut].rstrip()


def demote_headings(text: str) -> str:
    """Add one # to every ATX heading so the page h1 stays unique."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{1,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def tidy(text: str) -> str:
    lines = []
    for line in text.split("\n"):
        if NBSP_LINE.match(line):
            line = ""
        # Blank fill-in rules in annexed forms become styled fields.
        line = BLANK_RUN.sub('<span class="field"></span>', line)
        lines.append(line)
    # Collapse runs of blank lines left behind.
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, stem, title, category, order, description in DOCS:
        body = tidy(demote_headings(strip_signature_block(convert(stem))))
        if slug == "conflicts-of-interest":
            body += ADDENDUM_NOTE
        front = (
            "---\n"
            f'title: "{title}"\n'
            f'description: "{description}"\n'
            f'category: "{category}"\n'
            f"order: {order}\n"
            "adopted: 2026-08-13\n"
            "---\n\n"
        )
        path = OUT / f"{slug}.md"
        path.write_text(front + body + "\n", encoding="utf-8", newline="\n")
        print(f"{path.name}: {len(body):,} chars")


if __name__ == "__main__":
    main()
