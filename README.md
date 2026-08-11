# AIエージェントと本をつくるためのテンプレート

Markdown原稿から、JIS B5判PDFとEPUB 3を生成する技術書テンプレートです。人間とAIエージェントが同じリポジトリで執筆・レビュー・組版できるように、制作ルール、サンプル原稿、生成スクリプト、検査、CIをまとめています。

## 最短の使い方

GitHubの「Use this template」から新しいリポジトリを作るか、GitHub CLIを使います。

```bash
gh repo create my-book \
  --private \
  --template karaage0703/ai-agent-writing-book-template \
  --clone
cd my-book
```

次に、環境をセットアップしてサンプル本を生成します。

```bash
make setup
make check
make book
```

生成物は`output/sample_book.pdf`と`output/sample_book.epub`です。

## 対応環境

- macOS（Intel / Apple Silicon、Homebrewを使用）
- Linux（Ubuntu、x86_64 / ARM64）
- Windows 11 + WSL2 + Ubuntu（x86_64 / ARM64）

Windows側のPowerShellやコマンドプロンプトから直接ビルドする構成ではありません。リポジトリをWSL2のLinuxファイルシステム内へcloneし、Ubuntuのシェルで操作します。`/mnt/c/...`でも動作する場合はありますが、ファイルI/Oと権限の差を避けるため`~/src/...`のようなWSL2内の場所を推奨します。

## 必要なもの

- Pandoc 3.9以上
- Typst 0.14以上
- uv
- GNU Make
- Noto Sans CJK JP
- Poppler（`pdfinfo`と`pdftotext`）

`make setup`がOSを判定し、必要なツールを導入します。macOSではHomebrew、LinuxとWSL2のUbuntuではAPTと公式GitHub Releaseを使います。Ubuntu側では`sudo`のパスワード入力が必要になる場合があります。

### macOS

```bash
git clone https://github.com/OWNER/MY-BOOK.git
cd MY-BOOK
make setup
make book
```

Homebrewが未導入なら、先に<https://brew.sh/ja/>から導入します。セットアップではPandoc、Typst、uv、Poppler、Fontconfig、Noto Sans CJK JPをインストールします。

### Linux（Ubuntu）

リポジトリをcloneし、Ubuntuのシェルで実行します。

```bash
git clone https://github.com/OWNER/MY-BOOK.git
cd MY-BOOK
make setup
make book
```

`make setup`の途中で、APTを実行するための`sudo`パスワードを求められる場合があります。

### Windows 11 + WSL2 Ubuntu

PowerShellでWSL2とUbuntuを用意します。再起動を求められた場合は従います。

```powershell
wsl --install -d Ubuntu
```

Ubuntuを起動し、Linux側で実行します。

```bash
mkdir -p ~/src
cd ~/src
git clone https://github.com/OWNER/MY-BOOK.git
cd MY-BOOK
make setup
make book
```

`make setup`はPandoc 3.10.1、Typst 0.14.2、uv 0.12.3と、日本語フォント・PDF検査ツールを導入します。

## 自分の本へ変える

1. `book_config.yaml`の書名、著者名、ファイル名を変更する
2. `chapters/`のサンプルを、自分の章へ置き換える
3. 画像を`assets/`へ置き、Markdownから相対パスで参照する
4. 必要なら`templates/pandoc-typst.typ`と`templates/epub.css`を調整する
5. `make book`を実行し、PDFとEPUBを確認する

表紙を使う場合は、設定へリポジトリルートからの相対パスを書きます。

```yaml
book:
  cover_image: "assets/cover.png"
```

## ディレクトリ構成

```text
.
├── AGENTS.md
├── README.md
├── book_config.yaml
├── chapters/
├── assets/
├── templates/
├── scripts/
├── output/
└── .github/workflows/build-book.yml
```

- `chapters/`: Markdown原稿の正本
- `assets/`: 表紙、図、写真
- `templates/`: PDF用TypstテンプレートとEPUB用CSS
- `scripts/`: 生成と機械検査
- `output/`: 生成物。Gitには入れず、CI ArtifactやReleaseで保管

## コマンド

```bash
make setup   # macOS / Linux / WSL2へ依存ツールを導入
make check   # ツールとフォントを確認
make pdf     # PDFを生成
make epub    # EPUBを生成
make verify  # 生成物を機械検査
make book    # PDFとEPUBを生成して検査
make clean   # output内の生成物を削除
```

Pull RequestではGitHub Actionsが`make book`を実行し、PDFとEPUBを確認用Artifactとして保存します。公開や販売ページへのアップロードは自動化していません。

## AIエージェントへ依頼する例

```text
AGENTS.mdとREADME.mdを先に読んでください。
第1章へ図を追加し、make bookでPDFとEPUBを再生成してください。
変更したファイル、実行した検査、未確認事項を報告してください。
push、Release作成、外部公開は行わないでください。
```

## ライセンス

テンプレートのコードと設定はMIT Licenseです。テンプレートから作る本の本文、画像、表紙には、制作者が別の利用条件を設定できます。
