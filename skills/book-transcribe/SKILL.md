---
name: book-transcribe
description: transcriber_toolで音声や動画を文字起こしし、原音、生の文字起こし、編集稿を分けて保存する。「文字起こしして」「この録音を本の材料にして」で使う。
---

# 音声の文字起こし

`transcriber_tool`を既定の実行手段とし、結果を原稿とは別に保存する。

## 入力

- 音声または動画ファイル
- 言語、話者、収録日など分かっている情報
- 出力先。指定がなければ`materials/transcripts/`

## 手順

### Step 1 入力を確認する

対応形式は`mp3`、`mp4`、`wav`、`mov`、`avi`。元ファイルは変更しない。日本語音声では`--language ja`を使う。

### Step 2 文字起こしする

リポジトリのルートで実行する。

```bash
mkdir -p materials/transcripts
uvx transcriber_tool transcribe "audio/recording.mp3" \
  --model-size base \
  --device auto \
  --language ja \
  --output "materials/transcripts/recording.raw.txt" \
  --verbose
```

精度が足りない場合は`--model-size medium`または`large`で再実行する。GPU版を常用する場合は、`uv tool install "transcriber_tool[gpu]"`で導入し、同じコマンドの先頭を`transcriber_tool`へ変える。

### Step 3 成功を確認する

```bash
test -s materials/transcripts/recording.raw.txt
wc -c materials/transcripts/recording.raw.txt
```

コマンドの終了コードが0で、出力ファイルが存在し、空でないことを確認する。長時間音声をバックグラウンドで実行する場合は、利用中のAIエージェントの永続実行と完了通知の仕組みを使い、ログと終了コードも保存する。

### Step 4 原音と照合する

話者、固有名詞、数字、専門用語を優先して原音と照合する。聞き取れない箇所を推測で埋めず、`[要確認 00:12:34 固有名詞]`のように残す。

### Step 5 編集用Markdownを作る

生の文字起こしを上書きせず、`materials/transcripts/recording.edited.md`へ別保存する。冒頭に元音声、実行コマンド、モデル、言語、実行日を記録する。

## 出力

- 文字起こしMarkdown
- 誤認識の可能性がある箇所
- 著者または話者へ確認する項目

## Gotchas

- 日本語を自動判定に任せると誤検出することがあるため、`--language ja`を付ける
- 文字起こし結果を直接`chapters/`へ置くと原音との対応が失われるため、まず`materials/transcripts/`へ保存する
- `m4a`、`ogg`、`flac`はそのまま入力せず、元ファイルを残して`ffmpeg`で対応形式へ変換する

## 使用例

```text
book-transcribeスキルを使ってaudio/interview.mp3を文字起こししてください。
```

`transcriber_tool`は、からあげが開発しているMIT Licenseのツールです。
https://github.com/karaage0703/transcriber-tool
