#!/usr/bin/env python3
"""Generate PDF and EPUB books from Markdown with Pandoc and Typst."""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    book = config.get("book", {})
    if not book.get("title"):
        fail("book.title is required in config")
    if not book.get("author"):
        fail("book.author is required in config")
    return config


def resolve_path(value: str, base_dir: Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base_dir / path).resolve()


def collect_chapters(
    config: dict,
    config_dir: Path,
    content_dir: str | None = None,
) -> list[Path]:
    source = config.get("source", {})
    input_dir = (
        Path(content_dir).expanduser().resolve()
        if content_dir
        else resolve_path(source.get("input_dir", "./chapters"), config_dir)
    )
    pattern = source.get("file_pattern", "*.md")
    sort_by = source.get("sort_by", "filename")
    custom_order = source.get("custom_order", [])

    if not input_dir.is_dir():
        fail(f"input directory not found: {input_dir}")

    files = [Path(path) for path in glob.glob(str(input_dir / pattern))]
    if not files:
        fail(f"no files matching {pattern!r} in {input_dir}")

    if sort_by == "custom":
        by_name = {path.name: path for path in files}
        missing = [name for name in custom_order if name not in by_name]
        if missing:
            fail(f"custom_order contains missing files: {', '.join(missing)}")
        files = [by_name[name] for name in custom_order]
    elif sort_by == "date":
        files.sort(key=lambda path: path.stat().st_mtime)
    else:
        files.sort(key=lambda path: path.name)

    return files


def resolve_cover(config: dict, config_dir: Path) -> Path | None:
    value = config.get("book", {}).get("cover_image")
    if not value:
        return None
    path = resolve_path(value, config_dir)
    if not path.is_file():
        fail(f"cover image not found: {path}")
    return path


def generate_metadata(
    config: dict,
    destination: Path,
    cover: Path | None,
    config_dir: Path,
) -> Path:
    book = config["book"]
    author = book["author"]
    metadata = {
        "title": book["title"],
        "author": [author] if isinstance(author, str) else author,
        "lang": book.get("language", "ja"),
        "colophon": True,
    }
    for key in ("subtitle", "date", "version", "publisher", "description"):
        if book.get(key):
            metadata[key] = book[key]
    if cover:
        metadata["cover-image"] = os.path.relpath(cover, config_dir)

    path = destination / "metadata.yaml"
    with path.open("w", encoding="utf-8") as file:
        file.write("---\n")
        yaml.safe_dump(metadata, file, allow_unicode=True, sort_keys=False)
        file.write("---\n")
    return path


def require_command(command: str, install_hint: str) -> None:
    if not shutil.which(command):
        fail(f"{command} not found. {install_hint}")


def require_pandoc() -> None:
    require_command("pandoc", "Install Pandoc 3.9 or later.")
    result = subprocess.run(
        ["pandoc", "--version"], text=True, capture_output=True, check=True
    )
    match = re.search(r"pandoc\s+(\d+)\.(\d+)", result.stdout)
    if not match or tuple(map(int, match.groups())) < (3, 9):
        fail("Pandoc 3.9 or later is required")


def run(command: list[str], label: str) -> None:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        fail(f"{label} failed\n{details}")


def resource_path(config_dir: Path, chapters: list[Path]) -> str:
    roots = [config_dir, chapters[0].parent]
    unique = list(dict.fromkeys(str(path) for path in roots))
    return os.pathsep.join(unique)


def build_pdf(
    config: dict,
    config_dir: Path,
    chapters: list[Path],
    output_dir: Path,
    cover: Path | None,
) -> Path:
    require_pandoc()
    require_command("typst", "Install Typst 0.14 or later.")

    output = config.get("output", {})
    template = resolve_path(
        output.get("pdf_template", "./templates/pandoc-typst.typ"), config_dir
    )
    if not template.is_file():
        fail(f"PDF template not found: {template}")

    pdf_path = output_dir / f"{output.get('filename', 'book')}.pdf"
    with tempfile.TemporaryDirectory() as temporary:
        metadata = generate_metadata(config, Path(temporary), cover, config_dir)
        run(
            [
                "pandoc",
                "--from",
                "markdown+yaml_metadata_block+smart+pipe_tables+strikeout+task_lists+footnotes",
                "--pdf-engine=typst",
                f"--template={template}",
                "--toc",
                "--toc-depth=3",
                f"--resource-path={resource_path(config_dir, chapters)}",
                str(metadata),
                *[str(chapter) for chapter in chapters],
                "-o",
                str(pdf_path),
            ],
            "PDF build",
        )
    return pdf_path


def build_epub(
    config: dict,
    config_dir: Path,
    chapters: list[Path],
    output_dir: Path,
    cover: Path | None,
) -> Path:
    require_pandoc()

    output = config.get("output", {})
    css = resolve_path(output.get("epub_css", "./templates/epub.css"), config_dir)
    if not css.is_file():
        fail(f"EPUB stylesheet not found: {css}")

    epub_path = output_dir / f"{output.get('filename', 'book')}.epub"
    with tempfile.TemporaryDirectory() as temporary:
        metadata = generate_metadata(config, Path(temporary), cover, config_dir)
        command = [
            "pandoc",
            "--from",
            "markdown+yaml_metadata_block+smart+pipe_tables+strikeout+task_lists+footnotes",
            "--to",
            "epub3",
            "--toc",
            "--toc-depth=3",
            f"--resource-path={resource_path(config_dir, chapters)}",
            "--css",
            str(css),
            str(metadata),
            *[str(chapter) for chapter in chapters],
            "-o",
            str(epub_path),
        ]
        if cover:
            command[command.index("-o"):command.index("-o")] = [
                "--epub-cover-image",
                str(cover),
            ]
        run(command, "EPUB build")
    return epub_path


def requested_formats(config: dict, override: str | None) -> list[str]:
    if override == "both":
        return ["pdf", "epub"]
    if override:
        return [override]
    formats = config.get("output", {}).get("format", ["pdf"])
    invalid = [item for item in formats if item not in {"pdf", "epub"}]
    if invalid:
        fail(f"unsupported output formats: {', '.join(invalid)}")
    return formats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate PDF and EPUB books with Pandoc and Typst"
    )
    parser.add_argument("--config", "-c", required=True)
    parser.add_argument("--content-dir")
    parser.add_argument("--output", "-o")
    parser.add_argument("--format", "-f", choices=["pdf", "epub", "both"])
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    if not config_path.is_file():
        fail(f"config not found: {config_path}")
    config_dir = config_path.parent
    config = load_config(config_path)
    chapters = collect_chapters(config, config_dir, args.content_dir)
    cover = resolve_cover(config, config_dir)
    output_dir = (
        Path(args.output).expanduser().resolve()
        if args.output
        else resolve_path(config.get("output", {}).get("output_dir", "./output"), config_dir)
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(chapters)} chapters")
    print(f"Total characters: {sum(len(path.read_text(encoding='utf-8')) for path in chapters):,}")

    for output_format in requested_formats(config, args.format):
        if output_format == "pdf":
            result = build_pdf(config, config_dir, chapters, output_dir, cover)
        else:
            result = build_epub(config, config_dir, chapters, output_dir, cover)
        print(f"{output_format.upper()}: {result}")


if __name__ == "__main__":
    main()
