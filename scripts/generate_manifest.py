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
COVERS_DIR = REPO_ROOT / "covers"
MANIFEST_PATH = REPO_ROOT / "manifests" / "catalogs.json"
GITHUB_ORG = "Daniel-AA-Pinto"
GITHUB_REPO = "rubicer-catalogos"
GITHUB_BRANCH = "main"

ACCENT_MAP = {
    "LAMINAS": "Lâminas",
    "PORCELANICOS": "Porcelânicos",
    "PASTILHAS": "Pastilhas",
    "MOVEIS": "Móveis",
    "ESPELHOS": "Espelhos",
    "LAVATORIOS": "Lavatórios",
    "PEDRA": "Pedra Natural",
}


def title_from_id(catalog_id: str) -> str:
    cleaned = re.sub(r"^\d+\.", "", catalog_id)
    parts = [part for part in re.split(r"[-_.]+", cleaned) if part]
    if not parts:
        return catalog_id

    primary = parts[0].upper()
    if primary in ACCENT_MAP:
        return ACCENT_MAP[primary]

    return primary.capitalize()


def read_custom_title(catalog_id: str) -> str | None:
    title_path = COVERS_DIR / f"{catalog_id}.title"
    if title_path.exists():
        title = title_path.read_text(encoding="utf-8").strip()
        return title or None
    return None


def find_cover(catalog_id: str) -> Path | None:
    for extension in (".jpg", ".jpeg", ".png", ".webp"):
        cover_path = COVERS_DIR / f"{catalog_id}{extension}"
        if cover_path.exists():
            return cover_path
    return None


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
        entry = {
            "id": catalog_id,
            "title": read_custom_title(catalog_id) or title_from_id(catalog_id),
            "version": sha256_file(pdf_path),
            "url": (
                f"https://raw.githubusercontent.com/{GITHUB_ORG}/{GITHUB_REPO}/"
                f"{GITHUB_BRANCH}/catalogs/{pdf_path.name}"
            ),
            "sizeBytes": pdf_path.stat().st_size,
        }

        cover_path = find_cover(catalog_id)
        if cover_path is not None:
            entry["coverUrl"] = (
                f"https://raw.githubusercontent.com/{GITHUB_ORG}/{GITHUB_REPO}/"
                f"{GITHUB_BRANCH}/covers/{cover_path.name}"
            )

        catalogs.append(entry)

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
