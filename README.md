# news-image-20261124 — The World Today

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ayilinalin/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ayilinalin/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124): a program that writes one image to `/output/entry.png`.

## The image

A front page for **Tuesday 24 November 2026**, drawn from scratch with PIL
(`draw.py`, geometric shapes only, no photos, no network):

- **Headline — Kyiv region:** eleven dead in Dymer after a Russian drone
  strike hit flats; a boy of 7 was pulled alive after 22 hours under the
  rubble, and two people are still unaccounted for.
- **Libya:** Ukraine says sea drones sank the Russian corvette Merkury at
  Benghazi and hit a cargo ship and a helicopter.
- **Indonesia:** 24 dead in the factory fire in Cikande, Banten; about 30
  workers are still missing as the search goes on.
- **India & Nepal:** a new train links Ayodhya and Janakpur; Modi and PM
  Shah sign eight deals and a Rs 15,000-crore package.
- **Geneva:** the World Chess Championship begins — champion Gukesh, 20,
  meets challenger Sindarov, 20, in Game 1.
- **Also today:** Seoul's cabinet reshuffle, the Oxfam report on Gaza's
  contamination, and Lisbon's budget-vote rally.

## Run

```sh
python3 draw.py          # regenerate entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

`main.py` uses only the Python standard library. It copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, checks the PNG magic, the 1 MiB size cap
and the 1024x1024 cap, and verifies the copy is byte-identical (sha256)
with mode 0644. Two runs produce identical bytes.

## License

MIT — see [LICENSE](LICENSE).
