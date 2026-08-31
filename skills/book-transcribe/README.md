# book-transcribe

音声・動画を`transcriber_tool`で文字起こしし、原音、生の文字起こし、編集用Markdownを分けて保存するスキルです。

## 使い方

AIエージェントへ次のように頼みます。

```text
book-transcribeスキルを使ってaudio/interview.mp3を文字起こししてください。
```

自分で実行する場合の最小コマンドです。

```bash
mkdir -p materials/transcripts
uvx transcriber_tool transcribe "audio/interview.mp3" \
  --model-size base \
  --device auto \
  --language ja \
  --output "materials/transcripts/interview.raw.txt" \
  --verbose
```

詳細な実行フローは[SKILL.md](./SKILL.md)を参照してください。

## 必要なもの

- macOS、Linux、またはWSL2
- `uv`
- 対応する音声・動画ファイル: `mp3`、`mp4`、`wav`、`mov`、`avi`

2026年8月30日に`transcriber_tool 0.3.2`とリポジトリ付属のテスト音声を使い、CPU・tinyモデルで出力ファイルが生成されることを確認しています。

## よくある問題

- 日本語が別言語と判定される: `--language ja`を指定します
- 処理が重い: 最初に`--model-size tiny`または`base`で短い音声を試します
- `m4a`を入力できない: 元ファイルを残し、`ffmpeg`で対応形式へ変換します
- 出力がない: コマンドの終了コードとログを確認し、`test -s <出力ファイル>`で空でないことを確認します

## 開発元

`transcriber_tool`は、からあげが開発しているMIT Licenseのオープンソースソフトウェアです。

https://github.com/karaage0703/transcriber-tool
