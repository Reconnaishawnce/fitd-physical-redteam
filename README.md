# FITD: Foot in the Door

**Physical Red Team Reference Guide**

A curated, sortable reference of links for physical red teams: real-world incidents, tradecraft, engagement lessons, legal footing, gear, defenses, talks, and community references. Accountability-framed — entries carry an honest `verified` flag and link to a primary or reputable source.

> **This file is generated.** Do not edit it by hand. The single source of truth is [`data/links.csv`](data/links.csv), which GitHub also renders as a sortable, searchable table. To add a link, append a row to the CSV — see [CONTRIBUTING.md](CONTRIBUTING.md). A GitHub Action regenerates this README on every push.

## Contents

- [Incidents in the Wild](#incidents-in-the-wild) (1)
- [Tradecraft & Methodology](#tradecraft-methodology) (1)
- [Engagements & Lessons Learned](#engagements-lessons-learned) (1)
- [Legal, Authorization & Liability](#legal-authorization-liability) (0)
- [Tools & Gear](#tools-gear) (0)
- [Detection & Defense](#detection-defense) (0)
- [Talks, Reports & Case Studies](#talks-reports-case-studies) (0)
- [Reference & Communities](#reference-communities) (2)

## Incidents in the Wild

| Title | Year | Actor | Technique | Summary |
| --- | --- | --- | --- | --- |
| [Stuxnet and the air-gap USB vector](https://archive.org/details/w32_stuxnet_dossier) | 2010 | Nation-state | Media drop (USB) | Malware widely reported to have reached air-gapped industrial systems via removable media. Illustrates a physical introduction vector into an isolated network; specific attribution is widely reported rather than adjudicated. |

## Tradecraft & Methodology

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [Users Really Do Plug in USB Drives They Find](https://elie.net/publication/users-really-do-plug-in-usb-drives-they-find/) | 2016 | Media drop (USB) | IEEE S&P | Field study that dropped 297 USB drives on a university campus and measured how many were plugged in; a large share were. Empirical basis for USB drop tradecraft. |

## Engagements & Lessons Learned

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [Coalfire pentesters arrested at Dallas County Courthouse](https://www.theregister.com/2019/09/13/pentest_arrest_coalfire/) | 2019 | Covert entry | The Register | Two Coalfire operators were arrested during an authorized physical penetration test of the Dallas County, Iowa courthouse; charges were later dropped and the county reached a settlement. A canonical lessons-learned case on scope, authorization, and law-enforcement contact. |

## Legal, Authorization & Liability

_No entries yet._

## Tools & Gear

_No entries yet._

## Detection & Defense

_No entries yet._

## Talks, Reports & Case Studies

_No entries yet._

## Reference & Communities

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [MITRE ATT&CK T1200: Hardware Additions](https://attack.mitre.org/techniques/T1200/) | 2018 | Hardware implant | MITRE ATT&CK | ATT&CK reference page for introducing computer accessories, networking hardware, or devices into a system or network as an initial-access vector. |
| [MITRE ATT&CK T1091: Replication Through Removable Media](https://attack.mitre.org/techniques/T1091/) | 2017 | Media drop (USB) | MITRE ATT&CK | ATT&CK reference page for moving onto systems, including air-gapped networks, by copying malware to removable media. |

---

_5 entries. Last generated 2026-08-28 (UTC) by `scripts/build.py`._
