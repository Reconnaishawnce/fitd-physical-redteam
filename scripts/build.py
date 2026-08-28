#!/usr/bin/env python3
"""Build README.md from data/links.csv.

The CSV is the single source of truth. This script validates it and
regenerates README.md. It never edits any other file.
"""

import json
import re
import sys
from datetime import timezone, datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "links.csv"
README_PATH = ROOT / "README.md"
SITE_PATH = ROOT / "docs" / "index.html"

# Repository coordinates, used for badges and the live-site link.
REPO_SLUG = "Reconnaishawnce/fitd-physical-redteam"
PAGES_URL = "https://reconnaishawnce.github.io/fitd-physical-redteam/"

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

LINK_QUALITY_VALUES = {"low", "medium", "high"}

EXPECTED_COLUMNS = [
    "id", "title", "category", "technique", "actor_type", "attack_id",
    "year", "source", "url", "url_secondary", "summary", "tags",
    "link_quality", "added",
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

        url2 = row["url_secondary"].strip()
        if url2 and not url2.startswith("http"):
            errors.append(f"row {line} ({rid}): url_secondary must start with http or be blank")

        year = row["year"].strip()
        if year and not (year.isdigit() and len(year) == 4):
            errors.append(f"row {line} ({rid}): year '{year}' must be a 4-digit number or blank")

        quality = row["link_quality"].strip().lower()
        if quality not in LINK_QUALITY_VALUES:
            errors.append(f"row {line} ({rid}): link_quality '{row['link_quality']}' must be low/medium/high")

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
    url2 = row["url_secondary"].strip()
    if url2:
        cell += f" ([alt source]({url2}))"
    if row["link_quality"].strip().lower() == "low":
        cell += " `[low quality]`"
    return cell


def render_section(df, category):
    rows = [r for _, r in df.iterrows() if r["category"].strip() == category]
    rows.sort(key=year_sort_key, reverse=True)

    lines = [f"## {category}", ""]
    if not rows:
        lines.append("_No entries yet. [Contribute one](CONTRIBUTING.md)._ "
                     "&nbsp;·&nbsp; [Back to contents](#contents)")
        lines.append("")
        return lines

    plural = "entry" if len(rows) == 1 else "entries"
    lines.append(f"_{len(rows)} {plural}_ &nbsp;·&nbsp; [Back to contents](#contents)")
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
    high_quality = int((df["link_quality"].str.strip().str.lower() == "high").sum())

    lines = [
        "<div align=\"center\">",
        "",
        "# FITD · Foot in the Door",
        "",
        "### Physical Red Team Reference Guide",
        "",
        "A curated index of the physical red-team canon: incidents, tradecraft, engagement",
        "post-mortems, legal footing, gear, defense, and talks.",
        "",
        f"[![Entries]({badge('entries', total, '8a2f2f')})](data/links.csv) "
        f"[![High quality]({badge('high quality', f'{high_quality}/{total}', 'a6741c')})](data/links.csv) "
        f"[![Categories]({badge('categories', categories_used, '6d6558')})](#contents) "
        f"[![Build](https://github.com/{REPO_SLUG}/actions/workflows/build.yml/badge.svg)]"
        f"(https://github.com/{REPO_SLUG}/actions/workflows/build.yml) "
        f"[![License]({badge('license', 'MIT', '3f7d52')})](LICENSE)",
        "",
        f"**[Browse the searchable index]({PAGES_URL})** · "
        "**[Add a link](CONTRIBUTING.md)** · "
        "**[Raw CSV](data/links.csv)**",
        "",
        "</div>",
        "",
        "---",
        "",
        "The single source of truth is [`data/links.csv`](data/links.csv), which GitHub also "
        "renders as a sortable table. Add a resource by appending one row to the CSV; see "
        "[CONTRIBUTING.md](CONTRIBUTING.md). This README is generated by "
        "[`scripts/build.py`](scripts/build.py) and rebuilt on every push, so don't edit it by "
        "hand. The `link_quality` column rates the linked source as a citation: "
        "`high` (primary/official), `medium` (reputable secondary), or `low`.",
        "",
        "## Contents",
        "",
    ]

    for category in CATEGORIES:
        count = int((df["category"].str.strip() == category).sum())
        lines.append(f"- [{category}](#{anchor_for(category)}) &nbsp;·&nbsp; **{count}**")
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
        f"**{total} entries** · **{high_quality} high-quality sources** · "
        f"last generated **{generated}** (UTC) by "
        "[`scripts/build.py`](scripts/build.py)"
    )
    lines.append("")
    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


SITE_DATA_RE = re.compile(
    r'(<script id="fitd-data" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)


def inject_site_data(df):
    """Embed the dataset as JSON in docs/index.html so the page needs no fetch
    and works on GitHub Pages (root or /docs), locally, or from the raw file."""
    if not SITE_PATH.exists():
        return False
    html = SITE_PATH.read_text(encoding="utf-8")
    if not SITE_DATA_RE.search(html):
        print(f"WARN: no data marker in {SITE_PATH}; skipping embed", file=sys.stderr)
        return False
    records = df.to_dict(orient="records")
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    # Guard against breaking out of the <script> block.
    payload = payload.replace("</", "<\\/")
    new_html = SITE_DATA_RE.sub(lambda m: m.group(1) + payload + m.group(3), html)
    if new_html != html:
        SITE_PATH.write_text(new_html, encoding="utf-8")
    return True


def main():
    df = load_csv()
    validate(df)
    readme = build_readme(df)
    README_PATH.write_text(readme, encoding="utf-8")
    embedded = inject_site_data(df)
    where = f" and embedded data in {SITE_PATH.name}" if embedded else ""
    print(f"OK: wrote {README_PATH.name} from {len(df)} row(s) in {CSV_PATH.name}{where}")


if __name__ == "__main__":
    main()
