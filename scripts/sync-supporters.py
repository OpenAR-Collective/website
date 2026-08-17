"""Sync the Mission Supporter roster from CiviCRM into the content collection.

Reads the organizations in a CiviCRM group through the API4 REST endpoint and
writes one JSON file per organization into src/content/supporters/. Files for
organizations no longer in the group are removed, which is how a withdrawal
reaches the website.

The script only touches the working tree. Committing and deploying is the job of
.github/workflows/sync-supporters.yml, which runs this on a schedule so an
approved organization reaches the roster with no further step. The human check
happens earlier, when a reviewer adds the organization to the published group.

Usage:
    python scripts/sync-supporters.py --dry-run
    python scripts/sync-supporters.py

Configuration comes from the environment, never from the repository:

    CIVI_BASE_URL   e.g. https://join.openarcollective.org
    CIVI_API_KEY    the CiviCRM contact's API key
    CIVI_SITE_KEY   the site key from civicrm.settings.php, sent as X-Civi-Key
                    because authx_guards includes site_key on this install
    CIVI_GROUP      group name or title, defaults to "supporters_published"

Offline testing:

    CIVI_FIXTURE=path/to/contacts.json python scripts/sync-supporters.py --dry-run

reads the contact list from a file instead of the network, using the same shape
the API returns.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "src/content/supporters"
DEFAULT_GROUP = "supporters_published"
USER_AGENT = "OpenAR-roster-sync/1.0 (+https://openarcollective.org)"

# Astro's content layer keeps a persistent store here. Deleting a source file
# does not evict its entry, so a withdrawn organization would still render in a
# local build. The store is a cache and is rebuilt on the next build; CI clones
# fresh and never has one.
ASTRO_STORE = ROOT / "node_modules/.astro/data-store.json"

# Fields the supporters content collection accepts. Anything else is dropped
# rather than written, so a stray CiviCRM field cannot break the site build.
SCHEMA_FIELDS = ("name", "website")


class SyncError(Exception):
    pass


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "supporter"


def call_api4(entity: str, action: str, params: dict) -> list[dict]:
    """Call the CiviCRM API4 AJAX endpoint and return the values."""
    base = os.environ.get("CIVI_BASE_URL")
    api_key = os.environ.get("CIVI_API_KEY")
    site_key = os.environ.get("CIVI_SITE_KEY")
    missing = [
        name
        for name, value in (
            ("CIVI_BASE_URL", base),
            ("CIVI_API_KEY", api_key),
            ("CIVI_SITE_KEY", site_key),
        )
        if not value
    ]
    if missing:
        raise SyncError(
            "missing environment variables: " + ", ".join(missing) +
            "\nSet them, or use CIVI_FIXTURE to run offline."
        )

    url = f"{base.rstrip('/')}/civicrm/ajax/api4/{entity}/{action}"
    data = urllib.parse.urlencode({"params": json.dumps(params)}).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            # X-Civi-Auth is authx's "xheader" flow, which accepts an API key.
            "X-Civi-Auth": f"Bearer {api_key}",
            # authx_guards includes site_key on this install, so the request is
            # refused without this even when the API key itself is valid.
            "X-Civi-Key": site_key,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
            # Cloudflare sits in front of join.openarcollective.org and blocks
            # urllib's default agent outright, with its own 403 before the
            # request ever reaches CiviCRM.
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SyncError(f"CiviCRM returned HTTP {exc.code}: {exc.read()[:400]!r}") from exc
    except urllib.error.URLError as exc:
        raise SyncError(f"could not reach CiviCRM: {exc.reason}") from exc

    if "values" not in payload:
        raise SyncError(f"unexpected API response: {json.dumps(payload)[:400]}")
    return payload["values"]


def fetch_group_id(group: str) -> int:
    """Resolve a group name or title to its id.

    Filtering contacts by ["groups", "IN", ["some title"]] is a DB syntax error;
    the pseudo-field only accepts ids. Resolving here keeps the configuration
    readable while sending CiviCRM something it can actually use.
    """
    values = call_api4("Group", "get", {
        "select": ["id", "name", "title"],
        "where": [["OR", [["name", "=", group], ["title", "=", group]]]],
        "limit": 2,
    })
    if not values:
        raise SyncError(f"no CiviCRM group named or titled {group!r}")
    if len(values) > 1:
        found = ", ".join(f"#{v['id']} {v['name']}" for v in values)
        raise SyncError(f"{group!r} matches more than one group: {found}")
    return int(values[0]["id"])


def fetch_contacts() -> list[dict]:
    """Return the organization records in the published group."""
    fixture = os.environ.get("CIVI_FIXTURE")
    if fixture:
        return json.loads(Path(fixture).read_text(encoding="utf-8"))

    group = os.environ.get("CIVI_GROUP", DEFAULT_GROUP)
    return call_api4("Contact", "get", {
        "select": [
            "organization_name",
            "display_name",
            "MissionSupporter.trade_name",
            "MissionSupporter.website_url",
        ],
        "where": [["groups", "IN", [fetch_group_id(group)]], ["is_deleted", "=", False]],
        "limit": 0,
    })


def first_value(contact: dict, *keys: str) -> str:
    """Return the first non-empty value among keys, stripped."""
    for key in keys:
        value = contact.get(key)
        if value:
            return str(value).strip()
    return ""


def to_entry(contact: dict) -> dict | None:
    """Map one CiviCRM record to a content collection entry, or None to skip."""
    # The roster lists an organization under the name it trades as. The legal
    # name is what the Statement is signed in, and it stands in when the
    # organization gave no trade name.
    name = first_value(
        contact,
        "MissionSupporter.trade_name",
        "trade_name",
        "organization_name",
        "display_name",
    )
    if not name:
        return None

    entry = {"name": name}

    website = first_value(contact, "MissionSupporter.website_url", "website")
    if website:
        if not website.startswith(("http://", "https://")):
            website = "https://" + website
        entry["website"] = website

    return {k: v for k, v in entry.items() if k in SCHEMA_FIELDS}


def plan(entries: list[dict]) -> tuple[dict[str, dict], list[Path]]:
    """Return the files to write, and the stale files to delete."""
    wanted: dict[str, dict] = {}
    for entry in entries:
        slug = slugify(entry["name"])
        if slug in wanted and wanted[slug] != entry:
            raise SyncError(
                f"two organizations collide on the filename {slug}.json: "
                f"{wanted[slug]['name']!r} and {entry['name']!r}"
            )
        wanted[slug] = entry

    existing = {p.stem: p for p in OUT_DIR.glob("*.json")}
    stale = [path for slug, path in existing.items() if slug not in wanted]
    return wanted, stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would change without touching any files",
    )
    args = parser.parse_args()

    try:
        contacts = fetch_contacts()
    except SyncError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    entries = [e for e in (to_entry(c) for c in contacts) if e]
    skipped = len(contacts) - len(entries)

    try:
        wanted, stale = plan(entries)
    except SyncError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    added, changed = [], []
    for slug, entry in sorted(wanted.items()):
        path = OUT_DIR / f"{slug}.json"
        body = json.dumps(entry, indent=2, ensure_ascii=False) + "\n"
        if not path.exists():
            added.append(slug)
        elif path.read_text(encoding="utf-8") != body:
            changed.append(slug)
        else:
            continue
        if not args.dry_run:
            path.write_text(body, encoding="utf-8", newline="\n")

    for path in stale:
        if not args.dry_run:
            path.unlink()

    invalidated = False
    if not args.dry_run and (added or changed or stale) and ASTRO_STORE.exists():
        ASTRO_STORE.unlink()
        invalidated = True

    prefix = "would " if args.dry_run else ""
    print(f"{len(contacts)} record(s) from CiviCRM, {len(entries)} publishable")
    if skipped:
        print(f"  skipped {skipped} with no usable name")
    print(f"  {prefix}add:    {', '.join(added) or 'none'}")
    print(f"  {prefix}update: {', '.join(changed) or 'none'}")
    print(f"  {prefix}remove: {', '.join(p.stem for p in stale) or 'none'}")
    if invalidated:
        print("  cleared the Astro content cache so the next build picks these up")
    if not args.dry_run and (added or changed or stale):
        print("\nReview the diff, then commit. Nothing has been pushed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
