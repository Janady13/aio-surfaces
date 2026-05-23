"""Typed site config. The single source of truth for every surface
this package generates. Load from YAML/JSON or build in code.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Service:
    """One service pillar — appears in llms.txt + aeo.json."""
    name: str
    summary: str
    url: str
    price: str | None = None


@dataclass
class Fact:
    """One declarative atomic fact (the unit of AI citation).

    Keep `answer` under 500 chars and use [subject][verb][object] sentence
    structure. AI engines cite spans, not paragraphs, so density of clean
    factual sentences correlates directly with citation rate.
    """
    id: str
    question: str
    answer: str

    def __post_init__(self) -> None:
        if len(self.answer) > 1000:
            raise ValueError(
                f"Fact {self.id!r}: answer is {len(self.answer)} chars. "
                "Aim for < 500 chars per atomic fact. AI citation rate drops "
                "sharply above 500."
            )


@dataclass
class SiteConfig:
    """Everything aio-surfaces needs to render the four surfaces.

    Required:
      site_name, site_url, tagline, description, services, facts

    Optional verification graph (strongly recommended for AI citation):
      legal_name, ein, uei, naics, orcid, kg_mid, gbp_cid, same_as,
      veteran, has_credential
    """
    # Core identity
    site_name: str
    site_url: str               # canonical, e.g. "https://example.com"
    tagline: str
    description: str            # ~200 chars

    # Content
    services: list[Service] = field(default_factory=list)
    facts: list[Fact] = field(default_factory=list)

    # Provenance / identity (Schema.org Organization)
    legal_name: str | None = None
    founding_date: str | None = None
    founder_name: str | None = None
    founder_url: str | None = None
    address_street: str | None = None
    address_locality: str | None = None
    address_region: str | None = None
    address_postal_code: str | None = None
    address_country: str = "US"
    telephone: str | None = None
    email: str | None = None

    # Verifiable identifiers
    ein: str | None = None              # IRS EIN (e.g. "12-3456789")
    uei: str | None = None              # SAM.gov UEI (12 char alnum)
    cage_code: str | None = None
    naics: list[str] = field(default_factory=list)
    orcid: str | None = None            # Person ORCID iD
    kg_mid: str | None = None           # Google Knowledge Graph MID
    gbp_cid: str | None = None          # Google Business Profile CID

    # Off-site verification (sameAs JSON-LD)
    same_as: list[str] = field(default_factory=list)

    # Person credentials
    veteran_branch: str | None = None
    veteran_subgroups: list[str] = field(default_factory=list)

    # AI crawler policy (allowlist)
    ai_bots: list[str] = field(default_factory=lambda: [
        "GPTBot",
        "OAI-SearchBot",
        "ChatGPT-User",
        "ClaudeBot",
        "Claude-User",
        "Claude-SearchBot",
        "PerplexityBot",
        "Perplexity-User",
        "Google-Extended",
        "Applebot-Extended",
        "Amazonbot",
        "Meta-ExternalAgent",
    ])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SiteConfig:
        # Reconstitute Service/Fact dataclasses
        services = [Service(**s) for s in data.pop("services", [])]
        facts = [Fact(**f) for f in data.pop("facts", [])]
        cfg = cls(**data)
        cfg.services = services
        cfg.facts = facts
        return cfg
