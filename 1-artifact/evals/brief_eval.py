"""Brief evals: deterministic checks a CAE-forwardable brief must pass.
Run: python 1-artifact/evals/brief_eval.py 1-artifact/briefs/<file>.md
Exit code 1 if any check fails."""
import re
import sys
from pathlib import Path

PRIMARY = ("federalreserve.gov", "occ.gov", "fdic.gov", "eur-lex.europa.eu", "fda.gov")
BANNED = ["transformative", "unlock", "game-changer", "game changer", "cutting-edge", "revolutionary",
          "seamless", "leverage", "synergy", "rapidly evolving landscape", "harness the power",
          "in today's", "worth noting", "reign", "itmethods"]
FALSE_CLAIMS = [  # things SR 26-2 does NOT say (see references/sr-26-2.md)
    (r"sr 26-2 (now )?(regulates|covers|applies to|governs) (generative|genai|agentic|ai agents|agents)",
     "claims SR 26-2 covers GenAI/agents (it excludes them)"),
    (r"\b(deadline|effective (date|on|from)|must comply by|fines?|penalt(y|ies))\b",
     "states a deadline, effective date or penalty not in the reference file"),
    (r"\bnon-?compliant\b", "calls the account non-compliant"),
    # v1 of this regex only caught "no framework exists" and missed "there is no supervisory
    # framework for them" in brief v1. Widened after a human read caught it.
    (r"\bno (supervisory |regulatory |control )?(framework|rules?|guidance|oversight)\b"
     r"(?! in sr 26-2)(?! under sr 26-2)",
     "overclaims that no framework exists (we only know SR 26-2 excludes agents)"),
]


def check(text: str) -> list[tuple[str, bool, str]]:
    body = text.split("## Sources")[0]
    low = text.lower()
    results = []
    words = len(re.findall(r"\b\w+\b", text))
    results.append(("under 400 words", words <= 400, f"{words} words"))

    section = re.search(r"## What it means for.*?\n(.*?)\n## ", text, re.S)
    bullets = re.findall(r"^\s*[-*] ", section.group(1), re.M) if section else []
    results.append(("exactly 3 'what it means' bullets", len(bullets) == 3, f"{len(bullets)} bullets"))

    sources = re.findall(r"https?://\S+", text.split("## Sources")[-1]) if "## Sources" in text else []
    non_primary = [s for s in sources if not any(p in s for p in PRIMARY)]
    results.append(("sources are primary URLs", bool(sources) and not non_primary,
                    f"{len(sources)} sources, non-primary: {non_primary or 'none'}"))

    changed = re.search(r"## What changed\n(.*?)\n## ", text, re.S)
    results.append(("'What changed' is footnoted", bool(changed and re.search(r"\[\^?\d+\]", changed.group(1))),
                    "needs [1]-style footnotes"))

    hits = [b for b in BANNED if b in body.lower()]
    results.append(("no banned words / no pitch", not hits, f"found: {hits or 'none'}"))
    results.append(("no exclamation marks", "!" not in body, ""))

    bad = [msg for pat, msg in FALSE_CLAIMS if re.search(pat, low)]
    results.append(("no false or overreaching claims", not bad, "; ".join(bad) or "none"))

    results.append(("fictional labels kept", "(fictional)" in text or "[INVENTED]" in text, ""))
    results.append(("marked not sent / internal", "not sent to the account" in low, ""))
    return results


if __name__ == "__main__":
    f = Path(sys.argv[1])
    res = check(f.read_text())
    for name, ok, note in res:
        print(f"{'PASS' if ok else 'FAIL'}  {name:38} {note}")
    failed = sum(not ok for _, ok, _ in res)
    print(f"\n{len(res) - failed}/{len(res)} passed  ({f.name})")
    sys.exit(1 if failed else 0)
