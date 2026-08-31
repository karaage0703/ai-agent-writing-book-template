#!/usr/bin/env python3
"""電子書籍の表紙生成スクリプト: 背景画像にタイトル・著者名等を合成

Usage:
    uv run book_cover.py --background bg.png --title "タイトル" --author "著者 著" --output cover.png
    uv run book_cover.py --background bg.png --title "タイトル" --style karaage --preview
    uv run book_cover.py --help
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow が必要です: uv add pillow")
    sys.exit(1)

# ========== スタイルプリセット ==========

STYLES = {
    "default": {
        "title_color": (255, 255, 255),
        "subtitle_color": (220, 220, 220),
        "author_color": (255, 255, 255),
        "label_color": (200, 200, 200),
        "badge_bg": (43, 87, 151),
        "badge_text": (255, 255, 255),
        "title_band_color": (0, 0, 0, 160),
        "author_band_color": (0, 0, 0, 140),
        "title_position": "top",  # top / center / bottom
    },
    "karaage": {
        "title_color": (255, 255, 255),
        "subtitle_color": (200, 200, 200),
        "author_color": (255, 255, 255),
        "label_color": (180, 180, 180),
        "badge_bg": (43, 87, 151),
        "badge_text": (255, 255, 255),
        "title_band_color": (0, 0, 0, 140),
        "author_band_color": (0, 0, 0, 160),
        "title_position": "top",
    },
    "minimal": {
        "title_color": (255, 255, 255),
        "subtitle_color": (200, 200, 200),
        "author_color": (255, 255, 255),
        "label_color": (180, 180, 180),
        "badge_bg": (80, 80, 80),
        "badge_text": (255, 255, 255),
        "title_band_color": (0, 0, 0, 100),
        "author_band_color": (0, 0, 0, 80),
        "title_position": "bottom",
    },
    "tech": {
        "title_color": (0, 255, 150),
        "subtitle_color": (100, 200, 150),
        "author_color": (200, 200, 200),
        "label_color": (150, 150, 150),
        "badge_bg": (0, 100, 60),
        "badge_text": (255, 255, 255),
        "title_band_color": (20, 20, 30, 200),
        "author_band_color": (20, 20, 30, 180),
        "title_position": "top",
    },
}

# フォントパス候補
FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
]

FONT_REGULAR_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]


def find_font(paths: list[str]) -> str | None:
    for p in paths:
        if Path(p).exists():
            return p
    return None


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    paths = FONT_PATHS if bold else FONT_REGULAR_PATHS
    font_path = find_font(paths)
    if font_path:
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def fit_text_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_size: int,
    min_size: int = 20,
    bold: bool = True,
) -> tuple[ImageFont.FreeTypeFont, int]:
    """テキストが収まるフォントサイズを計算"""
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            return font, size
    return load_font(min_size, bold), min_size


def draw_band(
    img: Image.Image,
    y: int,
    height: int,
    color: tuple,
) -> None:
    """半透明の帯を描画"""
    overlay = Image.new("RGBA", (img.width, height), color)
    img.paste(overlay, (0, y), overlay)


def generate_cover(
    background_path: str,
    title: str,
    subtitle: str = "",
    author: str = "",
    label: str = "",
    badges: list[str] | None = None,
    output_path: str = "cover.png",
    style_name: str = "default",
    width: int = 1632,
    height: int = 2624,
    preview: bool = False,
) -> str:
    style = STYLES.get(style_name, STYLES["default"])

    # 背景画像の読み込みとリサイズ
    bg = Image.open(background_path).convert("RGBA")

    # アスペクト比を維持してリサイズ（カバー方式: はみ出る部分をトリミング）
    bg_ratio = bg.width / bg.height
    target_ratio = width / height

    if bg_ratio > target_ratio:
        # 横長 → 高さに合わせて幅をトリミング
        new_height = height
        new_width = int(height * bg_ratio)
    else:
        # 縦長 → 幅に合わせて高さをトリミング
        new_width = width
        new_height = int(width / bg_ratio)

    bg = bg.resize((new_width, new_height), Image.LANCZOS)

    # 中央でトリミング
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    bg = bg.crop((left, top, left + width, top + height))

    img = bg.copy()
    draw = ImageDraw.Draw(img)

    margin = int(width * 0.06)
    text_area_width = width - margin * 2

    # ========== タイトルエリア ==========
    if style["title_position"] == "top":
        title_y_start = int(height * 0.02)
    elif style["title_position"] == "center":
        title_y_start = int(height * 0.35)
    else:
        title_y_start = int(height * 0.65)

    # タイトル帯の高さを計算
    title_font, _ = fit_text_size(draw, title, text_area_width, 120, 50)
    band_height = title_font.size + 60
    if subtitle:
        band_height += 70

    draw_band(img, title_y_start, band_height, style["title_band_color"])
    draw = ImageDraw.Draw(img)  # 再取得（paste後）

    # タイトル描画
    title_y = title_y_start + 20
    draw.text(
        (margin, title_y),
        title,
        font=title_font,
        fill=style["title_color"],
    )

    # サブタイトル
    if subtitle:
        sub_font = load_font(64, bold=False)
        sub_y = title_y + title_font.size + 20
        draw.text(
            (margin, sub_y),
            subtitle,
            font=sub_font,
            fill=style["subtitle_color"],
        )

    # ========== 下部エリア（著者名・レーベル・バッジ） ==========
    bottom_elements_height = 80
    if label:
        bottom_elements_height += 35
    if badges:
        bottom_elements_height += 50

    bottom_y_start = height - bottom_elements_height - 30
    draw_band(img, bottom_y_start, bottom_elements_height + 30, style["author_band_color"])
    draw = ImageDraw.Draw(img)

    current_y = bottom_y_start + 15

    # バッジ
    if badges:
        badge_font = load_font(20, bold=True)
        badge_label_font = load_font(18, bold=False)
        # 「対応ツール・プラットフォーム」ラベル
        draw.text(
            (margin, current_y),
            "対応ツール・プラットフォーム",
            font=badge_label_font,
            fill=style["label_color"],
        )
        current_y += 28

        badge_x = margin
        badge_padding = 8
        badge_gap = 10
        for badge_text in badges:
            bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
            bw = bbox[2] - bbox[0] + badge_padding * 2
            bh = bbox[3] - bbox[1] + badge_padding * 2

            # バッジ背景
            draw.rounded_rectangle(
                [badge_x, current_y, badge_x + bw, current_y + bh],
                radius=4,
                fill=style["badge_bg"],
            )
            draw.text(
                (badge_x + badge_padding, current_y + badge_padding - 2),
                badge_text,
                font=badge_font,
                fill=style["badge_text"],
            )
            badge_x += bw + badge_gap

        current_y += bh + 12

    # 著者名
    if author:
        author_font = load_font(64, bold=True)
        # 右寄せ
        bbox = draw.textbbox((0, 0), author, font=author_font)
        author_w = bbox[2] - bbox[0]
        draw.text(
            (width - margin - author_w, current_y),
            author,
            font=author_font,
            fill=style["author_color"],
        )
        current_y += 45

    # レーベル名
    if label:
        label_font = load_font(24, bold=False)
        bbox = draw.textbbox((0, 0), label, font=label_font)
        label_w = bbox[2] - bbox[0]
        draw.text(
            (width - margin - label_w, current_y),
            label,
            font=label_font,
            fill=style["label_color"],
        )

    # 保存
    output = Path(output_path)
    img = img.convert("RGB")
    img.save(str(output), quality=95)
    print(f"表紙を生成しました: {output} ({width}x{height}px)")

    # プレビュー
    if preview:
        preview_width = 800
        preview_height = int(height * preview_width / width)
        preview_img = img.resize((preview_width, preview_height), Image.LANCZOS)
        preview_path = output.with_name(f"{output.stem}_preview{output.suffix}")
        preview_img.save(str(preview_path), quality=85)
        print(f"プレビュー: {preview_path} ({preview_width}x{preview_height}px)")

    return str(output)


def main():
    parser = argparse.ArgumentParser(description="電子書籍の表紙を生成")
    parser.add_argument("--background", "-b", required=True, help="背景画像パス")
    parser.add_argument("--title", "-t", required=True, help="タイトル")
    parser.add_argument("--subtitle", "-s", default="", help="サブタイトル")
    parser.add_argument("--author", "-a", default="", help="著者名（例: からあげ 著）")
    parser.add_argument("--label", "-l", default="", help="レーベル名")
    parser.add_argument("--badges", default="", help="バッジテキスト（カンマ区切り）")
    parser.add_argument("--output", "-o", default="cover.png", help="出力パス")
    parser.add_argument("--style", default="default", choices=list(STYLES.keys()), help="スタイルプリセット")
    parser.add_argument("--width", type=int, default=1632, help="出力幅px")
    parser.add_argument("--height", type=int, default=2624, help="出力高さpx")
    parser.add_argument("--preview", action="store_true", help="プレビュー画像も生成")
    args = parser.parse_args()

    badges = [b.strip() for b in args.badges.split(",") if b.strip()] if args.badges else None

    generate_cover(
        background_path=args.background,
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        label=args.label,
        badges=badges,
        output_path=args.output,
        style_name=args.style,
        width=args.width,
        height=args.height,
        preview=args.preview,
    )


if __name__ == "__main__":
    main()
