#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

case "$(uname -s)" in
  Darwin)
    exec bash "$script_dir/setup-macos.sh"
    ;;
  Linux)
    exec bash "$script_dir/setup-ubuntu.sh"
    ;;
  *)
    echo "未対応のOSです: $(uname -s)" >&2
    echo "対応OS: macOS、Linux（Ubuntu）、WSL2（Ubuntu）" >&2
    exit 1
    ;;
esac
