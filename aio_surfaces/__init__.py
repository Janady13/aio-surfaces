"""aio-surfaces — generate llms.txt, aeo.json, entity.json, brand.json
from a single site config so AI engines (ChatGPT, Claude, Gemini,
Perplexity, Google AI Overviews) can correctly cite your site.

Spec references:
  llms.txt        https://llmstxt.org/
  Schema.org      https://schema.org/
  IETF .well-known https://www.rfc-editor.org/rfc/rfc8615
"""
from .config import SiteConfig, Service, Fact
from .render import (
    render_llms_txt,
    render_aeo_json,
    render_entity_json,
    render_brand_json,
)

__version__ = "0.1.0"
__all__ = [
    "SiteConfig",
    "Service",
    "Fact",
    "render_llms_txt",
    "render_aeo_json",
    "render_entity_json",
    "render_brand_json",
]
