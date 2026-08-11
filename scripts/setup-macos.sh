#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrewが必要です: https://brew.sh/ja/" >&2
  exit 1
fi

echo "macOS用の組版ツールをHomebrewでインストールします"
brew install pandoc typst uv poppler fontconfig
brew install --cask font-noto-sans-cjk
fc-cache -f

echo "macOSのセットアップが完了しました"
