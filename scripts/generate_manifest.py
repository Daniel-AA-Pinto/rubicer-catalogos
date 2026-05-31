#!/usr/bin/env python3
"""Gera manifests/catalogs.json a partir dos PDFs em catalogs/."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOGS_DIR = REPO_ROOT / "catalogs"
MANIFEST_PATH = REPO_ROOT / "manifests" / "catalogs.json"
GITHUB_ORG = "Daniel-AA-Pinto"
GITHUB_REPO = "rubicer-catalogos"
GITHUB_BRANCH = "main"


def title_from_id(catalog_id: str) -> str:
    words = re.split(r"[-_]+", catalog_id)
    return " ".join(word.capitalize() for word in words if word)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest() -> dict:
    catalogs = []
    for pdf_path in sorted(CATALOGS_DIR.glob("*.pdf")):
        catalog_id = pdf_path.stem
        catalogs.append(
            {
                "id": catalog_id,
                "title": title_from_id(catalog_id),
                "version": sha256_file(pdf_path),
                "url": (
                    f"https://raw.githubusercontent.com/{GITHUB_ORG}/{GITHUB_REPO}/"
                    f"{GITHUB_BRANCH}/catalogs/{pdf_path.name}"
                ),
                "sizeBytes": pdf_path.stat().st_size,
            }
        )

    return {
        "updatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "catalogs": catalogs,
    }


def main() -> None:
    manifest = build_manifest()
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {MANIFEST_PATH} with {len(manifest['catalogs'])} catalog(s).")


if __name__ == "__main__":
    main()
