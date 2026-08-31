---
name: book-setup
description: macOS、Linux、WSL2で書籍制作環境を用意し、サンプルPDFとEPUBを生成する。「セットアップして」「執筆環境を作って」で使う。
---

# 書籍制作環境のセットアップ

## 入力

- この書籍リポジトリ
- 現在のOSとCPUアーキテクチャ

## 手順

1. リポジトリ直下の`README.md`と`AGENTS.md`を読む
2. OSがmacOS、Linux、WSL2のどれかを確認する
3. `make setup`を実行する。管理者権限やパスワード入力が必要なら、実行前に人間へ伝える
4. `make check`で必要なツールと日本語フォントを確認する
5. `make book`でサンプルPDFとEPUBを生成し、検査する
6. 生成物の場所、検査結果、未解決の問題を報告する

## 完了条件

- `output/sample_book.pdf`と`output/sample_book.epub`が生成されている
- PDFの判型と章タイトル、EPUBのアーカイブと目次の検査が成功している

## 出力

- 生成したPDFとEPUBのパス
- 実行したコマンドと検査結果
- 未解決の問題

## 外部操作

push、Pull Request、Release、販売ページ、SNSへの投稿は行わない。必要な場合は人間へ確認する。

## 使用例

```text
book-setupスキルを使って、このOSへ執筆環境をセットアップしてください。
```
