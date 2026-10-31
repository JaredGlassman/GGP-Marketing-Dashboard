#!/usr/bin/env python3
"""Build the goodguyspoolsreviews.com static site from reviews.json."""
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SAMPLE = "--sample" in sys.argv
SRC = HERE / ("reviews.sample.json" if SAMPLE else "reviews.json")
DIST = HERE / "dist"
SITE = "https://goodguyspoolsreviews.com/"
SERVICES = {"construction": "New pool", "renovation": "Renovation", "repair": "Repair", "service": "Service"}
SOURCES = {"Google", "Houzz", "HomeAdvisor", "Yelp", "Facebook", "Trustpilot", "Angi", "BBB", "direct"}

e = html.escape


def validate(data):
    errs = []
    for i, r in enumerate(data["reviews"]):
        tag = r.get("id", f"#{i}")
        for k in ("id", "name", "rating", "date", "source", "text"):
            if not r.get(k):
                errs.append(f"{tag}: missing {k}")
        if r.get("source") not in SOURCES:
            errs.append(f"{tag}: unknown source {r.get('source')!r}")
        if r.get("source") == "direct" and not r.get("consent"):
            errs.append(f"{tag}: direct testimonial needs consent: true")
        elif r.get("source") != "direct" and not r.get("source_url"):
            errs.append(f"{tag}: missing source_url")
        if r.get("service") and r["service"] not in SERVICES:
            errs.append(f"{tag}: unknown service {r['service']!r}")
        if not SAMPLE and "[[" in json.dumps(r):
            errs.append(f"{tag}: contains [[ placeholder")
    if errs:
        sys.exit("reviews.json invalid:\n  " + "\n  ".join(errs))


def stars(n):
    n = round(n)
    return f'<span class="stars" aria-label="{n} out of 5 stars">' + "★" * n + '<span class="off">' + "★" * (5 - n) + "</span></span>"


def card(r):
    svc = SERVICES.get(r.get("service", ""), "")
    meta = " · ".join(x for x in (e(r.get("town", "")) + (", NJ" if r.get("town") else ""), svc) if x)
    src = r["source"]
    link = (f'<a href="{e(r["source_url"])}" rel="nofollow noopener" target="_blank">Read on {e(src)} ↗</a>'
            if src != "direct" else '<span>Shared directly with permission</span>')
    return f"""<article class="card" data-service="{e(r.get('service',''))}" data-town="{e(r.get('town',''))}">
  <header>{stars(r['rating'])}<time datetime="{e(r['date'])}">{e(r['date'])}</time></header>
  <blockquote>{e(r['text'])}</blockquote>
  <footer><div><strong>{e(r['name'])}</strong>{f'<span class="meta">{meta}</span>' if meta else ''}</div>{link}</footer>
</article>"""


def page(data):
    b = data["business"]
    five = sorted([r for r in data["reviews"] if r["rating"] == 5], key=lambda r: r["date"], reverse=True)
    totals = [t for t in data["platform_totals"] if t.get("url") and "[[" not in t["url"]]
    towns = sorted({r["town"] for r in five if r.get("town")})
    svcs = [s for s in SERVICES if any(r.get("service") == s for r in five)]
    noindex = SAMPLE or not five

    chips = "".join(
        f'<a class="plat" href="{e(t["url"])}" rel="noopener" target="_blank"><b>{e(t["platform"])}</b>'
        + (f'{t["rating"]:.1f} ★' if t.get("rating") else "")
        + (f' <small>({t["count"]} reviews)</small>' if t.get("count") else "") + "</a>"
        for t in totals)
    filters = '<button class="on" data-f="">All</button>' + "".join(
        f'<button data-f="{s}">{SERVICES[s]}</button>' for s in svcs)
    town_opts = '<option value="">All towns</option>' + "".join(f'<option>{e(t)}</option>' for t in towns)
    cards = "\n".join(card(r) for r in five) or '<p class="empty">Reviews are being added. Meanwhile, read them on the platforms above.</p>'
    town_list = "".join(f'<li><a href="#" data-town="{e(t)}">{e(t)}, NJ</a></li>' for t in towns)

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Good Guys Pools Reviews",
         "publisher": {"@id": b["website"] + "#business"}},
        {"@type": "HomeAndConstructionBusiness", "@id": b["website"] + "#business", "name": b["name"], "url": b["website"],
         "sameAs": [t["url"] for t in totals] + [SITE],
         "review": [{"@type": "Review", "author": {"@type": "Person", "name": r["name"]}, "datePublished": r["date"],
                     "reviewBody": r["text"], "reviewRating": {"@type": "Rating", "ratingValue": r["rating"], "bestRating": 5},
                     "publisher": {"@type": "Organization", "name": r["source"]}} for r in five[:50]]}]}

    banner = '<div class="sample">SAMPLE LAYOUT. Placeholder entries, not real reviews. Do not deploy.</div>' if SAMPLE else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Good Guys Pools Reviews | NJ Inground Pool Builder</title>
<meta name="description" content="{len(five)} five-star reviews of Good Guys Pools from New Jersey homeowners: inground pool construction, renovation and repair in Bergen, Passaic, Morris and Essex counties.">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{SITE}">'}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld)}</script>
<style>
:root{{--bg:#f6f4ef;--card:#fff;--ink:#14232b;--muted:#5b6b73;--line:#e3ded3;--accent:#0f6b73;--accent-ink:#fff;--star:#c98a0b;--off:#d8d2c4;--chip:#ece7dc}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#10171b;--card:#18232a;--ink:#e9eef0;--muted:#9aabb3;--line:#26343c;--accent:#4fb3ba;--accent-ink:#0b1a1d;--star:#e7b03a;--off:#3a4950;--chip:#1f2c33}}}}
:root[data-theme="dark"]{{--bg:#10171b;--card:#18232a;--ink:#e9eef0;--muted:#9aabb3;--line:#26343c;--accent:#4fb3ba;--accent-ink:#0b1a1d;--star:#e7b03a;--off:#3a4950;--chip:#1f2c33}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif}}
a{{color:var(--accent)}}.wrap{{max-width:1080px;margin:0 auto;padding:0 16px}}
.sample{{background:#b42318;color:#fff;text-align:center;padding:8px;font-weight:600}}
.disc{{font-size:13px;color:var(--muted);border-bottom:1px solid var(--line);padding:8px 0}}
.hero{{padding:48px 0 28px}}h1{{font:600 clamp(32px,6vw,52px)/1.05 Fraunces,Georgia,serif;margin:0 0 12px;letter-spacing:-.01em}}
.lede{{font-size:18px;color:var(--muted);max-width:640px;margin:0 0 22px}}
.plats{{display:flex;flex-wrap:wrap;gap:10px}}.plat{{display:flex;gap:8px;align-items:baseline;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 14px;text-decoration:none;color:var(--ink);font-size:14px}}
.plat small{{color:var(--muted)}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:24px 0 16px}}
.bar button,.bar select{{font:inherit;font-size:14px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 14px;cursor:pointer}}
.bar button.on{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
.grid{{columns:3 300px;column-gap:16px}}
.card{{break-inside:avoid;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:0 0 16px}}
.card header{{display:flex;justify-content:space-between;align-items:center}}.card time{{font-size:13px;color:var(--muted)}}
.stars{{color:var(--star);letter-spacing:2px;font-size:18px}}.stars .off{{color:var(--off)}}
blockquote{{margin:12px 0 14px;font-size:15.5px}}
.card footer{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:flex-end;font-size:14px}}
.meta{{display:block;color:var(--muted);font-size:13px}}.card footer a,.card footer span{{font-size:13px;color:var(--muted)}}
.empty{{color:var(--muted)}}
.towns{{margin:40px 0}}.towns h2,.cta h2{{font:600 26px/1.2 Fraunces,Georgia,serif;margin:0 0 12px}}
.towns ul{{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:8px}}.towns a{{display:block;background:var(--chip);border-radius:8px;padding:6px 10px;text-decoration:none;color:var(--ink);font-size:14px}}
.cta{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px;margin:40px 0;display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center}}
.cta p{{margin:0;color:var(--muted)}}.btn{{background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:600;padding:12px 20px;border-radius:10px}}
footer.site{{border-top:1px solid var(--line);padding:24px 0 40px;font-size:13px;color:var(--muted)}}
</style></head><body>
{banner}
<div class="wrap"><p class="disc">This site is operated by {e(b['name'])}. Reviews are reproduced word for word from public review platforms, each linked to its original.</p>
<section class="hero">
<h1>Good Guys Pools reviews</h1>
<p class="lede">{len(five)} five-star reviews from New Jersey homeowners on inground pool construction, renovation and repair across North Jersey. Overall ratings on each platform:</p>
<div class="plats">{chips}</div>
</section>
<div class="bar" role="toolbar" aria-label="Filter reviews">{filters}<select id="town" aria-label="Filter by town">{town_opts}</select></div>
<section class="grid" id="grid">{cards}</section>
{f'<section class="towns"><h2>Reviews by town</h2><ul>{town_list}</ul></section>' if towns else ''}
<section class="cta"><div><h2>Planning a pool in New Jersey?</h2><p>Free estimates for inground pool construction, renovation and repair. {e(b['license'])}</p></div>
<a class="btn" href="{e(b['estimate_url'])}">Get an estimate</a></section>
<footer class="site">© {e(b['name'])}, Hackensack, NJ · <a href="{e(b['website'])}">{e(b['website'])}</a> · {e(b['license'])}<br>
Each review is shown with its source and date. Platform totals above include all ratings, not only five-star reviews. This page shows five-star reviews only, so read every review on each platform for the full picture.</footer>
</div>
<script>
const cards=[...document.querySelectorAll('.card')],sel=document.getElementById('town');let svc='';
function apply(){{const t=sel.value;cards.forEach(c=>c.hidden=!((!svc||c.dataset.service===svc)&&(!t||c.dataset.town===t)))}}
document.querySelectorAll('.bar button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.bar button').forEach(x=>x.classList.remove('on'));b.classList.add('on');svc=b.dataset.f;apply()}});
sel.onchange=apply;
document.querySelectorAll('.towns a').forEach(a=>a.onclick=ev=>{{ev.preventDefault();sel.value=a.dataset.town;apply();document.getElementById('grid').scrollIntoView({{behavior:'smooth'}})}});
</script>
</body></html>"""


def main():
    data = json.loads(SRC.read_text())
    validate(data)
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(page(data))
    noindex = SAMPLE or not any(r["rating"] == 5 for r in data["reviews"])
    (DIST / "robots.txt").write_text("User-agent: *\n" + ("Disallow: /\n" if noindex else f"Allow: /\nSitemap: {SITE}sitemap.xml\n"))
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}</loc></url></urlset>')
    print(f"built dist/ from {SRC.name}: {sum(r['rating']==5 for r in data['reviews'])} five-star reviews{' (SAMPLE, noindex)' if SAMPLE else ''}")


if __name__ == "__main__":
    main()
