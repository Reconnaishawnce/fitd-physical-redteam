# Contributing to FITD

FITD is a curated reference guide for physical red teams. The entire dataset
lives in one file: [`data/links.csv`](data/links.csv). Everything else
(the README table, exports) is generated from it. **You add a link by appending
one row to that CSV.** Do not edit `README.md` by hand; it is regenerated on
every push.

## How to add a link

1. Open [`data/links.csv`](data/links.csv).
2. Append one row using the column order below.
3. Run `python scripts/build.py` locally (optional) to regenerate `README.md`
   and confirm your row validates.
4. Open a pull request. The GitHub Action re-runs validation and regenerates
   the README; if validation fails, the check fails.

## Column reference

The header, in exact order:

```
id,title,category,technique,actor_type,attack_id,year,source,url,summary,tags,link_quality,added
```

| Field | Rule |
| --- | --- |
| `id` | Stable, unique, lowercase slug. Used for dedup. e.g. `coalfire-dallas-county`. |
| `title` | Display title of the resource. |
| `category` | Exactly one value from the Categories list below. |
| `technique` | Zero or more Techniques, joined with `; `. |
| `actor_type` | One Actor Type, for Incidents only. Blank otherwise. |
| `attack_id` | Optional MITRE ATT&CK id (e.g. `T1200`) where one genuinely applies. Blank if none fits; do not force a mapping. |
| `year` | 4-digit year of the event or publication, or blank. Used for sorting. |
| `source` | Publisher or org (e.g. `IEEE S&P`, `DOJ`, `404 Media`). |
| `url` | Full `https` URL. **Required**; a row with no URL is invalid. |
| `summary` | One or two plain sentences. No hype. |
| `tags` | Freeform, joined with `; `. |
| `link_quality` | `high` (primary/official source), `medium` (reputable secondary), or `low` (blog, forum, unconfirmed). Rates the link as a citation. |
| `added` | ISO date `YYYY-MM-DD`. |

Wrap any field that contains a comma in double quotes (standard CSV).

## Categories (controlled)

1. Incidents in the Wild
2. Tradecraft & Methodology
3. Engagements & Lessons Learned
4. Legal, Authorization & Liability
5. Tools & Gear
6. Detection & Defense
7. Talks, Reports & Case Studies
8. Reference & Communities

## Actor types (controlled, incidents only)

`Nation-state`, `Criminal`, `Corporate`, `Insider`, `Hacktivist`,
`Authorized red team`, `Unknown`

## Techniques (controlled)

`Tailgating`, `Impersonation/Pretext`, `Covert entry`, `Media drop (USB)`,
`Hardware implant`, `Badge/RFID cloning`, `Insider recruitment`,
`Surveillance/Recon`, `Dumpster diving`, `Elicitation`, `RF/Wireless`

## Accuracy guardrails

This repo is accountability-framed. **Do not invent incidents, dates, actors,
or attributions.**

- Only add a row if you have a real, working `url` to a primary or clearly
  reputable source.
- If you cannot confirm a detail against the linked source, set `link_quality`
  to `medium` or `low` and keep the summary conservative. Do not assert.
- Attribution for nation-state activity is often "widely reported" rather than
  adjudicated. Phrase summaries accordingly; do not state contested attribution
  as settled fact.
- Prefer primary sources (court records, agency releases, the actual paper or
  report) over secondary coverage.

## Validation rules enforced by `build.py`

- `id` is unique, non-empty, and lowercase.
- `category` is in the controlled list.
- Every `technique` value is in the controlled list.
- Every non-blank `actor_type` is in the controlled list.
- `url` is present and starts with `http`.
- `year` is a 4-digit number or blank.
- `link_quality` is one of `low`, `medium`, `high`.

Rows flagged `link_quality: low` are rendered with a trailing `[low quality]`
marker so citation strength stays visible.
