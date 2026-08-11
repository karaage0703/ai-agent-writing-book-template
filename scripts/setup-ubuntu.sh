#!/usr/bin/env bash
set -euo pipefail

if [[ ! -r /etc/os-release ]]; then
  echo "Ubuntuを判定できませんでした" >&2
  exit 1
fi

# shellcheck disable=SC1091
source /etc/os-release
if [[ "${ID:-}" != "ubuntu" ]]; then
  echo "このスクリプトの対象はWSL2上のUbuntuです: ID=${ID:-unknown}" >&2
  exit 1
fi

case "$(uname -m)" in
  x86_64)
    deb_arch="amd64"
    typst_target="x86_64-unknown-linux-musl"
    uv_target="x86_64-unknown-linux-gnu"
    ;;
  aarch64|arm64)
    deb_arch="arm64"
    typst_target="aarch64-unknown-linux-musl"
    uv_target="aarch64-unknown-linux-gnu"
    ;;
  *)
    echo "未対応のCPUです: $(uname -m)" >&2
    exit 1
    ;;
esac

pandoc_version="3.10.1"
typst_version="0.14.2"
uv_version="0.12.3"
setup_tmp_dir="$(mktemp -d)"
trap 'rm -r -- "$setup_tmp_dir"' EXIT

sudo apt-get update
sudo apt-get install -y ca-certificates curl fonts-noto-cjk make poppler-utils xz-utils

pandoc_deb="pandoc-${pandoc_version}-1-${deb_arch}.deb"
curl -fL --retry 3 \
  "https://github.com/jgm/pandoc/releases/download/${pandoc_version}/${pandoc_deb}" \
  -o "$setup_tmp_dir/$pandoc_deb"
sudo apt-get install -y "$setup_tmp_dir/$pandoc_deb"

typst_archive="typst-${typst_target}.tar.xz"
curl -fL --retry 3 \
  "https://github.com/typst/typst/releases/download/v${typst_version}/${typst_archive}" \
  -o "$setup_tmp_dir/$typst_archive"
tar -xJf "$setup_tmp_dir/$typst_archive" -C "$setup_tmp_dir"
sudo install -m 0755 "$setup_tmp_dir/typst-${typst_target}/typst" /usr/local/bin/typst

uv_archive="uv-${uv_target}.tar.gz"
curl -fL --retry 3 \
  "https://github.com/astral-sh/uv/releases/download/${uv_version}/${uv_archive}" \
  -o "$setup_tmp_dir/$uv_archive"
curl -fL --retry 3 \
  "https://github.com/astral-sh/uv/releases/download/${uv_version}/${uv_archive}.sha256" \
  -o "$setup_tmp_dir/${uv_archive}.sha256"
(
  cd "$setup_tmp_dir"
  sha256sum -c "${uv_archive}.sha256"
)
tar -xzf "$setup_tmp_dir/$uv_archive" -C "$setup_tmp_dir"
sudo install -m 0755 "$setup_tmp_dir/uv-${uv_target}/uv" /usr/local/bin/uv

echo "WSL2 Ubuntuのセットアップが完了しました"
