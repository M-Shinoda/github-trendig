# GitHub Trending 分析レポート

- 対象期間: 1日間(daily) (収集: 2026-07-29 (時刻不明: ファイル名に時刻情報なし))
- 対象言語フィルタ: all
- リポジトリ数: 13
- 元データ: `/home/masami/projects/github-trendig/.claude/skills/github-trending/data/final/daily/trending_daily_all_2026-07-29_final.csv`

---

## pascalorg/editor

**なぜこの時期にトレンド入りしたか**

本リポジトリは2026年1月18日作成の比較的新しいプロジェクトで、React Three Fiber・WebGPUを用いたブラウザ完結の3D建築エディタ。2026年3月24日にはすでにGitHub Trendingで1位を記録しており、その後もexplainx.ai、PyShine、toolworthy.aiなど複数のブログが「AutoCADやSketchUpを置き換える無料オープンソース建築ツール」として継続的に紹介、さらにComfyUI連携プラグイン(jtydhr88/ComfyUI-PascalEditor)も登場するなど周辺エコシステムが拡大していた。7月29日時点のスター数は約2万、直近のpushも2026年7月29日と非常にアクティブ。ただし7月29日固有の単一の外的トリガー(特定のリリースやバイラル投稿)は確認できず、既存の人気に加えてブログ露出とプラグイン連携拡大による自然な継続的トレンド化が主因と考えられる。

**類似サービス・システムとの違い**

検索結果でも明示されている通り、本プロジェクトは商用の3D建築/BIMツールであるSketchUp(Trimble社、プロプライエタリ、Ruby拡張エコシステム、有料Proプラン)やAutodesk Revit(高額な企業向けBIMソフト)への「モダンな無料代替」と位置付けられている。Pascal EditorはMITライセンスでブラウザネイティブに動作し、Three.js/WebGPUによるリアルタイムレンダリング、TypeScript製プラグインアーキテクチャ(Turborepoモノレポ)を採用しており、デスクトップアプリのインストールや高額ライセンスが不要な点、Web配信・共同編集がしやすい点で差別化されている。

**参考にした情報源**

- https://github.com/pascalorg/editor
- https://trendshift.io/repositories/23831
- https://www.explainx.ai/blog/pascal-editor-open-source-3d-building-webgpu-july-2026
- https://github.com/jtydhr88/ComfyUI-PascalEditor

---

## jenkinsci/jenkins

**なぜこの時期にトレンド入りしたか**

2026年7月は通常のリリースサイクルの範囲内の動きが中心。7月8日予定でLTS版2.568.1がリリースされ(Windows 2019コントローライメージの廃止を含む)、7月21日にはJUnit/Mailer/Matrix Authorization StrategyなどのプラグインがWAR同梱から外され、jenkins.warのダウンロードサイズが20MB以上削減された。Platform SIGミーティング(7月14日・7月28日)ではJava 25移行の進捗(上位250プラグインの96%がJava 25でビルド・テスト対応)が報告されている。これらはいずれも定例のメンテナンス的アップデートであり、7月29日周辺の急上昇を説明する単一のバイラルな外的要因(著名人の言及やHacker News投稿など)は確認できなかった。20年以上の歴史を持つ成熟プロジェクトが定期リリースのたびに一時的にトレンド入りする自然な現象と考えられる。

**類似サービス・システムとの違い**

GitHub Actionsとの比較が最も明確。GitHub ActionsはGitHubに統合されたSaaS型CI/CDでYAMLベースの設定のみでサーバー管理不要、利用量課金である一方、Jenkinsは自前ホスト型のJavaモノリスで2,000以上のプラグインによる高い拡張性・カスタマイズ性を持つがJVM運用やプラグインのセキュリティパッチ管理などの保守負荷がある。ライセンスは両者ともMIT系だが、GitHub Actionsは自己ホストランナーはあるもののGitHubエコシステムへの依存が強く、Jenkinsは任意のインフラ・任意のSCMと組み合わせられる自由度の高さが差別化点。

**参考にした情報源**

- https://github.com/jenkinsci/jenkins
- https://community.jenkins.io/t/jenkins-jenkins-2-568-1-rc-released/37130
- https://community.jenkins.io/t/platform-sig-july-28-2026/37187
- https://community.jenkins.io/t/platform-sig-july-14-2026/37157

---

## moeru-ai/airi

**なぜこの時期にトレンド入りしたか**

AIRIはNeuro-sama(閉鎖的な商用AI VTuber)の「オープンソース版」を目指すプロジェクトとして2025年初頭から段階的に注目を集めてきた。2026年3〜6月にかけてexplainx.ai、BrightCoding、byteiotaなど複数メディアがWebGPUによるローカル音声チャットやMinecraft/Factorioの自律プレイ機能を紹介しており、スター数は約4.6万、pushは2026年8月2日時点でも継続中と非常にアクティブ。ただし7月29日周辺に限定した新リリースや著名人の言及など明確な単発トリガーは検索で確認できず、VTuber/AIコンパニオン愛好者コミュニティによる継続的な機能追加と口コミ的拡散が主因と考えられる(特定の外的要因は確認できず、既存コミュニティによる自然な拡大が主因と考えられる)。

**類似サービス・システムとの違い**

同じくNeuro-sama系オープンソースAIコンパニオンであるOpen-LLM-VTuber(Open-LLM-VTuber/Open-LLM-VTuber)と比較すると、Open-LLM-VTuberはPythonバックエンド+Live2Dフロントエンドで音声対話とオフライン動作に特化したシンプルな構成であるのに対し、AIRIはTypeScript/Vue/Electronスタックで、VRMとLive2Dの両対応、Minecraft/Factorio/Kerbal Space Programでの自律プレイ、Discord/Telegram連携、DuckDB WASMによる記憶システムなど、単なる音声対話コンパニオンを超えた「ゲームも遊べるデジタルペット」という広いスコープを持つ点で差別化されている。両者ともMITライセンス。

**参考にした情報源**

- https://github.com/moeru-ai/airi
- https://explainx.ai/blog/airi-ai-vtuber-neuro-sama-guide-2026
- https://github.com/Open-LLM-VTuber/Open-LLM-VTuber
- https://airi.moeru.ai/docs/en/docs/overview/versions

---

## andrewyng/aisuite

**なぜこの時期にトレンド入りしたか**

検索により「AISuiteは2026年7月27日にGitHub Trendingで12位にランクイン」という具体的な記述が見つかった。これは今回のデータ収集日(7月29日)の直前であり、時期的に整合する。背景には、OAuth対応のリモートMCPサーバーサポート追加、プロバイダ横断の非同期(async)対応、新規プロバイダ統合など活発なPRマージが続いていたこと、また作成者がDeepLearning.AIの著名人Andrew Ngであることによる知名度も押し上げ要因と考えられる。

**類似サービス・システムとの違い**

同種の「複数LLMプロバイダを統一APIで扱うSDK」であるLiteLLM(BerriAI/litellm)と比較すると、LiteLLMは100以上のプロバイダに対応し、コスト追跡・ガードレール・ロードバランシングを備えたプロキシ/ゲートウェイサーバーモードを持つなど機能・実績ともに大規模かつ成熟している(スター数もaisuiteの数倍規模)。一方aisuiteは対応プロバイダ数こそ約10と少ないが、Chat Completions APIに加えてツール呼び出し・承認ワークフロー・allow/denyリストによるツールポリシーを備えた「Agents API」層とネイティブMCPサポートを軽量な形で提供する点が特徴で、シンプルさとAndrew Ngブランドによる信頼性を武器にしている。両者ともMITライセンス。

**参考にした情報源**

- https://github.com/andrewyng/aisuite
- https://orangebot.ai/github-trending-today
- https://saqibcs.medium.com/recently-andrew-ng-released-aisuite-but-how-does-it-stack-up-against-litellm-e1efbda1d122
- https://github.com/BerriAI/litellm

---

## affaan-m/ECC

**なぜこの時期にトレンド入りしたか**

GitHub APIで実際に確認したところ、本リポジトリは2026年1月18日作成でありながら7月29日時点でスター236,904、フォーク36,016という極めて急激な成長を遂げている。経緯としては、作成者Affaan MustafaがAnthropic×Forum Venturesハッカソンで優勝した後、Claude Codeの設定術をまとめたXスレッド「The Shorthand Guide to Everything Claude Code」が数日で90万ビュー・1万以上のブックマークを獲得してバズり、その設定一式をオープンソース化したのが本リポジトリ(ECC = Everything Claude Code)。直近ではv2.0.0「Agent Harness Operating System」リリース(Plan Canvas、Kimiハーネス対応、セルフホストGPU連携などを追加)が出ており、これが7月末のトレンド入りを後押しした可能性が高い。なお、作成から半年程度で23万超のスターという伸び方は通常のバイラル成長としては極めて急峻であり、Medium記事のタイトルが「開発者コミュニティを二分する8.2万スターのエージェントハーネス」と評するなど賛否両論も存在する点は付言しておく(不正なスター増加を断定する一次情報は確認できなかった)。

**類似サービス・システムとの違い**

同種のClaude Code向けマルチエージェント設定フレームワークであるwshobson/agents(112エージェント・72プラグインを必要な分だけ組み込む「コンポーザブル」設計、Claude Code/Codex/Cursor/OpenCode/Gemini/Copilotの6ハーネス対応)やSuperClaude_Framework(pipインストール可能な軽量Markdown設定、約30コマンド・20エージェント、セキュリティスキャナやメモリ層なし)と比較すると、ECCはAgentShieldによるセキュリティスキャン、永続的なクロスセッション記憶システム、自動化フック、月19ドルのProプラン付きGitHub Appという「重量級のエージェントOS」路線を取っている点で異なる。単独開発者が週次で7つのハーネスに機能追加を行う開発体制も特徴的。

**参考にした情報源**

- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/ECC/releases/tag/v2.0.0
- https://medium.com/@tentenco/everything-claude-code-inside-the-82k-star-agent-harness-thats-dividing-the-developer-community-4fe54feccbc1
- https://github.com/wshobson/agents
- https://github.com/SuperClaude-Org/SuperClaude_Framework

---

## hello245m/free-stockdb

**なぜこの時期にトレンド入りしたか**

リポジトリは2026年5月8日作成と新しく、7月29日時点でスターは約1,700。リポジトリ自身の告知によれば「7月27日にバグ修正版を公開、数ヶ月のユーザーテストを経てMac/Linux版も近日対応予定」とのアナウンスがあり、これがトレンド集計日(7月29日)の直前というタイミングと重なる。ただし英語圏のプレスやHacker News/Redditでの言及は検索では確認できず、主に中国語圏のA株クオンツ開発者コミュニティ内での口コミ的拡散が中心とみられる。特定の大規模な外的バイラル要因は確認できず、リポジトリ自身のアップデート告知とニッチだが実需のあるコミュニティ内拡散が主因と考えられる。

**類似サービス・システムとの違い**

中国語圏で広く使われる無料オープンソースの金融データライブラリAKShare(akfamily/akshare)と比較すると、AKShareはA株/香港株/米株/先物/マクロ経済まで幅広い市場をカバーする「都度リモート取得型」のデータインターフェースライブラリとして既に大規模なコミュニティを持つ。一方free-stockdbはA株の日足・分足・ETF分足に特化し、Zstd圧縮によるローカルDB(5〜20GB)への増分同期・ローカルキャッシュを核とした「ローカルファースト」設計で、データ取得層と戦略検証層を完全に分離し、バックテストや39種類のテクニカル指標計算、Python SDK/HTTP API/Excel・WPSマクロ/MCPなど複数のアクセス手段を提供する点が特徴。全市場網羅性ではAKShareに劣るが、大規模バックテスト時のクエリ性能とオフライン耐性を重視した設計思想で差別化している。

**参考にした情報源**

- https://github.com/hello245m/free-stockdb
- https://github.com/akfamily/akshare

---

## huggingface/speech-to-speech

**なぜこの時期にトレンド入りしたか**

具体的な外的要因として、Hugging Face・Pollen Robotics・Seeed Studioが共同開発したオープンソースロボット「Reachy Mini」(累計3,000台出荷)との連動が挙げられる。2026年6月28日付のHackaday記事「Reachy Mini Desktop Robot Gets All-local, Conversational AI」やHugging Face公式ブログ「Reachy Mini goes fully local」で、本speech-to-speechリポジトリがReachy Miniの本番会話バックエンド(VAD→STT→LLM→TTSのカスケード、OpenAI Realtime API互換WebSocket)として明示的に紹介されており、ロボット関連の話題が続く中で7月末にかけても注目が持続したと考えられる。

**類似サービス・システムとの違い**

音声AIエージェント構築フレームワークとして著名なPipecat(pipecat-ai/pipecat、Daily.co製、BSD-2ライセンス)と比較すると、Pipecatは100以上のAIサービス・WebRTC/WebSocketなど複数トランスポートに対応し、JS/React/iOS/Android/C++向けクライアントSDKを備えたクラウド・プロバイダ非依存の汎用オーケストレーション基盤である。一方Hugging Faceのspeech-to-speechはApache 2.0ライセンスで、Parakeet/Whisper/Kokoro/Qwen3-TTSなどHugging Faceエコシステムのモデルに密結合した「リファレンス実装」的な位置付けが強く、llama.cppやmlx-lmを用いた完全オンデバイス推論に最適化されている点、そして実際にReachy Miniという物理ロボット製品に組み込まれて量産稼働している点がPipecatとの明確な違いとなっている。

**参考にした情報源**

- https://github.com/huggingface/speech-to-speech
- https://huggingface.co/blog/local-reachy-mini-conversation
- https://hackaday.com/2026/06/28/reachy-mini-desktop-robot-gets-all-local-conversational-ai/
- https://github.com/pipecat-ai/pipecat

## virgiliojr94/book-to-skill

**なぜこの時期にトレンド入りしたか**

特定の単一ニュースやHacker News/Redditでのバイラル投稿は確認できなかった。Trendshiftの記録では7月26日にPython言語別トレンド入りし、7月28日には全言語デイリートレンドで3位まで上昇、7月中に約28,000スターを獲得しており、2026年に急拡大した『Claude Agent Skills』(Claude Code/GitHub Copilot CLI/Ampが共通で読める SKILL.md 標準)エコシステム全体の盛り上がりに乗った、コミュニティ内の口コミによる自然な拡散が主因と考えられる。『PDF全文をコンテキストに詰め込むより24〜51倍トークン効率が良い』という具体的な性能訴求も拡散を後押しした可能性がある。

**類似サービス・システムとの違い**

Google NotebookLMとの違いが明確。NotebookLMはクラウドホスト型でGeminiの大コンテキストにソースを読み込みRAGで応答するクローズドソースのWebサービスで、利用にはGoogleアカウントとネット接続が必要。一方book-to-skillはMITライセンスのローカルCLI/エージェントスキルで、書籍を事前に『SKILL.md+章ごとのMarkdownファイル+用語集+チートシート』という階層構造にコンパイルし、Claude Code等のコーディングエージェントセッション内でオンデマンド読み込みする設計。サーバーやベクトルDBを必要とせず、コーディングエージェントのトークン消費削減に特化している点が、汎用の対話型リサーチノートであるNotebookLMと根本的に異なる。

**参考にした情報源**

- https://github.com/virgiliojr94/book-to-skill
- https://trendshift.io/repositories/27038
- https://www.msfconsole.cn/Bot-GithubTrending-2026-07-29/

---

## opengeos/GeoLibre

**なぜこの時期にトレンド入りしたか**

明確な外的要因あり。トレンド当日の2026年7月29日にデスクトップ版v2.4.0(Windows/macOS)と複数アーキテクチャ向けAndroid APKが新規リリースされており、その直前の7月14日にはv2.0.0リリースがGIS専門ブログSpatialistsで取り上げられている。さらに開発者Qiusheng Wu氏(leafmap/geemapの作者として知られるテネシー大学教授)が2026年5月の初公開時からX(旧Twitter)で各リリースを継続的に告知しており、これが継続的なトラフィック流入源になっていると考えられる。

**類似サービス・システムとの違い**

デファクトスタンダードのオープンソースデスクトップGISであるQGISとの違いが顕著。QGISはC++/Qt製でPythonプラグインに対応した強力な解析機能を持つが、デスクトップ専用でWeb/モバイル/Jupyter対応がなく学習コストも高い。対してGeoLibreはTauri v2・React・TypeScript・MapLibre GL JS・DuckDB-WASM Spatial・deck.glという単一コードベースで、Webブラウザ・デスクトップ・モバイル・Jupyterノートブックの全環境を横断し、サーバー不要のブラウザ内空間SQL処理でデータをローカルに保持できる。Uberのkepler.glと比べても、デスクトップ/モバイルへのネイティブ配布まで持つ点が差別化要因。

**参考にした情報源**

- https://github.com/opengeos/GeoLibre
- https://github.com/opengeos/GeoLibre/releases
- https://spatialists.ch/posts/2026/07/14-geolibre-200-released/
- https://x.com/giswqs/status/2060457987035042297
- https://gishub.org/blog/geolibre/

---

## paperswithbacktest/awesome-systematic-trading

**なぜこの時期にトレンド入りしたか**

7月29日に特定できる単一の外的トリガーは確認できず、機能の完成度や既存コミュニティによる自然な拡大が主因と考えられる。この種の『awesomeリスト』は日々のトレンドに周期的に再浮上しやすく、スター数もソースによって記録時期が異なり(7月27日時点で4.5kと報告する情報源もあれば、別の情報源は12.4kと報告するなど不整合がある)、単発のバイラルというより2026年5月・6月のブログ紹介記事(blog.brightcoding.dev等)を通じたじわじわとした認知拡大の蓄積結果とみられる。

**類似サービス・システムとの違い**

同名の先行リストであるwangzhe3224/awesome-systematic-tradingとの違いが明確。wangzhe3224版は純粋なコミュニティ主導のリンク集であるのに対し、paperswithbacktest版は実在するアルゴトレーディング教育企業Papers With Backtest(2023年設立、ニューヨーク拠点)が運営し、単なるリンク集にとどまらず static/strategies フォルダに40以上の戦略の実行可能なPythonサンプルコードを独自収録している点が特徴。同社の商用プラットフォーム(査読済み戦略5,000件超のデータベースとバックテスト基盤)への導線を兼ねたコンテンツマーケティング的な性格が強く、純粋な非営利コミュニティリストとは運営動機が異なる。

**参考にした情報源**

- https://github.com/paperswithbacktest/awesome-systematic-trading
- https://github.com/wangzhe3224/awesome-systematic-trading
- https://www.blog.brightcoding.dev/2026/05/22/stop-wasting-hours-hunting-quant-tools-awesome-systematic-trading-has-97-libraries
- https://paperswithbacktest.com/

---

## microsoft/agent-governance-toolkit

**なぜこの時期にトレンド入りしたか**

初回リリースは2026年4月2日のMicrosoft Open Source Blogでの発表だが、その後もv4.1.0リリースや.NET向けMCP拡張の発表(devblogs.microsoft.com)、アーキテクチャ解説記事(techcommunity.microsoft.com)など継続的な広報活動があり、トレンド当日の2026年7月29日付でも本ツールを紹介するブログ記事(cafeai.home.blog)が公開されている。単発の新機能公開というより、Microsoftによる継続的なコンテンツ発信のタイミングがトレンド入りと重なったと考えられる。

**類似サービス・システムとの違い**

NVIDIAのNeMo Guardrailsとの違いが明確。NeMo Guardrailsは主に対話フロー上のプロンプト・出力レベルで『レール』(トピック制限、安全性、脱獄対策)を追加するPythonライブラリであるのに対し、Agent Governance Toolkitはエージェントランタイム全体のツール呼び出し(アクション)レベルで動作し、実行前にYAML/OPA/Cedarベースの決定論的ポリシーエンジンで全ツールコールをインターセプトする。さらにゼロトラストのエージェントID管理、サンドボックスの権限リング、改ざん検知可能なMerkleツリー監査ログ、Python/TypeScript/.NET/Rust/Goの多言語SDKでSemantic Kernel・AutoGen・LangGraph・CrewAI・OpenAI Agents SDKと統合できる点が特徴で、単なるプロンプトフィルタというよりエージェント向け『OSカーネル』に近い設計思想を持つ。OWASP Agentic Top10やNIST AI RMF、EU AI Actへの準拠を明示的に掲げている点もガードレール系ツールとの違い。

**参考にした情報源**

- https://github.com/microsoft/agent-governance-toolkit
- https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/
- https://devblogs.microsoft.com/dotnet/announcing-agent-governance-toolkit-mcp-extensions-for-dotnet/
- https://cafeai.home.blog/2026/07/29/agent-governance-toolkit/
- https://techcommunity.microsoft.com/blog/linuxandopensourceblog/agent-governance-toolkit-architecture-deep-dive-policy-engines-trust-and-sre-for/4510105

---

## yorukot/superfile

**なぜこの時期にトレンド入りしたか**

特定の外的要因は確認できず、機能の完成度や既存コミュニティによる自然な拡大が主因と考えられる。本リポジトリは2024年3月から続く既存プロジェクトで直近のリリースはv1.6.0(2026年6月7日)、メインブランチへの最終プッシュは2026年6月30日であり、トレンド入りした7月27〜29日前後に対応する新リリースやニュース記事は見つからなかった。JetBrainsのオープンソース支援やブログ紹介記事(coddykit.com等)はあるが、いずれも当日と直接結びつく明確なトリガーではなく、GitHubのトレンドアルゴリズムが拾う日々のスター増加速度による周期的な再浮上とみられる。

**類似サービス・システムとの違い**

Rust製の新興TUIファイルマネージャーyazi(sxyazi/yazi)との違いが明確。yaziは非同期I/Oを軸にした高速な画像・動画プレビューとプラグインエコシステムで評価されているのに対し、superfileはGo言語とBubbleTeaフレームワークで構築され、アイコンや色分けされた複数パネルなど『GUIライクな見た目』の使いやすさを重視した設計。両者ともMITライセンスでクロスプラットフォームだが、大量ファイルを扱う際のパフォーマンスではRustの非同期処理を持つyaziが有利とされる一方、superfileはGUIファイラーからの移行者向けの視覚的な親しみやすさで差別化している。

**参考にした情報源**

- https://github.com/yorukot/superfile
- https://github.com/yorukot/superfile/releases
- https://awesome.ecosyste.ms/projects/github.com/yorukot/superfile
- https://www.coddykit.com/pages/blog-detail?id=512970&slug=superfile-the-open-source-terminal-file-manager-that-makes-the-command-line-beau

---

## bradautomates/claude-video

**なぜこの時期にトレンド入りしたか**

明確な外的要因あり。本リポジトリは2026年7月7日にGitHubトレンド全体で1位を獲得し、Trendshiftの記録では7月28日にも全言語トレンドに再浮上している。Towards AI掲載のブログ記事『Claude Couldn't Watch Videos. One Developer Fixed that With a Clever Trick』(2026年7月)など複数のブログで取り上げられ、Anthropicのエージェントスキル(Agent Skills)エコシステムの盛り上がりの中で『マルチモーダルで動画を解析できる好例』として繰り返し紹介されたことが、7月29日前後の再トレンド入りにつながったと考えられる。

**類似サービス・システムとの違い**

本リポジトリのフォークであるmathiaschu/watchとの違いが具体的で分かりやすい。オリジナルのclaude-videoは字幕取得を優先し、字幕がない場合はクラウドのWhisper API(GroqまたはOpenAI、要APIキー)にフォールバックするのに対し、フォーク版はmlx-whisperを用いて完全ローカル(Apple Silicon最適化、ネットワーク・APIキー不要)で文字起こしを行う設計に変更されている。また同種の独立実装であるNewuxtreme/watch-video-skillと比較すると、claude-videoは効率重視/バランス/トークン大量消費の3段階フレーム抽出モード、近似フレームの自動重複排除、YouTube/TikTok/Loom/Instagram/X/Vimeoという幅広い動画ソース対応を特徴としており、単なる字幕取得パイプラインより機能範囲が広い。

**参考にした情報源**

- https://github.com/bradautomates/claude-video
- https://trendshift.io/repositories/30967
- https://pub.towardsai.net/claude-couldnt-watch-videos-one-developer-fixed-that-with-a-clever-trick-here-s-how-it-works-76e6cc17c0db
- https://github.com/mathiaschu/watch
- https://github.com/Newuxtreme/watch-video-skill
