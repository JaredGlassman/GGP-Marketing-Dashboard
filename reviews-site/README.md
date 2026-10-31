# goodguyspoolsreviews.com: review hub

A static site generated from `reviews.json` by `build.py` (Python 3, no dependencies).

```
python3 build.py            # builds dist/ from reviews.json (real data)
python3 build.py --sample   # builds dist/ from reviews.sample.json, with a SAMPLE banner and noindex, for layout checks only
```
Deploy `dist/` to Netlify (see `netlify.toml`), then point goodguyspoolsreviews.com at it.

## Why it isn't styled like Google
It is deliberately an independent design with a disclosure line saying the site is operated by Good Guys Pools. A Google look-alike that presents a company-run site as a neutral review source breaks the FTC Consumer Review rule (16 CFR §465.6) and infringes Google's trade dress. It also risks a spam action that reaches goodguyspools.com. See `seo/STRATEGY.md` §6.

## Adding reviews (`reviews.json` → `reviews[]`)
```json
{"id":"g-2026-08-14-jm","name":"Jane M.","rating":5,"date":"2026-08-14",
 "source":"Google","source_url":"https://g.co/kgs/…","service":"construction",
 "town":"Ridgewood","text":"Exact review text, verbatim."}
```
- `text` must be **verbatim** from the source. Trimming with "…" is allowed. Rewording is not.
- `source` ∈ Google, Houzz, HomeAdvisor, Yelp, Facebook, Trustpilot, Angi, BBB, direct. A `direct` testimonial needs `"consent": true`.
- `service` ∈ construction, renovation, repair, service. `town` only if known, NJ only.
- Only 5★ reviews are shown as cards (that is the point of the hub), but `platform_totals` must hold each platform's **true overall** rating and count. The page displays these, so it never implies the 5★ set is everything.
- The build fails if a review is missing a source, date or rating, or contains a `[[` placeholder.

Fastest way to fill it: export reviews from Google Business Profile (Google Takeout → Business Profile), or paste them into Claude and run the `review-curator` agent.
