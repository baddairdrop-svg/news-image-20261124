# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/baddairdrop-svg/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/baddairdrop-svg/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A program that draws one image summing up the world's news of
Tuesday 24 November 2026, for the make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124),
entered by **@badd-airdrop2**.

## The image

"THE WORLD IN ONE DAY": the page is one day running midnight to
midnight, 1024x1024. A black masthead, a region-count strip, a
four-block timeline spine (00-06 / 06-12 / 12-18 / 18-24 UTC) with a
red dot on each story that carries a reported time, three hero cards
with drawn scenes, a five-number stat strip, a six-card grid numbered
4-9, a dotted world map with numbered pins, and a red DATE CHECK box.

Every story on the page happened or was first reported on Tuesday
24 November 2026, as the named outlets reported it. Stories that look
like 24 November news but are not are listed in the DATE CHECK box
with their real dates, not presented as the day's news.

1. **Riyadh tower struck** — A Houthi drone hits the PIF Tower,
   the capital's tallest, a second strike in less than a week.
   11 people wounded. (Reuters)
2. **Zaporizhzhia struck overnight** — A Russian attack kills 2
   and wounds 40, including four children. (Reuters)
3. **Huawei guilty** — A Brooklyn jury convicts the Chinese
   telecom giant on 10 of 12 counts. (Reuters, WSJ)

Grid: Senegal reinstated as Africa Cup champions (CAS); Zelenskyy
confirms Ukraine's strike on the Russian ship Sparta II; a Gaza
strike kills Hamas security chief Naeem Abu Nahel and six others;
Sanofi agrees to buy Insmed for $41bn; a Turkish Air Force
helicopter crashes in Eskisehir, killing 5; Iran says four tankers
hit mines in the Strait of Hormuz, a claim the maritime centre says
is unverified.

No quotes, numbers or faces are invented, and no real person is drawn.
Map and drawings are original vector art.

## How it runs

`main.py` is pure Python 3 standard library only (no network, no fonts
on disk, no randomness, no clock). It draws the picture with a small
5x7 bitmap font and a hand-written PNG encoder, and writes it to
`/output/entry.png`. Running it twice writes the same bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
