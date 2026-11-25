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
with drawn scenes, a six-number stat strip, six numbered grid cards, a
dotted world map with 13 numbered pins, a 21-item "ALSO ON TUESDAY 24
NOV" list, and a red DATE CHECK box. 30 stories in all, across 7
regions.

Every card carries a certainty badge — REPORTED (wires), OFFICIAL (on
the record), CLAIM (one side says) — explained in the footer.

Every story on the page happened or was first reported on Tuesday
24 November 2026, as the named outlets reported it. Stories that look
like 24 November news but are not are listed in the DATE CHECK box
with their real dates, not presented as the day's news.

1. **Drone war** — Russia says it shot down 699 Ukrainian drones
   overnight, 355 aimed at Moscow; a drone strays into Poland and
   NATO sends an AWACS. A strike on Zaporizhzhia kills 2, wounds
   40+. (Reuters, Al Jazeera)
2. **Riyadh tower struck** — Saudi Arabia blames a Houthi drone
   for the second strike in under a week on a tower in the
   financial district. 11 people wounded. (Reuters)
3. **Huawei guilty** — A Brooklyn jury convicts the Chinese
   telecom giant on 10 of 12 counts, and clears it of
   racketeering. (Reuters, WSJ)

Grid: Senegal reinstated as Africa Cup champions (CAS); Zelenskyy
confirms Saturday's strike on the Russian ship Sparta II, saying it
carried weapons (claim unverified); a Gaza strike kills Hamas
security chief Naeem Abu Nahel and six others; Sanofi agrees to buy
Insmed for $41bn; Malaysia will send 6,803 Myanmar nationals back,
1,500 by ship and 5,303 by air; Baghdad takes over Kurdish-held
oilfields.

The ALSO list adds the Eskisehir helicopter crash, Iran's claim of a
fourth tanker hit by a mine in Hormuz, the Hanoi restaurant blast,
Hasina's planned return, the UN's 47,000 women killed by partners, the
Ulleung jet alert, the Bougainville vote, the Taplejung quake, the
Cikande fire toll, the Dow topping 50,000 as the Nasdaq slides, the
world chess match, the UN AI debate, the EU hybrid-car cap, Mexico's
"El Chapo Isidro" trial, WHO staff freed in Ituri after three days
trapped, New York's ban on AI chatbot toys, the UK's nuclear-test
veterans inquiry, Euclid's most distant quasar, Indonesia's VP
candidates, a death sentence for spying in Beijing, and Portugal's
budget vote.

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
