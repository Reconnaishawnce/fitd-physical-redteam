<div align="center">

# 🚪 FITD — Foot in the Door

### Physical Red Team Reference Guide

_The physical red-team canon in one searchable, accountability-framed index:_  
_real incidents · tradecraft · engagement post-mortems · legal footing · gear · defense · talks._

[![Entries](https://img.shields.io/badge/entries-6-ff4d4d)](data/links.csv) [![Verified](https://img.shields.io/badge/verified-3/6-ff8a3d)](data/links.csv) [![Categories](https://img.shields.io/badge/categories-4-444)](#contents) [![Build](https://github.com/Reconnaishawnce/fitd-physical-redteam/actions/workflows/build.yml/badge.svg)](https://github.com/Reconnaishawnce/fitd-physical-redteam/actions/workflows/build.yml) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**[🔎 Browse the live searchable index](https://reconnaishawnce.github.io/fitd-physical-redteam/)** · **[➕ Add a link](CONTRIBUTING.md)** · **[📄 Raw CSV](data/links.csv)**

</div>

---

> [!NOTE]
> **This README is generated — do not edit it by hand.** The single source of truth is [`data/links.csv`](data/links.csv), which GitHub renders as a sortable table for free. Add a link by appending one row to the CSV (see [CONTRIBUTING.md](CONTRIBUTING.md)); a GitHub Action re-validates the data and regenerates this file on every push.

> [!IMPORTANT]
> Accountability-framed: we do not invent incidents, dates, actors, or attributions. Every row carries an honest `verified` flag (✔ `yes` · ◐ `partial` · ✕ `no`) and links a primary or reputable source. Contested attribution is phrased as reported, not adjudicated.

## Contents

- 🎯 [Incidents in the Wild](#incidents-in-the-wild) — **2**
- 🛠️ [Tradecraft & Methodology](#tradecraft--methodology) — **1**
- 📓 [Engagements & Lessons Learned](#engagements--lessons-learned) — **1**
- ⚖️ [Legal, Authorization & Liability](#legal-authorization--liability) — **0**
- 🧰 [Tools & Gear](#tools--gear) — **0**
- 🛡️ [Detection & Defense](#detection--defense) — **0**
- 🎤 [Talks, Reports & Case Studies](#talks-reports--case-studies) — **0**
- 🔗 [Reference & Communities](#reference--communities) — **2**

---

## Incidents in the Wild

🎯 _2 entries_ &nbsp;·&nbsp; [↑ Contents](#contents)

| Title | Year | Actor | Technique | Summary |
| --- | --- | --- | --- | --- |
| [Huawei drone surveillance in the TDC 5G contract fight](https://www.bloomberg.com/news/features/2023-06-15/how-huawei-got-caught-spying-and-lost-a-200-million-5g-contract) | 2019 | Corporate | Surveillance/Recon | During the fight over TDC's ~EUR 200M 5G contract, a large drone was reportedly seen scanning an investigation room whiteboard in Copenhagen and later monitoring TDC's executive team before descending into a waiting van. Reported by Bloomberg as part of an alleged Huawei espionage effort; Huawei denies involvement, so attribution is reported rather than adjudicated. |
| [Stuxnet and the air-gap USB vector](https://archive.org/details/w32_stuxnet_dossier) | 2010 | Nation-state | Media drop (USB) | Malware widely reported to have reached air-gapped industrial systems via removable media. Illustrates a physical introduction vector into an isolated network; specific attribution is widely reported rather than adjudicated. |

---

## Tradecraft & Methodology

🛠️ _1 entry_ &nbsp;·&nbsp; [↑ Contents](#contents)

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [Users Really Do Plug in USB Drives They Find](https://elie.net/publication/users-really-do-plug-in-usb-drives-they-find/) | 2016 | Media drop (USB) | IEEE S&P | Field study that dropped 297 USB drives on a university campus and measured how many were plugged in; a large share were. Empirical basis for USB drop tradecraft. |

---

## Engagements & Lessons Learned

📓 _1 entry_ &nbsp;·&nbsp; [↑ Contents](#contents)

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [Coalfire pentesters arrested at Dallas County Courthouse](https://www.theregister.com/2019/09/13/pentest_arrest_coalfire/) | 2019 | Covert entry | The Register | Two Coalfire operators were arrested during an authorized physical penetration test of the Dallas County, Iowa courthouse; charges were later dropped and the county reached a settlement. A canonical lessons-learned case on scope, authorization, and law-enforcement contact. |

---

## Legal, Authorization & Liability

⚖️ _No entries yet — [contribute one](CONTRIBUTING.md)._ &nbsp;·&nbsp; [↑ Contents](#contents)

---

## Tools & Gear

🧰 _No entries yet — [contribute one](CONTRIBUTING.md)._ &nbsp;·&nbsp; [↑ Contents](#contents)

---

## Detection & Defense

🛡️ _No entries yet — [contribute one](CONTRIBUTING.md)._ &nbsp;·&nbsp; [↑ Contents](#contents)

---

## Talks, Reports & Case Studies

🎤 _No entries yet — [contribute one](CONTRIBUTING.md)._ &nbsp;·&nbsp; [↑ Contents](#contents)

---

## Reference & Communities

🔗 _2 entries_ &nbsp;·&nbsp; [↑ Contents](#contents)

| Title | Year | Technique | Source | Summary |
| --- | --- | --- | --- | --- |
| [MITRE ATT&CK T1200: Hardware Additions](https://attack.mitre.org/techniques/T1200/) | 2018 | Hardware implant | MITRE ATT&CK | ATT&CK reference page for introducing computer accessories, networking hardware, or devices into a system or network as an initial-access vector. |
| [MITRE ATT&CK T1091: Replication Through Removable Media](https://attack.mitre.org/techniques/T1091/) | 2017 | Media drop (USB) | MITRE ATT&CK | ATT&CK reference page for moving onto systems, including air-gapped networks, by copying malware to removable media. |

---

<div align="center">

**6 entries** · **3 fully verified** · last generated **2026-08-28** (UTC) by [`scripts/build.py`](scripts/build.py)

</div>
