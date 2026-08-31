# book-visualize

実際の可視化スキルで使っているローカルPNG生成スクリプトから、書籍向けの関係図・フロー図部分を移植しています。外部APIは不要です。

```bash
uv run --with pillow skills/book-visualize/scripts/draw_diagram.py --help
```

図の内容はJSON、生成物はPNGとして分けて保存します。書籍用では背景色と装飾を増やしすぎず、PDF上の縮小表示を確認します。
