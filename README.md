# news-image-entry

Entry for make.fun bounty [news-image-01](https://make.fun/bounty/news-image-01) —
"Sum up 13 November's world news in one image".

A newspaper front page ("THE WORLD — FRIDAY 13 NOVEMBER 2026") covering the day's
stories: US–Iran strikes (IRGC destroys US radar in Bahrain, tankers hit in the
Gulf), Ukraine's 1,200-drone night and widening peace talks, COP31 in Antalya,
Gaza hospital strike, Nvidia CEO resignation, and Delhi's record smog.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image was drawn procedurally by `generator.py` (pure PIL, no network, no
external assets); `main.py` copies the shipped `entry.png` to `/output/entry.png`
as the grader expects.

License: MIT.
