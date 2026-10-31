# GGP-Marketing-Dashboard

- `index.html`: paid-media performance dashboard
- `seo/STRATEGY.md`: **Google + AI-answer (AEO) strategy** for NJ inground pool construction/repair within 50 mi of Hackensack
- `seo/data/service-area-towns.json`: 133 NJ towns, tiered by distance
- `seo/schema/`: LocalBusiness JSON-LD, `llms.txt`, `facts.json` for goodguyspools.com
- `seo/content/`: blog drafts (fill `[[GGP FILL]]` markers before publishing)
- `seo/scripts/aeo_probe.py`: weekly AI share-of-voice measurement (also runs in GitHub Actions if `ANTHROPIC_API_KEY` secret is set)
- `.claude/agents/` + `.claude/skills/seo-weekly/`: the SEO/AEO agent team. In Claude Code, run `/seo-weekly`.
- `reviews-site/`: goodguyspoolsreviews.com static review hub (`python3 reviews-site/build.py`)
