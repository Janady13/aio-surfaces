"""CLI: aio-surfaces generate <config.yaml> --out ./public/"""
from __future__ import annotations

import argparse
import pathlib
import sys

from .config import SiteConfig
from .render import (
    render_aeo_json,
    render_brand_json,
    render_entity_json,
    render_llms_txt,
    render_robots_txt_aibots,
)


def _load_config(path: pathlib.Path) -> SiteConfig:
    text = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit(
                "PyYAML required for YAML configs. "
                "`pip install aio-surfaces[yaml]` or use JSON."
            )
        data = yaml.safe_load(text)
    else:
        import json
        data = json.loads(text)
    return SiteConfig.from_dict(data)


def cmd_generate(args: argparse.Namespace) -> int:
    cfg = _load_config(pathlib.Path(args.config))
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    (out / "llms.txt").write_text(render_llms_txt(cfg))
    (out / "aeo.json").write_text(render_aeo_json(cfg))
    (out / "entity.json").write_text(render_entity_json(cfg))
    (out / "brand.json").write_text(render_brand_json(cfg))
    (out / "robots-aibots.txt").write_text(render_robots_txt_aibots(cfg))

    print(f"wrote 5 surfaces to {out}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="aio-surfaces",
        description=(
            "Generate AI-citation surfaces (llms.txt, aeo.json, entity.json, "
            "brand.json) from a single site config."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Generate all surfaces")
    g.add_argument("config", help="Path to YAML or JSON site config")
    g.add_argument(
        "--out", default="./public",
        help="Output directory (default: ./public)",
    )
    g.set_defaults(func=cmd_generate)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
