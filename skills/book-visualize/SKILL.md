---
name: book-visualize
description: 章の内容から表、フロー、比較図、関係図など適切な形式を選び、再編集できる元データと書籍用画像を作る。「図を作って」「関係を可視化して」で使う。
---

# 図版の作成

## 入力

- 図で伝えたい関係または手順
- 掲載する章と前後の説明
- 書籍の判型、配色、画像形式

## 手順

1. 文章より図が分かりやすい内容か確認する
2. 時系列はフロー、対応関係は表、構造は関係図など、内容に合う形式を選ぶ
3. 一つの図へ情報を詰め込みすぎず、ラベルを短くする
4. 図の内容をJSONで`assets/diagrams/`へ保存する
5. 同梱スクリプトでPDFとEPUBへ掲載できるPNGを生成する
6. 縮小時の文字、線、コントラスト、代替テキストを確認する
7. 実際のPDFとEPUBで掲載箇所を見る

## 出力

- 再編集可能な元データ
- 掲載用画像
- Markdownの代替テキストとキャプション案

## 実行コマンド

```bash
uv run --with pillow skills/book-visualize/scripts/draw_diagram.py flowchart \
  --file assets/diagrams/example.json \
  --output assets/diagrams/example.png
```

入力形式と図の種類は次で確認する。

```bash
uv run --with pillow skills/book-visualize/scripts/draw_diagram.py --help
```

## 完了条件

- 元データと掲載用画像の両方が保存されている
- JSONから上のコマンドを再実行してPNGを作れる
- PDFとEPUBの掲載ページで文字と線を確認している

## 使用例

```text
book-visualizeスキルを使って、第4章の「離れた原稿の間を埋める流れ」を図にしてください。
```
