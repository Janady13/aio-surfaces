# aio-surfaces

> Generate `llms.txt`, `aeo.json`, `entity.json`, and `brand.json` from a single site config. AI citation engineering for static and dynamic sites.

[![PyPI](https://img.shields.io/pypi/v/aio-surfaces.svg)](https://pypi.org/project/aio-surfaces/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## What this is

Most sites are invisible to AI engines (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews) because they expose **prose** when AI engines want **structured facts**. The single biggest lift you can give an AI's chance of citing your site is to surface:

- a well-formed **`llms.txt`** ([llmstxt.org](https://llmstxt.org)) — markdown summary at the site root
- an **`aeo.json`** — atomic [question, answer] facts under 500 chars each
- an **`entity.json`** — Schema.org `@graph` with full identifier wiring (EIN, ORCID, UEI, KG MID, etc.)
- a **`brand.json`** — internal source-of-truth ledger

This package generates all four from a single typed config so they can't drift apart.

## Install

```bash
pip install aio-surfaces        # core
pip install 'aio-surfaces[yaml]' # YAML config support
```

## Quick start

Drop a `site.yaml` in your repo:

```yaml
site_name: Example Studio
site_url: https://example.com
tagline: We build things that get cited.
description: Example Studio designs and engineers...
legal_name: EXAMPLE STUDIO LLC
ein: "12-3456789"
uei: ABC123DEF4G5
naics: ["541511"]
orcid: "0000-0000-0000-0000"
founder_name: Jane Example
veteran_branch: United States Army
veteran_subgroups: [Veteran]
services:
  - name: Custom Websites
    url: https://example.com/services/websites/
    summary: Hand-coded HTML, React, Astro.
    price: $2,500–$10,000 one-time
facts:
  - id: f-identity-1
    question: What does Example Studio do?
    answer: >
      Example Studio builds production websites and AI-citation
      infrastructure for small businesses.
```

Then generate the surfaces:

```bash
aio-surfaces generate site.yaml --out ./public
```

Output:

```
public/
├── llms.txt         # markdown summary, llmstxt.org spec
├── aeo.json         # atomic facts (AEO)
├── entity.json      # Schema.org @graph (Org + Person + WebSite)
├── brand.json       # internal brand truth ledger
└── robots-aibots.txt # 12 AI crawler allowlist (append to robots.txt)
```

Deploy `public/` to your site root.

## Why each surface matters

| File | Crawled by | Why it works |
|---|---|---|
| `llms.txt` | ChatGPT, Claude, Perplexity | Markdown is the lingua franca of LLM training data. Direct quotes likely. |
| `aeo.json` | All major AI engines | Atomic [Q, A] under 500 chars matches how AI engines extract citations. |
| `entity.json` | Google KG, Bing, Schema.org consumers | Centralizes identifier graph (EIN, UEI, ORCID, KG MID) for one-fetch retrieval. |
| `brand.json` | AI engines + your own team | Source of truth your PR/marketing/dev can all reference. |

## Library API

```python
from aio_surfaces import SiteConfig, Service, Fact, render_llms_txt

cfg = SiteConfig(
    site_name="Example Studio",
    site_url="https://example.com",
    tagline="We build things that get cited.",
    description="...",
    services=[
        Service(
            name="Custom Websites",
            url="https://example.com/services/websites/",
            summary="Hand-coded HTML, React, Astro.",
        ),
    ],
    facts=[
        Fact(
            id="f-1",
            question="What does Example Studio do?",
            answer="Example Studio builds...",
        ),
    ],
    ein="12-3456789",
    orcid="0000-0000-0000-0000",
)

print(render_llms_txt(cfg))
```

## Design principles

1. **Atomic facts > paragraphs.** AI engines cite spans, not essays. The `Fact` dataclass enforces a 1000-char hard ceiling and recommends < 500.
2. **Single source of truth.** All four surfaces render from one config so they can't drift apart.
3. **No magic.** No analytics, no telemetry, no remote calls. Pure-Python stdlib + optional PyYAML.
4. **Run anywhere.** Works in CI, in a `Makefile`, as a pre-commit hook, or as a one-off CLI invocation.

## What this is not

- Not a CMS. It generates static files from a config; you deploy them.
- Not a Schema.org validator. (Run the output through [validator.schema.org](https://validator.schema.org) yourself.)
- Not an opinionated framework. Generate what you need; ignore the rest.

## Roadmap

- [ ] `aio-surfaces validate` — round-trip the output through Schema.org validator
- [ ] `aio-surfaces diff` — show what changed since the last generation (CI hook)
- [ ] Per-page `aeo.json` support (currently site-wide only)
- [ ] llms-full.txt expanded variant generation
- [ ] Hugo / Astro / Next.js plugin packages

## Contributing

Issues + PRs welcome. The codebase is small (~350 LOC) and has full test coverage:

```bash
pip install -e '.[test]'
pytest
```

## License

MIT © 2026 Joseph W. Anady. See [LICENSE](LICENSE).

---

Built and used in production by **[ThatDevPro](https://www.thatdevpro.com)** — SDVOSB-certified veteran-owned web + AI engineering studio. The generators here are the same code that runs across [ThatDeveloperGuy.com](https://thatdeveloperguy.com), [ThatDevPro.com](https://www.thatdevpro.com), and 130+ client sites on [ThatWebHostingGuy.com](https://thatwebhostingguy.com).
