# Good Guys Pools — Search & AI-Answer Dominance Plan (North NJ, 50 mi of Hackensack)

**Goal:** Good Guys Pools (GGP) is the company Google, Google AI Overviews / AI Mode, ChatGPT, Gemini, Perplexity, Claude, Copilot and Siri recommend when anyone in NJ within 50 miles of Hackensack asks about **in-ground pool construction, renovation, or repair**.

**Owner of record for every claim in this repo:** GGP. Nothing here invents reviews, projects, prices, credentials, or awards. Every `[[GGP FILL]]` marker means "real company data required" — the agents in `.claude/agents/` refuse to publish content containing one.

---

## 0. Read this first: the hard truths

1. **"#1 on Google across a 50-mile radius" is three different games, and you can only fully win two.**
   - **Map pack (the 3 listings with the map):** ranks heavily on *proximity to the searcher*. One Hackensack address will not hold #1 in the Map Pack for "pool builder near me" when the searcher is in Princeton (48 mi) or Sparta (34 mi). Nobody wins that with one location, and fake addresses or virtual offices get Google Business Profiles suspended. **Realistic target: Map Pack top 3 in Tier-1 towns (0–12 mi, 56 towns).**
   - **Organic blue links:** winnable across the whole radius with genuinely useful town and project pages.
   - **AI answers:** these are *entity + consensus* games, not proximity games. This is where GGP can win the entire 50 miles, and where competitors are not playing yet. **This is the main bet.**

2. **Your citations are currently broken, and that is the #1 thing holding back AI answers.** From public listings found during the audit (Oct 31, 2026):
   | Source | Problem found |
   |---|---|
   | Yelp (`good-guys-hackensack-3`) | Listed as **"Closed"**, name "Good Guys", address shown as **86110 Orchard St**, 3.0★ / 2 reviews |
   | Houzz | Location shown as **"Hackensack, NY"** |
   | HomeAdvisor | **"South Hackensack, NJ"** |
   | Website | "Based on 30 reviews" (self-reported widget) |
   | BuildZoom | "Good Guys Pools LLC", Hackensack, licenses 13VH14082500 / 13VH13660100 |

   When an LLM sees "Closed," "NY," and three addresses, it lowers its confidence and recommends whoever it has a cleaner picture of. **Fix this before any content work.** (Agent: `citation-nap-auditor`.)

3. **The review site cannot look like Google.** See §6. The short version: copying Google's trade dress plus presenting a company-run site as neutral breaks the FTC's Consumer Review rule (16 CFR Part 465, in force since Oct 2024; civil penalties of $50k+ *per violation*). It also hands Google a reason to treat GGP's *main* domain as spam. I built it as a disclosed, independently designed review hub instead. It still captures the "Good Guys Pools reviews" search and feeds AI models a clean consensus signal.

---

## 1. Canonical entity (single source of truth)

Every listing, schema block, llms.txt and press mention must match **character for character**:

```
Name:     Good Guys Pools                 [[GGP FILL: confirm whether "LLC" is used publicly]]
Address:  [[GGP FILL: exact street, e.g. 86 Orchard St]], Hackensack, NJ [[ZIP]]
Phone:    [[GGP FILL: (201) xxx-xxxx]]   (one tracking-free number everywhere)
Website:  https://goodguyspools.com/
Category: Swimming Pool Contractor (primary); Swimming Pool Repair Service; Pool Cleaning Service (only if offered)
License:  NJ HIC 13VH14082500 / 13VH13660100   [[GGP FILL: confirm active on NJ DCA lookup]]
Founded:  [[GGP FILL]]   Experience claim: "25+ years" (from existing listings; confirm)
Area:     NJ only — see seo/data/service-area-towns.json (133 towns, 13 counties)
```

`seo/schema/organization.jsonld` holds the machine-readable version. `sameAs` must list every real profile.

---

## 2. The signal map: what drives each answer surface

| Surface | What it actually reads | GGP lever |
|---|---|---|
| **Google Map Pack** | GBP category, proximity, review count/velocity/recency, review *text keywords*, photos, GBP posts, NAP consistency, website relevance | GBP program (§4), review velocity (§5) |
| **Google organic** | Helpful, first-hand content, links, local relevance, page experience | Town pages, project pages, cost data (§3) |
| **Google AI Overviews / AI Mode** | Google index + Knowledge Graph + GBP + reviews + "consensus" across third-party pages (listicles, Reddit, Houzz, Yelp) | Entity consistency, third-party mentions, Q&A-shaped pages |
| **ChatGPT (search)** | Mostly the **Bing** index + Bing Places, plus listicles and Reddit | **Bing Places + Bing Webmaster Tools** (most competitors skip this) |
| **Gemini** | Google stack + **YouTube transcripts** heavily | Project videos with spoken town + service names |
| **Perplexity** | Live web, favors fresh, well-structured pages with clear facts/numbers | Cost index, dated updates, tables |
| **Siri / Apple Intelligence / Apple Maps** | **Apple Business Connect**, Yelp | Claim Apple Business Connect; fix Yelp |
| **Claude / Copilot** | Web search (Brave/Bing) | Same as ChatGPT |
| **AI agents booking on a user's behalf** (Google "Ask for Me" calls, ChatGPT/Gemini agents) | Phone answer quality, structured offers, booking endpoints | §7 "agent-ready business" |

---

## 3. Content architecture (main site: goodguyspools.com)

### 3a. Money pages (one per service, NJ-scoped)
- `/inground-pool-construction-nj/` — gunite, vinyl, fiberglass [[GGP FILL: which ones GGP builds]]
- `/pool-renovation-nj/` — resurfacing, tile/coping, re-plaster, liner replacement
- `/pool-repair-nj/` — leak detection, equipment, structural cracks
- `/pool-cost-north-jersey/` — **the cost index (§3c). This is the page AIs will quote.**

Each page opens with a **40–60 word answer block** (who/what/where/price range), followed by an FAQ section (with `FAQPage` schema), a short "how we work" list, and real project photos with geotagged EXIF.

### 3b. Town pages — tiered, never thin
Driven by `seo/data/service-area-towns.json`:
- **Tier 1 (0–12 mi, 56 towns):** full page per town. Every page must contain at least one *real* GGP project in or near that town (photos, scope, timeline), that town's permit/zoning notes (setback, fence/barrier, lot coverage, from the municipal code), and a local review. **No project = no page.** Publish as projects happen.
- **Tier 2 (12–25 mi, 40 towns):** county-level hub pages (Morris, Passaic, Essex...) listing towns served, upgraded to town pages once a project exists.
- **Tier 3 (25–50 mi, 37 towns):** county hubs only. Thin "pool builder in {town}" doorway pages are a Google spam-policy violation and would damage the whole domain.

### 3c. Original data: the "North Jersey Pool Cost Index" (pioneer tactic)
AI answers need *numbers* to quote, and today they quote national averages from Angi or HomeGuide. GGP has real NJ job data. Publish:
- Median and range by pool type (gunite / vinyl / fiberglass), by county, by add-on (spa, auto cover, retaining walls, rock removal, which is common in Passaic/Morris)
- Permit timelines by municipality (from GGP's own permit history)
- Updated each January with a dated changelog

Release it as an HTML table, a downloadable CSV, and a `Dataset` JSON-LD block. Pitch it to NorthJersey.com / The Record, Patch, NJ Monthly, and local real-estate agents. **Being the source of the number is the single most durable AEO position there is.** It earns links, AI citations, and press at the same time.

### 3d. Blog / answer content
Drafts in `seo/content/`. Each post answers one real query in the first paragraph, is written in first person from GGP's crew ("On a Wyckoff build last spring we hit ledge rock at 4 ft..."), and carries an author byline with credentials (E-E-A-T).

Priority queue (from your top-performing paid keywords in "Google Keywords" sheet, plus AI-prompt research):
1. How much does an inground pool cost in North Jersey? (→ cost index)
2. Inground pool permits in Bergen County: what to expect (draft included)
3. Pool repair vs. renovation vs. rebuild: how to tell (draft included)
4. Gunite vs. vinyl vs. fiberglass in NJ freeze-thaw climate
5. How to choose a pool builder in NJ: 12 questions to ask (draft included; makes GGP the "framework" AIs quote)
6. When to open/close a pool in North Jersey
7. Pool resurfacing: signs, cost, timeline in NJ
8. Best time of year to build an inground pool in NJ (off-season booking → winter leads)

---

## 4. Google Business Profile program
- Primary category **Swimming pool contractor**. Add secondary categories only for services actually offered.
- **Service areas:** NJ towns only, and no more than 20 (Google's cap). Use Tier-1 towns.
- **Weekly GBP post** (agent `gbp-post-writer`): one real project, naming the town and service. Geotagged photos.
- **Products/Services section:** each service with a price range taken from the cost index.
- **Q&A:** seed with real customer questions, answered by the owner.
- **Photos:** 10+/month, real jobs, before/after.
- Respond to **every** review within 48h, mentioning service + town naturally.

## 5. Review engine (the biggest Map Pack lever)
- **Target velocity:** 6–10 new Google reviews/month, steady. Spikes look like manipulation.
- **Ask everyone, not just happy customers.** Selective asking ("review gating") violates Google policy and the FTC rule.
- **Ask at three moments:** dig day, water fill, first swim.
- **The ask** (SMS, QR code on the truck and the final invoice): *"Would you share an honest review on Google? If you mention what we did (new pool, renovation, repair) and your town, it helps neighbors find us."* Asking for *detail* is fine. Scripting the wording or offering incentives is not.
- Then cross-post: ask a share of customers for Houzz / Yelp / Bing / Facebook. AI consensus rewards the same company being praised in many places.
- Every 5-star review (with permission) flows into the review hub (§6) via `reviews-site/reviews.json`.

## 6. goodguyspoolsreviews.com: the compliant version
**What you asked for:** Google-branded look, amalgamation of 5-star reviews.
**What I built:** `reviews-site/`, an independently branded, mobile-first review hub that:
- shows only real reviews, each with its source platform, date, and a link to the original;
- states plainly at the top: "Operated by Good Guys Pools. Reviews are reproduced from public platforms with links to the originals";
- also shows the *overall* platform rating and count (including non-5-star) so it never misrepresents the full picture;
- carries `Organization` + `ItemList` schema and links back to the main site, GBP, and each platform.

**Why not Google-styled:**
1. **FTC 16 CFR §465.6:** a company-controlled site that presents itself as an independent review source is a per-violation civil-penalty offense.
2. **§465.7 (review suppression / misrepresentation):** showing only 5-stars as if they were the full picture is risky. Showing the full platform totals alongside fixes that.
3. **Google trademark / trade dress:** Lanham Act exposure, plus Google can and does act against sites that impersonate its UI.
4. **SEO reality:** Google's site-reputation and spam systems are trained to catch exactly that pattern. If it is caught, the penalty can reach the main domain through the links between them.
5. Self-serving review stars (`AggregateRating` on your own business) have not shown in Google results since 2019, so a fake-Google look would not even get star snippets.

**Why the honest version still works:** it ranks for "Good Guys Pools reviews" and "{town} pool builder reviews." It gives LLMs one clean, crawlable page of real praise tied to specific towns and services, and the outbound links to Google, Houzz and Yelp reinforce those profiles.

## 7. Pioneer tactics (12–24 months ahead of local competitors)
1. **llms.txt + `/ai/facts.json`**: a plain-language and a machine-readable fact sheet (services, area, license, pricing ranges, warranty, process) at stable URLs. Templates are in `seo/schema/`. AI crawlers increasingly fetch these. Cost is zero, and it removes any guessing.
2. **Agent-ready business:**
   - Google's "Ask for Me" / AI calling assistants phone local businesses for quotes. Train whoever answers the phone to give a price *range* and the next available consult date to an AI caller. Log these calls.
   - Add `potentialAction: RequestQuoteAction/ReserveAction` schema plus a simple, stable quote-request endpoint so AI agents can book a consult without scraping a form.
   - Later: publish a small public MCP server ("GGP quote & availability") so assistants that support MCP can check availability directly. Cheap to build, and almost no local contractor has one.
3. **Answer-shaped everything:** every page starts with the answer, uses question H2s, tables for comparisons, and dated "last updated" stamps. LLM retrieval chunks reward self-contained 100–300 word sections.
4. **YouTube project log:** one 60–120 sec video per build, saying out loud *"inground gunite pool in Franklin Lakes, New Jersey"*. Gemini and AI Overviews cite YouTube transcripts. Post as Shorts too.
5. **Third-party consensus:** AI "best pool builder in Bergen County" answers are built from listicles, Reddit, Houzz and Nextdoor. Plan:
   - Get legitimately listed in every "best pool builders NJ" roundup. Outreach is in agent `backlink-prospector`. **Never pay for fake placements.**
   - Houzz: fix the location, add 20+ project photos, ask 10 clients for Houzz reviews.
   - Reddit (r/newjersey, r/pools, r/HomeImprovement): an owner account with disclosed affiliation, answering pool questions helpfully. No astroturfing; Reddit and Google both detect it, and it destroys trust.
6. **Bing Places + Apple Business Connect + Bing Webmaster Tools + IndexNow**: this feeds ChatGPT, Copilot and Siri. Most local competitors have none of it.
7. **Wikidata / Knowledge Graph:** only once real press coverage exists (the cost index makes that likely). Then create a Wikidata item citing it, which locks in the entity.
8. **AI share-of-voice tracking:** `seo/scripts/aeo_probe.py` asks AI models 40+ real buyer prompts across towns weekly and logs whether GGP is named, its position, and which competitors are. This is the KPI that matters. Rankings alone no longer tell you if you are winning.

## 8. Backlinks (legitimate only)
Ordered by value:
1. Local press for the cost index and seasonal stories (The Record, Patch, TAPinto, NJ.com)
2. Supplier/manufacturer dealer pages (Pentair, Hayward, Latham, etc. for any brand GGP is certified with)
3. Chamber of commerce memberships (Hackensack Regional, Bergen County, Ridgewood, Wyckoff, Morris County)
4. Local sponsorships: youth swim teams, town swim clubs (your competitor sheet lists Bogota and Cresskill swim clubs)
5. Real-estate agents and landscapers: co-authored "adding a pool: home value in Bergen County" content
6. Trade associations: NJ Pool & Spa association / PHTA member directory
7. Scholarships are **not** recommended. Google discounts them.

**Never:** PBNs, paid link packages, mass guest posts, or fake directory networks. These are the fastest way to lose everything above.

## 9. KPIs and cadence
| KPI | Baseline (fill) | 90-day | 12-month |
|---|---|---|---|
| Google reviews (count / avg) | [[GGP FILL]] | +25 | +100 |
| Map Pack top-3, Tier-1 towns (grid scan) | [[GGP FILL]] | 40% | 80% |
| AI share-of-voice (aeo_probe, % prompts naming GGP) | run probe | 25% | 60% |
| Organic clicks/mo (GSC) | [[GGP FILL]] | +50% | +200% |
| NAP-consistent citations | ~0 of 6 audited | 100% top 30 | 100% top 60 |
| Referring domains (local/relevant) | [[GGP FILL]] | +10 | +40 |

**Weekly:** run `/seo-weekly` (skill in `.claude/skills/seo-weekly/`). It chains the agents: probe, then content, then GBP post, then review sync, then a report.

## 10. 90-day sequence
- **Weeks 1–2:** fix NAP on Yelp, Houzz, HomeAdvisor, BBB, Facebook, Bing, Apple. Deploy schema, llms.txt and facts.json. Verify GSC + Bing WMT. Run the baseline AI probe.
- **Weeks 2–4:** launch the review engine (SMS + QR). Deploy the review hub. Publish the 3 drafted posts after GGP fills the data markers.
- **Weeks 4–8:** build the cost index from job data. Publish Tier-1 town pages that have real projects. Start the YouTube project log.
- **Weeks 8–12:** cost index press push, listicle/backlink outreach, Reddit presence, a second probe to measure the delta.
