"""Tests for the four AI-citation surface renderers."""
from __future__ import annotations

import json

import pytest

from aio_surfaces import (
    Fact,
    Service,
    SiteConfig,
    render_aeo_json,
    render_brand_json,
    render_entity_json,
    render_llms_txt,
)
from aio_surfaces.render import render_robots_txt_aibots


@pytest.fixture
def example_cfg() -> SiteConfig:
    return SiteConfig(
        site_name="Example Studio",
        site_url="https://example.com",
        tagline="We build things that get cited.",
        description=(
            "Example Studio is a hand-built example for the aio-surfaces "
            "test suite. We don't actually exist."
        ),
        services=[
            Service(
                name="Custom Websites",
                summary="Hand-coded HTML, React, Astro.",
                url="https://example.com/services/websites/",
                price="$2,500–$10,000",
            ),
        ],
        facts=[
            Fact(
                id="f-1",
                question="What does Example Studio do?",
                answer=(
                    "Example Studio builds production websites and AI-citation "
                    "infrastructure for small businesses."
                ),
            ),
        ],
        legal_name="EXAMPLE STUDIO LLC",
        ein="12-3456789",
        uei="ABC123DEF4G5",
        naics=["541511"],
        orcid="0000-0000-0000-0000",
        kg_mid="/g/exampleexample",
        same_as=[
            "https://github.com/example",
            "https://x.com/example",
        ],
        founder_name="Jane Example",
        founder_url="https://example.com/about/",
        veteran_branch="United States Army",
        veteran_subgroups=["Veteran"],
        address_street="123 Main St",
        address_locality="Springfield",
        address_region="MO",
        address_postal_code="65000",
    )


def test_llms_txt_contains_required_sections(example_cfg: SiteConfig):
    out = render_llms_txt(example_cfg)
    assert out.startswith("# Example Studio")
    assert "> We build things that get cited." in out
    assert "## Canonical Facts" in out
    assert "## Services" in out
    assert "## Machine-readable Endpoints" in out
    # Identifiers surface as cite-worthy facts
    assert "`12-3456789`" in out
    assert "ABC123DEF4G5" in out
    # llms.txt is markdown — must end with newline
    assert out.endswith("\n")


def test_llms_txt_omits_canonical_facts_block_when_empty():
    cfg = SiteConfig(
        site_name="Bare", site_url="https://bare.test",
        tagline="x", description="y",
    )
    out = render_llms_txt(cfg)
    assert "## Canonical Facts" not in out
    # Machine-readable endpoints always render
    assert "## Machine-readable Endpoints" in out


def test_aeo_json_is_valid_json_with_facts(example_cfg: SiteConfig):
    doc = json.loads(render_aeo_json(example_cfg))
    assert doc["siteName"] == "Example Studio"
    assert doc["siteUrl"] == "https://example.com"
    assert len(doc["facts"]) == 1
    assert doc["facts"][0]["id"] == "f-1"


def test_entity_json_has_organization_person_website(example_cfg: SiteConfig):
    doc = json.loads(render_entity_json(example_cfg))
    types = {n["@type"] for n in doc["@graph"]}
    assert types == {"Organization", "Person", "WebSite"}
    org = next(n for n in doc["@graph"] if n["@type"] == "Organization")
    # EIN surfaces twice: once on taxID, once on identifier[]
    assert org["taxID"] == "12-3456789"
    assert any(
        i["propertyID"] == "ein" and i["value"] == "12-3456789"
        for i in org["identifier"]
    )
    # UEI surfaces in identifier[]
    assert any(
        i["propertyID"] == "sam-gov-uei" and i["value"] == "ABC123DEF4G5"
        for i in org["identifier"]
    )


def test_entity_json_person_has_orcid_in_sameAs(example_cfg: SiteConfig):
    doc = json.loads(render_entity_json(example_cfg))
    person = next(n for n in doc["@graph"] if n["@type"] == "Person")
    assert person["identifier"]["value"] == "0000-0000-0000-0000"
    assert "https://orcid.org/0000-0000-0000-0000" in person["sameAs"]
    assert person["veteranOf"]["name"] == "United States Army"


def test_entity_json_omits_optional_blocks_when_absent():
    cfg = SiteConfig(
        site_name="Bare", site_url="https://bare.test",
        tagline="x", description="y",
    )
    doc = json.loads(render_entity_json(cfg))
    org = next(n for n in doc["@graph"] if n["@type"] == "Organization")
    assert "identifier" not in org
    assert "taxID" not in org
    assert "sameAs" not in org
    # Only Organization + WebSite when no founder declared
    types = [n["@type"] for n in doc["@graph"]]
    assert types == ["Organization", "WebSite"]


def test_brand_json_has_legal_entity(example_cfg: SiteConfig):
    doc = json.loads(render_brand_json(example_cfg))
    assert doc["legalEntity"]["legalName"] == "EXAMPLE STUDIO LLC"
    assert (
        doc["legalEntity"]["samLookupUrl"]
        == "https://sam.gov/entity/ABC123DEF4G5"
    )


def test_robots_block_contains_all_default_ai_bots(example_cfg: SiteConfig):
    out = render_robots_txt_aibots(example_cfg)
    for bot in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]:
        assert f"User-agent: {bot}" in out


def test_fact_rejects_oversize_answer():
    with pytest.raises(ValueError, match="Aim for"):
        Fact(id="x", question="?", answer="a" * 1001)


def test_siteconfig_roundtrip(example_cfg: SiteConfig):
    """to_dict -> from_dict should preserve everything."""
    data = example_cfg.to_dict()
    cfg2 = SiteConfig.from_dict(data)
    assert cfg2.site_name == example_cfg.site_name
    assert len(cfg2.services) == len(example_cfg.services)
    assert cfg2.services[0].name == example_cfg.services[0].name
    assert cfg2.facts[0].id == example_cfg.facts[0].id
    assert cfg2.same_as == example_cfg.same_as
