SHELL := /bin/bash

.PHONY: check book pdf epub verify clean

check:
	@command -v uv >/dev/null && uv --version || { echo "uv が見つかりません"; exit 1; }
	@command -v pandoc >/dev/null && pandoc --version | sed -n '1p' || { echo "pandoc が見つかりません"; exit 1; }
	@command -v typst >/dev/null && typst --version || { echo "typst が見つかりません"; exit 1; }
	@command -v pdfinfo >/dev/null || { echo "pdfinfo が見つかりません"; exit 1; }
	@command -v pdftotext >/dev/null || { echo "pdftotext が見つかりません"; exit 1; }
	@fc-match "Noto Sans CJK JP" | grep -q "NotoSansCJK" || { echo "Noto Sans CJK JP が見つかりません"; exit 1; }

book: pdf epub verify

pdf:
	uv run python scripts/generate_book.py --config book_config.yaml --format pdf

epub:
	uv run python scripts/generate_book.py --config book_config.yaml --format epub

verify:
	uv run python scripts/check_book.py --config book_config.yaml

clean:
	find output -maxdepth 1 -type f ! -name .gitkeep -delete
