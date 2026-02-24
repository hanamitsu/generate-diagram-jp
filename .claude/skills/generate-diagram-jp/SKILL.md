---
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - "Bash(python *)"
---

# 日本語図解生成（generate-diagram-jp）

PaperBananaの手法に基づき、日本語対応の図解を生成する。
Claude（自身）がRetriever/Planner/Stylist/Criticを担当し、画像生成のみGemini Imagenを使用する。

3つのスタイルモード（academic / balanced / graphic-note）を切り替え可能。

## 使い方

```
/generate-diagram-jp input.txt "図のキャプション"
/generate-diagram-jp input.txt "図のキャプション" --style graphic-note
```

- `$ARGUMENTS[0]`: 入力テキストファイルのパス
- `$ARGUMENTS[1]`: 図のキャプション（省略時はユーザーに質問する）
- `--style` オプション: `academic` / `balanced`（デフォルト）/ `graphic-note`

---

## パイプライン

以下の手順を順番に実行する。各工程の出力形式を厳守すること。

### Step 1: 入力読み取り

1. `$ARGUMENTS[0]` のファイルを Read tool で読み込む
2. `$ARGUMENTS[1]` が提供されていればキャプションとして使用。なければユーザーに質問する
3. `--style` オプションがあればそのモードを使用。なければ `balanced` をデフォルトとする
   - `academic`: 学術論文風モノクロ構造
   - `balanced`: 構造的な整然さ＋グラレコ風の温かみ（デフォルト）
   - `graphic-note`: グラレコ寄りの視覚的リッチさ
4. 出力先パスを決定する（入力ファイルと同じディレクトリに `[入力ファイル名]_diagram.png`）

### Step 2: 参照例選定（Retriever）

`data/reference_sets/index.json` を Read tool で読み込む。

入力テキストとキャプションを分析し、以下の優先度で参照例を選定する：
1. **図種（Visual Intent）が同じ**（Framework, Pipeline, Comparison, Module等）— 最優先
2. **研究トピックが同じ**（agent_reasoning, vision_perception, generative_learning, science_applications）
3. 図種 > トピックの優先度（PaperBanana論文の設計に準拠）

**出力形式（厳守）：**
```json
{"selected_ids": ["id1", "id2", "id3"]}
```

- 3〜5件を選定する
- **ID整合性チェック**: 選定したIDがindex.jsonに実在するか確認。不正IDは除外
- 有効ID 0件の場合: category一致で再選定。それも0件なら図種キーワードで再選定

### Step 3: 参照例の視覚的学習

選定した参照例の画像を Read tool で読み込む。
画像パスは `data/reference_sets/` + index.jsonの `image_path` フィールド。

各参照画像について、以下を観察する：
- レイアウト構成（フロー方向、ボックス配置、グルーピング）
- アイコンの使い方（種類、サイズ、配置位置）
- 空間構成（ホワイトスペース、要素間隔、グリッド整列）

画像の読み込みに失敗した場合：
- 一部失敗: 成功分のみで続行
- 全件失敗: index.jsonのcaption/source_contextのテキスト情報のみで続行

### Step 4: 記述生成（Planner）

参照例から学んだレイアウトパターンを踏まえ、入力テキストから図の詳細な視覚記述を生成する。

**記述の冒頭に、選択されたスタイルモードに応じたタッチ指定を含めること：**

- `academic`: 「クリーンで学術的なベクター図。白背景にモノクロ構造。色はアイコンのみ。」
- `balanced`: 「グラフィックレコーディング風の手描きタッチの横長図解。カラフルなソフトトーンのボックス。手書き風の太い矢印と吹き出し。リボンバナー見出しとマーカーハイライト。キャラクターやマスコットは使用しない。」
- `graphic-note`: 「グラフィックレコーディング風の手描きタッチの横長図解。カラフルなソフトトーンのボックス。手書き風の太い矢印と吹き出し。キャラクターやマスコットは原則使用しない。」

記述に含めるべき要素（PaperBanana planner.txt準拠）：

1. **全体レイアウト**: フロー方向（左→右 or 上→下）、主要フェーズ数
2. **各コンポーネント**: ボックスのラベル（日本語で明記）、形状、サイズ関係
3. **接続関係**: 矢印の方向、データフローの流れ
4. **グルーピング**: 関連要素のまとまり、破線枠の有無
5. **アイコン指定**: 各要素に付与するアイコンの種類と色（自然言語で）
6. **入出力**: 図の始点と終点
7. **日本語ラベル**: 全ラベル・注釈を日本語で明示的に記述に含める
8. **モード固有の装飾**: style-guide.mdのモード別ルールに従い、装飾要素（バナー、吹き出し、マーカーハイライト等）を記述に含める

記述は可能な限り詳細に書く。曖昧な記述は生成画像の品質を下げる。

### Step 5: スタイル精錬（Stylist）

`.claude/skills/generate-diagram-jp/style-guide.md` を Read tool で読み込み、
Step 4の記述を**選択されたスタイルモードのルール**に基づいて精錬する。

精錬の重点（PaperBanana stylist.txt準拠 + モード対応）：

1. **モード準拠の徹底**: style-guide.mdの該当モード（academic/balanced/graphic-note）のルールに従う
   - academic: 構造はモノクロ、色はアイコンのみ
   - balanced: カラフルなソフトトーンボックス、太い手描き風矢印、装飾要素（リボンバナー・吹き出し・マーカーハイライト・丸数字）を積極使用。キャラクター/マスコットは使用しない
   - graphic-note: カラフルなソフトトーン、手描き風タッチ強め、装飾要素（バナー・吹き出し・マーカーハイライト）を積極使用。キャラクターは原則使用しない（ユーザー要求時のみ）
2. **最小限の介入**: 記述が既に良ければ書き換えない。改善が必要な箇所のみ編集
3. **図種の多様性の尊重**: フローチャート・アーキテクチャ図・パイプラインなどの固有慣習を活かす
4. **詳細の補完**: 曖昧な部分に具体的な自然言語の視覚指示を追加
5. **内容の保持**: コンポーネント・接続・ラベルを追加/削除/変更しない
6. **空間的明瞭さ**: フロー方向統一、同レベル同サイズ、グリッド整列、ホワイトスペース（全モード共通）

**禁止事項チェック（記述Lint）:**

- hex/px/pt/CSS風の数値指定 → 自然言語に変換
- 図タイトルの描画指示 → 削除
- 英語ラベル → 日本語に変換
- テキスト過多のボックス → 簡潔化

精錬後の記述のみを出力する。説明や前置きは付けない。

### Step 6: 画像生成（Visualizer）

精錬された記述をファイルに保存し、Gemini Imagenで画像を生成する。

```bash
python .claude/skills/generate-diagram-jp/scripts/gemini_generate.py \
  --description-file /tmp/diagram_description.txt \
  --style <選択されたモード> \
  --output <出力先パス>
```

1. Write tool で精錬された記述を `/tmp/diagram_description.txt` に保存
2. Bash で上記コマンドを実行（`--style` にStep 1で決定したモードを渡す）
3. 正常終了: 出力パスが標準出力に表示される
4. 異常終了: エラーメッセージを確認し、1回だけ再試行。再失敗なら停止して理由を報告
5. 生成後、ファイルサイズが0でないことを確認（`ls -la` で検証）

### Step 7: 画像評価（Critic）

生成画像を Read tool で読み込み、以下の評価基準で判定する。

**Primary次元（毎回評価 — vetoあり）：**

Faithfulness（忠実性）:
- 入力テキストの主要概念が図に反映されているか
- 主要ラベルが存在し読めるか（中心概念、入出力、フェーズ見出し、固有名詞）
- 架空の要素が追加されていないか、論理的矛盾がないか
- 明確な文字化け（読めないレベル）がないか
- 微妙な誤字（漢字1文字の間違い等）はvetoしない → 最終報告に含める

Readability（読みやすさ）:
- 2秒以内にメインフローが把握できるか
- テキストの重なり、スパゲッティ矢印、読めないフォントサイズがないか
- フロー方向が統一されているか

**評価結果の出力形式（厳守）：**

Write tool で以下のJSON を `/tmp/critic_result.json` に保存する：
```json
{
  "critic_suggestions": ["改善点1", "改善点2"],
  "revised_description": "修正版の記述全文。問題なしの場合はnull"
}
```

**JSONパース検証（Criticのみ実施）：**
```bash
python -c "import json; f=open('/tmp/critic_result.json','r',encoding='utf-8'); data=json.load(f); assert isinstance(data.get('critic_suggestions',[]),list); print('ok')"
```
- パース成功: 結果に基づいて判定
- パース失敗: `suggestions=[], revised_description=null` として停止（保守的フォールバック）

### Step 8: 停止判定と改善ループ

**停止判定フロー：**
1. `critic_suggestions` が空 → 完了。ユーザーに画像を提示
2. `critic_suggestions` が非空 かつ `revised_description` が非null → Step 6に戻って再生成
3. `critic_suggestions` が非空 かつ `revised_description` が null → 完了（要改善点を報告して終了）
4. 最大2イテレーション到達 → 残課題を明示して終了

**最終候補のみ: Secondary次元の評価**
完了時、最終画像に対して以下も報告する（vetoはしない）：

- Conciseness: テキスト過多のボックスがないか
- Aesthetics: 選択されたスタイルモードへの準拠度（academicならモノクロ構造、balanced/graphic-noteならカラフルなソフトトーン＋手描きタッチ＋装飾要素の活用度。balancedはキャラクター不使用を確認）

**最終出力：**
1. 生成画像のパスをユーザーに提示
2. 評価サマリー（改善点があれば記載）
3. 微妙な誤字等のvetoしなかった問題点があれば付記