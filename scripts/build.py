#!/usr/bin/env python3
"""Build README.md from data/links.csv.

The CSV is the single source of truth. This script validates it and
regenerates README.md. It never edits any other file.
"""

import sys
from datetime import date, timezone, datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "links.csv"
README_PATH = ROOT / "README.md"

# Repository coordinates, used for badges and the live-site link.
REPO_SLUG = "Reconnaishawnce/fitd-physical-redteam"
PAGES_URL = "https://reconnaishawnce.github.io/fitd-physical-redteam/"

CATEGORY_EMOJI = {
    "Incidents in the Wild": "🎯",
    "Tradecraft & Methodology": "🛠️",
    "Engagements & Lessons Learned": "📓",
    "Legal, Authorization & Liability": "⚖️",
    "Tools & Gear": "🧰",
    "Detection & Defense": "🛡️",
    "Talks, Reports & Case Studies": "🎤",
    "Reference & Communities": "🔗",
}

CATEGORIES = [
    "Incidents in the Wild",
    "Tradecraft & Methodology",
    "Engagements & Lessons Learned",
    "Legal, Authorization & Liability",
    "Tools & Gear",
    "Detection & Defense",
    "Talks, Reports & Case Studies",
    "Reference & Communities",
]

ACTOR_TYPES = [
    "Nation-state",
    "Criminal",
    "Corporate",
    "Insider",
    "Hacktivist",
    "Authorized red team",
    "Unknown",
]

TECHNIQUES = [
    "Tailgating",
    "Impersonation/Pretext",
    "Covert entry",
    "Media drop (USB)",
    "Hardware implant",
    "Badge/RFID cloning",
    "Insider recruitment",
    "Surveillance/Recon",
    "Dumpster diving",
    "Elicitation",
    "RF/Wireless",
]

VERIFIED_VALUES = {"yes", "no", "partial"}

EXPECTED_COLUMNS = [
    "id", "title", "category", "technique", "actor_type", "attack_id",
    "year", "source", "url", "summary", "tags", "verified", "added",
]


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def split_multi(value):
    """Split a '; '-joined controlled field into clean, non-empty parts."""
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def load_csv():
    if not CSV_PATH.exists():
        fail(f"missing {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    if list(df.columns) != EXPECTED_COLUMNS:
        fail(
            "CSV header mismatch.\n"
            f"  expected: {EXPECTED_COLUMNS}\n"
            f"  found:    {list(df.columns)}"
        )
    return df


def validate(df):
    errors = []
    seen_ids = set()

    for i, row in df.iterrows():
        line = i + 2  # +1 for header, +1 for 0-based index
        rid = row["id"].strip()

        if not rid:
            errors.append(f"row {line}: empty id")
        elif rid in seen_ids:
            errors.append(f"row {line}: duplicate id '{rid}'")
        else:
            seen_ids.add(rid)

        if rid != rid.lower():
            errors.append(f"row {line}: id '{rid}' must be lowercase")

        category = row["category"].strip()
        if category not in CATEGORIES:
            errors.append(f"row {line} ({rid}): invalid category '{category}'")

        for tech in split_multi(row["technique"]):
            if tech not in TECHNIQUES:
                errors.append(f"row {line} ({rid}): invalid technique '{tech}'")

        actor = row["actor_type"].strip()
        if actor and actor not in ACTOR_TYPES:
            errors.append(f"row {line} ({rid}): invalid actor_type '{actor}'")

        url = row["url"].strip()
        if not url:
            errors.append(f"row {line} ({rid}): missing url")
        elif not url.startswith("http"):
            errors.append(f"row {line} ({rid}): url must start with http")

        year = row["year"].strip()
        if year and not (year.isdigit() and len(year) == 4):
            errors.append(f"row {line} ({rid}): year '{year}' must be a 4-digit number or blank")

        verified = row["verified"].strip().lower()
        if verified not in VERIFIED_VALUES:
            errors.append(f"row {line} ({rid}): verified '{row['verified']}' must be yes/no/partial")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        fail(f"validation failed with {len(errors)} error(s)")


def anchor_for(category):
    """Replicate GitHub's heading-anchor slug: lowercase, drop characters that
    are not alphanumeric/space/hyphen, then spaces to hyphens. GitHub does not
    collapse consecutive hyphens, so neither do we."""
    slug = category.strip().lower()
    slug = "".join(c for c in slug if c.isalnum() or c in " -")
    return slug.replace(" ", "-")


def md_escape(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def year_sort_key(row):
    year = row["year"].strip()
    return int(year) if year.isdigit() else -1


def title_cell(row):
    title = md_escape(row["title"])
    url = row["url"].strip()
    cell = f"[{title}]({url})"
    if row["verified"].strip().lower() == "no":
        cell += " `[unverified]`"
    return cell


def render_section(df, category):
    rows = [r for _, r in df.iterrows() if r["category"].strip() == category]
    rows.sort(key=year_sort_key, reverse=True)

    emoji = CATEGORY_EMOJI.get(category, "•")
    lines = [f"## {category}", ""]
    if not rows:
        lines.append(f"{emoji} _No entries yet — [contribute one](CONTRIBUTING.md)._ "
                     "&nbsp;·&nbsp; [↑ Contents](#contents)")
        lines.append("")
        return lines

    plural = "entry" if len(rows) == 1 else "entries"
    lines.append(f"{emoji} _{len(rows)} {plural}_ &nbsp;·&nbsp; [↑ Contents](#contents)")
    lines.append("")

    if category == "Incidents in the Wild":
        lines.append("| Title | Year | Actor | Technique | Summary |")
        lines.append("| --- | --- | --- | --- | --- |")
        for row in rows:
            lines.append(
                f"| {title_cell(row)} | {md_escape(row['year'])} | "
                f"{md_escape(row['actor_type'])} | {md_escape(row['technique'])} | "
                f"{md_escape(row['summary'])} |"
            )
    else:
        lines.append("| Title | Year | Technique | Source | Summary |")
        lines.append("| --- | --- | --- | --- | --- |")
        for row in rows:
            lines.append(
                f"| {title_cell(row)} | {md_escape(row['year'])} | "
                f"{md_escape(row['technique'])} | {md_escape(row['source'])} | "
                f"{md_escape(row['summary'])} |"
            )

    lines.append("")
    return lines


def badge(label, message, color):
    def enc(text):
        return (str(text).replace("-", "--").replace("_", "__").replace(" ", "_"))
    return f"https://img.shields.io/badge/{enc(label)}-{enc(message)}-{color}"


def build_readme(df):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = len(df)
    categories_used = int(df["category"].str.strip().nunique())
    verified_yes = int((df["verified"].str.strip().str.lower() == "yes").sum())

    lines = [
        "<div align=\"center\">",
        "",
        "# 🚪 FITD — Foot in the Door",
        "",
        "### Physical Red Team Reference Guide",
        "",
        "_The physical red-team canon in one searchable, accountability-framed index:_  ",
        "_real incidents · tradecraft · engagement post-mortems · legal footing · gear · defense · talks._",
        "",
        f"[![Entries]({badge('entries', total, 'ff4d4d')})](data/links.csv) "
        f"[![Verified]({badge('verified', f'{verified_yes}/{total}', 'ff8a3d')})](data/links.csv) "
        f"[![Categories]({badge('categories', categories_used, '444')})](#contents) "
        f"[![Build](https://github.com/{REPO_SLUG}/actions/workflows/build.yml/badge.svg)]"
        f"(https://github.com/{REPO_SLUG}/actions/workflows/build.yml) "
        f"[![License]({badge('license', 'MIT', 'blue')})](LICENSE)",
        "",
        f"**[🔎 Browse the live searchable index]({PAGES_URL})** · "
        "**[➕ Add a link](CONTRIBUTING.md)** · "
        "**[📄 Raw CSV](data/links.csv)**",
        "",
        "</div>",
        "",
        "---",
        "",
        "> [!NOTE]",
        "> **This README is generated — do not edit it by hand.** The single source of "
        "truth is [`data/links.csv`](data/links.csv), which GitHub renders as a sortable "
        "table for free. Add a link by appending one row to the CSV (see "
        "[CONTRIBUTING.md](CONTRIBUTING.md)); a GitHub Action re-validates the data and "
        "regenerates this file on every push.",
        "",
        "> [!IMPORTANT]",
        "> Accountability-framed: we do not invent incidents, dates, actors, or "
        "attributions. Every row carries an honest `verified` flag "
        "(✔ `yes` · ◐ `partial` · ✕ `no`) and links a primary or reputable source. "
        "Contested attribution is phrased as reported, not adjudicated.",
        "",
        "## Contents",
        "",
    ]

    for category in CATEGORIES:
        count = int((df["category"].str.strip() == category).sum())
        emoji = CATEGORY_EMOJI.get(category, "•")
        lines.append(f"- {emoji} [{category}](#{anchor_for(category)}) — **{count}**")
    lines.append("")

    for category in CATEGORIES:
        lines.append("---")
        lines.append("")
        lines.extend(render_section(df, category))

    lines.append("---")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append(
        f"**{total} entries** · **{verified_yes} fully verified** · "
        f"last generated **{generated}** (UTC) by "
        "[`scripts/build.py`](scripts/build.py)"
    )
    lines.append("")
    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def main():
    df = load_csv()
    validate(df)
    readme = build_readme(df)
    README_PATH.write_text(readme, encoding="utf-8")
    print(f"OK: wrote {README_PATH} from {len(df)} row(s) in {CSV_PATH.name}")


if __name__ == "__main__":
    main()
