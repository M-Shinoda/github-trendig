---
name: github-trending
description: Scrape GitHub Trending (https://github.com/trending), enrich each repository with an AI-generated overview/highlights/usage-ideas via a subagent, and export a final CSV (repository, language, overview, URL, star delta, highlights, usage ideas, license, first commit date) split by period (daily/weekly/monthly) and optionally filtered by language. Use this whenever the user asks to collect, scrape, track, summarize, or export GitHub Trending repositories/data.
---

# GitHub Trending Scraper

GitHub Trending ページ (`https://github.com/trending`) から情報を取得し、最終的に以下の9列を持つCSVを出力するスキルです。

**最終CSVの列**: リポジトリ名, 主要言語, 概要, GitHubURL, Star増分, 注目ポイント/要約, 活用アイデア/関連性/所感, ライセンス, first commit日

このうち **概要 / 注目ポイント/要約 / 活用アイデア/関連性/所感 の3列は生成AIによる要約・考察が必要**なため、決定的なスクリプトでは生成せず、**必ずAgentツールでサブエージェントに切り出して生成すること**。それ以外の列(リポジトリ名・主要言語・URL・Star増分・ライセンス・first commit日)はスクレイピング/GitHub APIで決定的に取得する。

## 重要: 呼び出すたびに必ず最初からやり直す

**このスキルが呼び出されたら、同じ日・同じ since/language の組み合わせで過去に実行済みであっても、必ずStep 1から3まで全て最初からやり直すこと。**

- 既存の `data/intermediate/<since>/*_raw.csv` や `enrichment_....json` があっても、それらを読み込んで再利用したり、リポジトリ一覧が重複しているからといってサブエージェント呼び出しを省略したりしない。
- 「今日すでに同じdailyを取得したから」「リポジトリが前回と同じだから」という理由でStep 1(スクレイピング)やStep 2(サブエージェントでのAI生成)をスキップしないこと。トレンド情報は日中でも変動するため、常に新しくスクレイピングし、概要等も都度新しく生成する。
- 過去の出力ファイルは削除せず残しておいてよいが、今回の実行は独立した新しい実行として、新しいタイムスタンプ付きファイルを一から生成すること。

## ディレクトリ構成

中間データ(raw CSV・enrichment JSON)と最終成果物(final CSV)は別ディレクトリに分け、さらに daily/weekly/monthly でも分ける。

```
data/
  intermediate/
    daily/    trending_daily_{lang}_{timestamp}_raw.csv, enrichment_daily_{lang}_{timestamp}.json
    weekly/   trending_weekly_{lang}_{timestamp}_raw.csv, enrichment_weekly_{lang}_{timestamp}.json
    monthly/  trending_monthly_{lang}_{timestamp}_raw.csv, enrichment_monthly_{lang}_{timestamp}.json
  final/
    daily/    trending_daily_{lang}_{timestamp}_final.csv
    weekly/   trending_weekly_{lang}_{timestamp}_final.csv
    monthly/  trending_monthly_{lang}_{timestamp}_final.csv
```

- `scrape_trending.py` は raw CSVを自動的に `<output-dir>/intermediate/<since>/` に書き出す(ディレクトリは自動作成される)。
- enrichment JSON(Step 2でサブエージェントが生成した内容をまとめたもの)も同じ `<output-dir>/intermediate/<since>/` に保存する。
- `merge_enriched.py` は `--output` を省略すると、`--base-csv` のパス(`.../intermediate/<since>/...`)から自動的に `.../final/<since>/...` を導出して書き出す。

## パイプライン全体像

```
1. scrape_trending.py   (決定的・conda環境で実行)
      ↓ 生成: data/intermediate/<since>/*_raw.csv
        (rank, repository, url, description, language, stars_total,
         forks_total, stars_period, since, language_filter, scraped_at,
         license, first_commit_date)
2. Agentツールでサブエージェントに委譲   (生成AI)
      ↓ 生成: data/intermediate/<since>/enrichment_....json
        { "owner/repo": {"overview": "...", "highlights": "...", "usage_ideas": "..."}, ... }
3. merge_enriched.py    (決定的・conda環境で実行)
      ↓ 生成: data/final/<since>/*_final.csv (9列、日本語ヘッダー)
```

### Step 1: スクレイピング(決定的、既存スクリプト)

専用conda環境 `github-trending` を使う(初回のみ作成。詳細は「セットアップ」参照)。

```bash
conda run -n github-trending python3 scripts/scrape_trending.py \
    --language python --since daily,weekly,monthly --output-dir ./data
```

- `article.Box-row` をパースして rank/repository/url/description/language/stars_total/forks_total/stars_period を取得。
- `license`: 各リポジトリのHTMLページ(`https://github.com/{owner}/{repo}`)の「About」欄をスクレイピングして取得する(`svg.octicon-law` アイコン横のテキスト)。トレンドページ自体と同じ普通のページ取得であり、**GitHub REST APIのレート制限は受けない**。ライセンス表記がない場合は空欄。
- `first_commit_date`: GitHub REST API (`/repos/{owner}/{repo}/commits`) でコミット履歴を最終ページまで辿って取得した最初のコミット日時。こちらは引き続きAPIのレート制限(未認証60回/時間)を受ける。**現状ユーザー方針によりデフォルトでは取得を省略している**(`--skip-first-commit` を付与、または必要になった時のみ外す)。
- 同一リポジトリがdaily/weekly/monthlyで重複しても、取得はユニークなリポジトリごとに1回だけ行う(無駄なリクエストを節約)。
- `first_commit_date`を取得する場合、GitHub APIは未認証だと60回/時間の制限がある。多数のリポジトリを扱う場合は環境変数 `GITHUB_TOKEN`(または `GH_TOKEN`)を設定しておくと5000回/時間まで上がるが、**ユーザーの意向によりトークンは使用しない**。レート制限に達した場合、`first_commit_date`のみ空欄のまま出力され、標準エラーに警告が出る(`license`は影響を受けない)。
- 出力先: `<output-dir>/intermediate/<since>/trending_{since}_{language}_{YYYY-MM-DD_HHMMSS}_raw.csv`(中間生成物であり、最終成果物ではない)

**推奨実行コマンド(現状のデフォルト運用)**:
```bash
conda run -n github-trending python3 scripts/scrape_trending.py \
    --since daily,weekly,monthly --output-dir ./data --skip-first-commit
```

### Step 2: AI付与列の生成(サブエージェントに切り出す)

raw CSVの各行について、次の3つのフィールドを生成する必要がある。

| フィールド | 内容の目安 |
|---|---|
| overview (概要) | リポジトリが何をするものか、2〜3文程度の説明 |
| highlights (注目ポイント/要約) | 技術的に注目すべき点・トレンド入りした理由などを箇条書き風に1〜3点 |
| usage_ideas (活用アイデア/関連性/所感) | どう使えそうか・既存プロジェクトとの関連・所感を2〜3文程度 |

**これはメインスレッドで直接書かず、Agentツール(`subagent_type: general-purpose` など)でサブエージェントに委譲すること。** 手順:

1. raw CSVを読み、リポジトリ一覧(repository, url, description, language)を得る。
2. リポジトリ数が多い場合は 5〜10件程度ずつバッチに分け、バッチごとに1つのAgentを(独立ならば並列に)起動する。それぞれのAgentプロンプトには対象リポジトリのリスト(repository名・url・description・language)を渡し、必要なら該当リポジトリのGitHubページ/READMEをWebFetchで参照して内容を把握した上で、上記3フィールドを日本語で生成し、**JSON形式**で返すよう指示する。

   出力JSONの形式(必須):
   ```json
   {
     "owner/repo": {
       "overview": "...",
       "highlights": "...",
       "usage_ideas": "..."
     }
   }
   ```

3. 各サブエージェントの返答(JSON)を集約し、raw CSVに含まれる全リポジトリ分をまとめた1つのJSONファイルとして、raw CSVと同じ `data/intermediate/<since>/` 配下に保存する(例: `data/intermediate/daily/enrichment_daily_python_2026-07-29_101230.json`)。

### Step 3: 最終CSVへのマージ(決定的)

```bash
conda run -n github-trending python3 scripts/merge_enriched.py \
    --base-csv ./data/intermediate/daily/trending_daily_python_2026-07-29_101230_raw.csv \
    --enrichment-json ./data/intermediate/daily/enrichment_daily_python_2026-07-29_101230.json
# --output を省略すると自動的に ./data/final/daily/trending_daily_python_2026-07-29_101230_final.csv に書き出される
```

- 9列の最終CSV(日本語ヘッダー)を `data/final/<since>/` 配下に出力する。
- enrichment JSONに存在しないリポジトリがあれば、該当3列は空欄のまま出力し、標準エラーに警告を出す(生成漏れがないか必ず確認すること)。

## セットアップ(conda環境)

```bash
conda env create -f environment.yml
# または: conda create -y -n github-trending python=3.11 beautifulsoup4
```

`conda info --envs` で `github-trending` が無ければ上記で作成する。

## 実行時の注意

- GitHub側のHTML構造が変わるとパースに失敗する可能性がある。取得件数が0件になった場合はページ構造の変更を疑い、`article.Box-row` セレクタ周辺を見直すこと。
- トレンドページへの短時間の大量リクエストは避ける(1回の実行で最大3リクエスト程度)。
- `GITHUB_TOKEN`/`GH_TOKEN`は**ユーザーの意向で使用しない**。`first_commit_date`はGitHub APIのレート制限(未認証60回/時間)を受けるため、現状は `--skip-first-commit` を付けて取得自体を省略する運用とする。`license`はHTMLスクレイピングなのでレート制限を受けず、通常通り取得する。
- Step 2(AI生成)を省略・簡略化しない。概要や所感を機械的なテンプレート文で済ませず、実際にリポジトリ内容を踏まえた生成をサブエージェントに行わせること。
- 実行後は最終CSVのパスと件数、enrichment漏れの有無を必ずユーザーに報告する。
