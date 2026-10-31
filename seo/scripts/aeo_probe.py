#!/usr/bin/env python3
"""AI share-of-voice probe for Good Guys Pools.

Asks an AI assistant (with live web search) the questions real NJ homeowners ask,
then records whether Good Guys Pools is recommended, in what position, and which
competitors are named instead. Results append to seo/data/aeo_results.jsonl and a
summary prints to stdout.

Usage:
  ANTHROPIC_API_KEY=... python3 seo/scripts/aeo_probe.py [--limit N] [--model MODEL]
"""
import argparse
import datetime as dt
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOWNS = json.loads((ROOT / "data/service-area-towns.json").read_text())["towns"]
OUT = ROOT / "data/aeo_results.jsonl"
BRAND = re.compile(r"good\s*guys(\s*pools)?", re.I)

TEMPLATES = [
    "Who is the best inground pool builder near {town}, NJ?",
    "I want to build an inground pool in {town}, New Jersey. Which companies should I get quotes from?",
    "Recommend a company to repair my inground pool in {town}, NJ.",
    "Best pool renovation or resurfacing company in {county} County NJ?",
    "Top rated pool contractors in {county} County, New Jersey",
]
STATIC = [
    "best pool builder nj",
    "best pool builder in Bergen County NJ",
    "inground pool contractors near Hackensack NJ",
    "who builds gunite pools in North Jersey",
    "pool leak repair company Bergen County",
]


def build_prompts(limit):
    random.seed(dt.date.today().isocalendar()[1])  # stable within a week
    t1 = [t for t in TOWNS if t["tier"] == 1]
    t23 = [t for t in TOWNS if t["tier"] > 1]
    picks = random.sample(t1, min(5, len(t1))) + random.sample(t23, min(4, len(t23)))
    prompts = list(STATIC)
    for t in picks:
        prompts.append(random.choice(TEMPLATES).format(town=t["town"], county=t["county"]))
    return prompts[:limit]


def ask(client, model, prompt):
    msg = client.messages.create(
        model=model,
        max_tokens=1500,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
        messages=[{"role": "user", "content": prompt + "\nAnswer as a numbered list of company names with one line each."}],
    )
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def position(answer):
    for i, line in enumerate([l for l in answer.splitlines() if re.match(r"\s*\d+[.)]", l)], 1):
        if BRAND.search(line):
            return i
    return 0 if BRAND.search(answer) else None


def competitors(answer):
    names = []
    for line in answer.splitlines():
        m = re.match(r"\s*\d+[.)]\s*\**([^*\-–—:(]+)", line)
        if m and not BRAND.search(m.group(1)):
            names.append(m.group(1).strip())
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=14)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    args = ap.parse_args()
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    client = anthropic.Anthropic()
    run = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    rows = []
    for p in build_prompts(args.limit):
        try:
            ans = ask(client, args.model, p)
        except Exception as e:  # keep the run going; log the failure
            rows.append({"run": run, "engine": args.model, "prompt": p, "error": str(e)})
            continue
        rows.append({"run": run, "engine": args.model, "prompt": p, "mentioned": bool(BRAND.search(ans)),
                     "position": position(ans), "competitors": competitors(ans)[:8], "answer": ans})
    with OUT.open("a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    ok = [r for r in rows if "error" not in r]
    hit = [r for r in ok if r["mentioned"]]
    print(f"Share of voice: {len(hit)}/{len(ok)} prompts name Good Guys Pools ({100*len(hit)//max(len(ok),1)}%)")
    comp = {}
    for r in ok:
        for c in r["competitors"]:
            comp[c] = comp.get(c, 0) + 1
    print("Most-named competitors:", ", ".join(f"{k} ({v})" for k, v in sorted(comp.items(), key=lambda x: -x[1])[:10]))
    for r in ok:
        print(f"  [{'#'+str(r['position']) if r['position'] else ('named' if r['mentioned'] else '--')}] {r['prompt']}")


if __name__ == "__main__":
    main()
