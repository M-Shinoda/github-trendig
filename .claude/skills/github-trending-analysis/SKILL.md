---
name: github-trending-analysis
description: Given one specific CSV file under .claude/skills/github-trending/data/final/ (produced by the github-trending skill), analyze each listed repository — why it trended during that collection period, and how it differs from similar tools/services — grounded in real research (repo page, README, web search), then report the findings to the user. Use this whenever the user asks to analyze, explain, or dig into why repositories on an already-collected GitHub Trending CSV became trendy, or how they compare to alternatives.
---

# GitHub Trending 分析スキル

[github-trending](../github-trending/SKILL.md) スキルが生成した `data/final/<since>/*_final.csv` を1つ指定して読み込み、そこに列挙されている各リポジトリについて、

1. **その収集期間(daily/weekly/monthly)になぜトレンド入りしたのか**
2. **類似のサービス・システムと何が違うのか**

を、実際にリポジトリのURLや関連情報(README、リリースノート、Web上の言及など)にアクセスして調査した根拠に基づき分析し、ユーザーに報告するスキルです。**推測や一般論での穴埋めは禁止**。裏付けが取れなかった場合はその旨を正直に書くこと。

## 入力

`.claude/skills/github-trending/data/final/<since>/trending_{since}_{language}_{YYYY-MM-DD}_{HHMMSS}_final.csv` の形式のファイルを1つ、ユーザーから指定してもらう(または「一番新しいdailyの結果を分析して」のような指示から該当ファイルを特定する)。

- 指定が曖昧な場合(例:「dailyの結果を分析して」で複数候補がある)は、`data/final/<since>/` 配下を `ls -t` 等で確認し、候補を提示してユーザーに確認する。
- 存在しないファイルや `data/final/` 以下にないファイルを指定された場合はエラーとして扱い、実行しない。

## パイプライン全体像

**中間生成物としてJSONファイルを作らないこと。** サブエージェントの出力・最終レポートいずれもMarkdownで統一する(JSONは Step 1 の stdout として一時的に使うだけで、ディスクには保存しない)。

```
1. parse_trending_csv.py   (決定的、stdoutにJSONを出すだけでファイル保存はしない)
      ↓ 出力: 期間メタデータ(since/language/収集時刻) + CSVの全行 (このターンの中で使うだけ)
2. Agentツールでサブエージェントに委譲   (生成AI + Web調査)
      ↓ 生成: Markdownフラグメントファイル(バッチごとに1つ)
        data/analysis/<since>/_fragments/<since>_<timestamp>_batchN.md
3. build_report.py    (決定的)
      ↓ 生成: data/analysis/<since>/*_analysis.md (Markdownレポート。これが唯一の永続的な成果物)
```

### Step 1: 対象CSVの読み込み(決定的)

```bash
python3 .claude/skills/github-trending-analysis/scripts/parse_trending_csv.py \
    --csv-path .claude/skills/github-trending/data/final/weekly/trending_weekly_all_2026-07-29_103249_final.csv
```

- ファイル名から `since`(daily/weekly/monthly)、対象言語、収集日時を抽出する。
- CSVの全行(リポジトリ名・主要言語・概要・GitHubURL・Star増分・ライセンスなど、github-trendingスキルが既に収集した情報)をJSONとして標準出力する。**これはStep 2のサブエージェント用プロンプトを組み立てるためだけに使う一時的な情報であり、ファイルとして保存しない。**
- Pythonの標準ライブラリ(`csv`, `json`, `re`)のみで動作するため、conda環境は不要(素の `python3` でよい)。

### Step 2: リポジトリごとの調査・分析(サブエージェントに切り出す)

**メインスレッドで直接分析を書かず、必ずAgentツール(`subagent_type: general-purpose`)でサブエージェントに委譲すること。** これは以下の理由による:

- 「なぜその時期にトレンド入りしたか」「類似サービスとの違い」は、リポジトリページ・README・Web検索結果を実際に調べて初めて根拠のある回答ができる、生成AIによる調査・考察が必要な作業だから。
- 1つの実行で扱うリポジトリ数が多い(daily: 10〜15件程度、weekly/monthly: 20件前後)ため、5〜8件程度ずつバッチに分けて並列にサブエージェントを起動する。

各サブエージェントへの指示に含めるべき内容:

1. 対象リポジトリのリスト(owner/repo, GitHubURL, 主要言語, Star増分, ライセンス, CSVに既にある概要)
2. 収集期間の情報(例:「このデータは2026-07-29 10:32:49時点で集計された、直近1週間(weekly)のGitHub Trendingです」)を伝え、**その期間内**の要因を意識して調査させる
3. 各リポジトリについて、**WebFetchでリポジトリページ・README・(あれば)CHANGELOG/Releasesページを確認し**、**WebSearchで当該期間前後のニュース・SNS言及・Hacker News/Reddit等の議論・関連ブログ記事を検索**した上で、次の2点を生成させる:
   - **なぜこの時期にトレンド入りしたか**: その収集期間中にトレンド入りした理由の分析(例: 大型リリース、著名人・メディアでの言及、特定の技術トレンドとの合致、OSSコミュニティでの話題化など)。裏付けとなる具体的事実(バージョン番号、日付、言及元など)を含めること。**明確な外的要因が見つからない場合は「特定の外的要因は確認できず、機能の完成度や既存コミュニティによる自然な拡大が主因と考えられる」のように正直に書く**。
   - **類似サービス・システムとの違い**: 類似のOSS・サービス・システムを最低1つ以上具体的に挙げ、アーキテクチャ・機能範囲・ライセンス・パフォーマンス・エコシステムなどの観点で何が違うのかを具体的に説明する。単なる「便利そう」「注目に値する」といった抽象的な表現ではなく、比較対象名を明示すること。
   - 末尾に**参考にした情報源**として、実際にアクセスして参照したURLを箇条書きで列挙する。

4. **出力はJSONではなく、以下のテンプレートに従ったMarkdownそのものにすること**(担当した全リポジトリ分を1つのMarkdownとして返す。見出しは `## owner/repo` の形式で、番号や余計な装飾を付けない):

   ```markdown
   ## owner/repo

   **なぜこの時期にトレンド入りしたか**

   (分析本文)

   **類似サービス・システムとの違い**

   (分析本文)

   **参考にした情報源**

   - https://github.com/owner/repo
   - https://...

   ---

   ## owner2/repo2
   ...
   ```

   サブエージェントの最終メッセージには、この形式のMarkdownだけを含めること(前置き・まとめ・JSON・コードフェンスでの囲みは不要)。

5. 各サブエージェントが返したMarkdownを、そのまま `data/analysis/<since>/_fragments/` 配下にバッチごとの `.md` ファイルとして保存する(例: `data/analysis/weekly/_fragments/weekly_2026-07-29_103249_batch1.md`)。**JSON化・要約変換はせず、返ってきたMarkdownをそのまま書き出すこと。**

### Step 3: レポートの組み立て(決定的)

```bash
python3 .claude/skills/github-trending-analysis/scripts/build_report.py \
    --csv-path .claude/skills/github-trending/data/final/weekly/trending_weekly_all_2026-07-29_103249_final.csv \
    --fragment data/analysis/weekly/_fragments/weekly_2026-07-29_103249_batch1.md \
    --fragment data/analysis/weekly/_fragments/weekly_2026-07-29_103249_batch2.md
# --output を省略すると自動的に .../data/analysis/weekly/trending_weekly_all_2026-07-29_103249_final_analysis.md に書き出される
```

- 対象CSVのファイル名から期間・言語などのヘッダー情報を自動導出し、渡されたMarkdownフラグメントをその後ろに連結して1つのレポートにする。
- CSVに含まれるリポジトリのうち、いずれのフラグメントにも `## owner/repo` セクションが無いものがあれば標準エラーに警告を出す(調査漏れの検出)。逆にCSVに存在しないリポジトリの見出しがあれば、それも警告する(誤ったリポジトリ名などのタイプミス検出)。
- `_fragments/` ディレクトリは中間生成物置き場なので、最終レポート完成後に残しておいても消してもよいが、`data/analysis/<since>/` 直下に置く最終成果物は常にこの `*_analysis.md` 1本にすること。

## ユーザーへの報告

- レポートファイルの保存先パスを伝える。
- さらに、レポート全体をそのまま貼り付けるのではなく、**チャット上でも主要なポイント(特に注目すべき数件のトレンド理由・差別化ポイント)を要約して直接伝えること**。ユーザーは「私に伝える」ことを明示的に求めているため、ファイルを作って終わりにしない。
- `build_report.py` が「CSVにあるがどのフラグメントにも見出しが無いリポジトリ」を警告した場合、そのリポジトリは分析なしでレポートから欠落しているということなので、不足分のサブエージェントを追加で走らせて埋めるか、少なくともユーザーに漏れがある旨を報告する。

## 実行時の注意

- 憶測で「なぜトレンド入りしたか」を断定しない。WebFetch/WebSearchで確認できた事実に基づいて記述し、確認できなかった場合はその旨を明記する。
- 類似サービスとの比較は、実在する具体的なプロダクト・OSS名を挙げて行う。比較対象が思いつかない場合は無理に挙げず、「直接の競合となる著名なOSSは確認できなかった」のように書く。
- CSVに既にある「概要」列は調査の出発点として使ってよいが、`trend_reason`・`differentiation` はそれを言い換えるだけでなく、新たな調査に基づいて掘り下げること。
- Web検索・ページ取得は各リポジトリにつき数回程度に留め、過度なリクエストを避ける。
