# book-cover

実際の書籍制作で使っている表紙スキルから、固有の作品設定を外したものです。背景画像は文字なしで用意し、書名と著者名を同梱のPillowスクリプトで合成します。

```bash
uv run --with pillow skills/book-cover/scripts/book_cover.py \
  --background assets/cover-background.png \
  --title "書籍タイトル" --author "著者名 著" \
  --output assets/cover.png --style default --preview
```

`--help`で全オプションを確認できます。日本語フォントが見つからない場合は、テンプレートの`make setup`を先に実行してください。
