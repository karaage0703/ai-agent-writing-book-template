#!/usr/bin/env python3
"""Verify generated PDF and EPUB files without changing them."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(command: list[str]) -> str:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        fail(result.stderr.strip() or f"command failed: {' '.join(command)}")
    return result.stdout


def top_level_titles(chapters_dir: Path, pattern: str) -> list[str]:
    titles = []
    for path in sorted(chapters_dir.glob(pattern)):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = re.sub(r"\s+\{[^}]+\}\s*$", "", line[2:].strip())
                titles.append(title)
                break
    return titles


def without_whitespace(value: str) -> str:
    """Normalize PDF extractors inserting spaces around Latin text in Japanese."""
    return re.sub(r"\s+", "", value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify generated PDF and EPUB")
    parser.add_argument("--config", "-c", required=True)
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    base = config_path.parent
    output = config.get("output", {})
    output_dir = (base / output.get("output_dir", "./output")).resolve()
    filename = output.get("filename", "book")
    pdf_path = output_dir / f"{filename}.pdf"
    epub_path = output_dir / f"{filename}.epub"

    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        fail(f"PDF not found or empty: {pdf_path}")
    if not epub_path.is_file() or epub_path.stat().st_size == 0:
        fail(f"EPUB not found or empty: {epub_path}")
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        fail("pdfinfo and pdftotext are required")

    info = run(["pdfinfo", str(pdf_path)])
    size_match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", info)
    if not size_match:
        fail("could not read PDF page size")
    width, height = map(float, size_match.groups())
    if abs(width - 515.9) > 2 or abs(height - 728.5) > 2:
        fail(f"PDF is not JIS B5: {width} x {height} pts")

    with tempfile.TemporaryDirectory() as temporary:
        text_path = Path(temporary) / "book.txt"
        run(["pdftotext", str(pdf_path), str(text_path)])
        pdf_text = text_path.read_text(encoding="utf-8")

    source = config.get("source", {})
    chapters_dir = (base / source.get("input_dir", "./chapters")).resolve()
    titles = top_level_titles(chapters_dir, source.get("file_pattern", "*.md"))
    normalized_pdf_text = without_whitespace(pdf_text)
    missing_titles = [
        title for title in titles if without_whitespace(title) not in normalized_pdf_text
    ]
    if missing_titles:
        fail(f"chapter titles missing from PDF: {', '.join(missing_titles)}")

    with zipfile.ZipFile(epub_path) as archive:
        if archive.testzip() is not None:
            fail("EPUB archive contains a corrupt member")
        names = set(archive.namelist())
        if "mimetype" not in names or archive.read("mimetype") != b"application/epub+zip":
            fail("EPUB mimetype is missing or invalid")
        if not any(name.endswith("nav.xhtml") for name in names):
            fail("EPUB navigation document is missing")

    pages = re.search(r"Pages:\s+(\d+)", info)
    print(f"PDF: {pdf_path} ({pages.group(1) if pages else '?'} pages, JIS B5)")
    print(f"EPUB: {epub_path} (archive and navigation OK)")
    print(f"Chapter titles: {len(titles)} found in PDF")


if __name__ == "__main__":
    main()
