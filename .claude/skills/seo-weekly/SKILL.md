---
name: seo-weekly
description: Weekly Good Guys Pools SEO/AEO run. Measures AI share of voice, audits citations, syncs reviews, drafts next content and GBP post, and writes one summary report.
---
Run in order, using the subagents in `.claude/agents/`:
1. `aeo-visibility-auditor`: share-of-voice report.
2. `citation-nap-auditor`: only on the first run of each month, or if step 1 found a listing issue.
3. `review-curator`: ingest new reviews (ask the user to paste or export new reviews if none were provided), rebuild the hub.
4. `local-content-writer`: draft the next item in the STRATEGY.md §3d queue, or the top gap from step 1.
5. `gbp-post-writer`: if the user supplied a project update.
6. `backlink-prospector`: first run of each month only.
Finish with `seo/reports/weekly-YYYY-MM-DD.md`: the KPI table from STRATEGY.md §9 with this week's numbers, what changed, and the 3 actions that need a human (with exact steps). Lead with the worst news.
