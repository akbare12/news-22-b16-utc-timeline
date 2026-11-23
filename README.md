# The World in One Day — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b16-utc-timeline/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b16-utc-timeline/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up Sunday 22 November 2026: 36 stories
across 7 regions, built around a 24-hour UTC timeline — from the overnight
drone barrage over Ukraine, through the Hong Kong polls and the COP31 collapse,
to the Bahrain radar claim in the evening.

The day's three biggest stories lead the page: **COP31 collapses with no deal**
in Antalya, **Russia fires 186 drones at Ukraine — 161 shot down or jammed**,
and **Iran's claim that two US Patriot radars were hit in Bahrain** (labelled
CLAIM: Bahrain denies a military strike). A kanon number strip (186 / 161 /
720/9 / 98.79% / $120bn / 35% / 44h / 50 / 258), a region bar with story counts,
a world map with 36 numbered pins, and a red **DATE CHECK** box close the page:
every story is dated to Sunday 22 November, with earlier events (the 400-drone
barrage, El Chapo Isidro, BepiColombo, the Hormuz tankers) explicitly left out
and unresolved items (the Dymer final toll, four uncalled House races, the
EU–Indonesia date split) listed as NOT YET.

## How it is built

`draw.py` (Pillow, standard library only in the entry program) draws the page
at 1024×1024 and writes `entry.png`. `main.py` copies that image to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy (PNG header, 1024×1024
dimensions, sha256, size under 1 MiB). It never writes anything next to itself.

## Sources

AP · Reuters · BBC · CNN · Guardian · France 24 · Al Jazeera · Yonhap · Anadolu ·
Detiknews · WHO · SpaceX. Certainty chips: CONFIRMED = 2+ outlets; REPORTED =
carried by the wires today; CLAIM = one side, unverified; OFFICIAL = recorded
result; FORECAST = not yet decided. Scenes are drawn illustrations, not
photographs.

<!-- SPDX-License-Identifier: MIT -->
