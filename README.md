# AIエージェントと本をつくるためのテンプレート

Markdown原稿から、JIS B5判PDFとEPUB 3を生成する技術書テンプレートです。人間とAIエージェントが同じリポジトリで執筆・レビュー・組版できるように、制作ルール、サンプル原稿、生成スクリプト、検査、CIをまとめています。

このテンプレートを使った本づくりの実例は、技術同人誌「[AIエージェントと本をつくる技術](https://karaage0703.booth.pm/items/8787339)」で紹介しています。書籍の紹介記事は「[『AIエージェントと本をつくる技術』を書きました](https://karaage.hatenadiary.jp/entry/2026/09/01/004718)」を参照してください。

## AIエージェントへ頼む

CodexやClaude Codeなど、ローカルのファイルを読み書きし、コマンドを実行できるAIエージェントへ次のプロンプトを渡します。

```text
このリポジトリのREADME.mdとAGENTS.mdを先に読んでください。
現在のOSに合う方法で執筆環境をセットアップし、サンプルのPDFとEPUBを生成して検査してください。
途中で管理者権限や外部への公開が必要になった場合は、実行前に確認してください。
最後に、生成したファイルの場所、実行した検査、残っている問題を報告してください。
```

テンプレートには、AIエージェントが必要なときに参照できる汎用的な執筆用スキルも含まれています。

- `book-setup`: OSに合うセットアップとサンプル生成
- `book-ideas`: 経験、材料、対象読者から本のテーマ候補を整理
- `book-interview`: 著者へ一問ずつ質問し、具体的な経験を原稿材料として保存
- `book-materials`: 手元の資料を探し、出典と不足情報を整理
- `book-transcribe`: `transcriber_tool`の実コマンドで音声を文字起こしし、原音と照合
- `book-draft`: 材料と章の目的からMarkdown原稿を作成
- `book-review`: 原稿の根拠、重複、表記、伝わり方をレビュー
- `book-visualize`: 内容に合う図を選び、再編集可能な元データと画像を保存
- `book-build`: PDF・EPUBの生成と検査
- `book-cover`: 文字なし背景の生成、書名・著者名の合成、縮小確認
- `book-publish`: 販売セット、紹介文、サンプル、公開前チェックリストを準備
- `book-feedback`: 販売後の感想、告知、改訂候補を整理
- `book-revise`: 改訂候補から影響範囲を調べ、原稿修正、再組版、更新履歴まで実行

これらは完成品ではなく、最初の一冊を始めるためのひな型です。すべてを使う必要はありません。材料の置き場所、利用できる道具、公開形式、確認したい品質は人によって異なるため、実際の作業で得た例、失敗、確認項目、スクリプトを加えて育ててください。詳しくは[`skills/README.md`](skills/README.md)を参照してください。

## 自分でコマンドを実行する

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
├── CLAUDE.md -> AGENTS.md
├── README.md
├── book_config.yaml
├── chapters/
├── assets/
├── templates/
├── scripts/
├── skills/
│   ├── book-setup/
│   ├── book-ideas/
│   ├── book-interview/
│   ├── book-materials/
│   ├── book-transcribe/
│   ├── book-draft/
│   ├── book-build/
│   ├── book-review/
│   ├── book-visualize/
│   ├── book-cover/
│   ├── book-publish/
│   ├── book-feedback/
│   └── book-revise/
├── .agents/skills -> ../skills
├── .claude/skills -> ../skills
├── output/
└── .github/workflows/build-book.yml
```

- `chapters/`: Markdown原稿の正本
- `assets/`: 表紙、図、写真
- `templates/`: PDF用TypstテンプレートとEPUB用CSS
- `scripts/`: 生成と機械検査
- `skills/`: AIエージェントが再利用できるセットアップ、組版、レビュー手順
- `.agents/skills`: Codexが参照する`skills/`へのシンボリックリンク
- `.claude/skills`: Claude Codeが参照する`skills/`へのシンボリックリンク
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

## 出版と改訂をAIエージェントへ頼む

販売準備は次の一文から始められます。

```text
book-publishスキルを使って、この本の販売準備をしてください。
```

公開後に直したい点が集まったら、次のように頼みます。

```text
book-reviseスキルを使って、集めた改訂候補を確認し、この本を改訂してください。
```

AIエージェントは販売ファイルや原稿をリポジトリ内で準備し、実行した検査と未確認事項を報告します。価格決定、販売ページの公開、販売中ファイルの差し替えなど、外部の状態を変える操作は人間の確認後に行います。

## AIエージェントへ依頼する例

```text
AGENTS.mdとREADME.mdを先に読んでください。
第1章へ図を追加し、make bookでPDFとEPUBを再生成してください。
変更したファイル、実行した検査、未確認事項を報告してください。
push、Release作成、外部公開は行わないでください。
```

## ライセンス

テンプレートのコードと設定はMIT Licenseです。テンプレートから作る本の本文、画像、表紙には、制作者が別の利用条件を設定できます。
