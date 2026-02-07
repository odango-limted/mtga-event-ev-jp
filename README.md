# MTG Arena Event EV Calculator (JP)

MTGアリーナのイベント（ドラフト、シールド、アリーナ・ダイレクト等）の期待値（EV）を計算し、可視化するWebアプリケーションです。
Streamlitを使用して構築されており、ユーザー独自の勝率や通貨レート設定に基づいて収支分析が可能です。

## 主な機能

- **イベント設定**: プレミアドラフト、マッチドラフト、アリーナ・ダイレクトなど、主要なイベントのプリセットを搭載。カスタム設定も可能。
- **期待値計算**: 勝率ごとの期待値をジェムまたは日本円換算で算出。
- **可視化**:
  - **期待値曲線**: 勝率に応じた収支の変化をグラフ化し、損益分岐点を表示。
  - **結果分布**: 特定の勝率における結果（○勝✕敗）の確率分布と、それぞれの収支を色分け表示。
- **高度な設定**:
  - ジェム、ゴールド、パック、ボックスの価値をカスタマイズ可能。
  - 参加賞（ドラフト等で得られるカード資産）の価値をEVに含めることが可能。
  - アリーナ・ダイレクト（プレイブースター/コレクターブースター）対応。

## デモ

Streamlit Community Cloudで稼働中のデモ: [https://mtga-event-ev-jp-lwpucsrdr8od88yrutaewq.streamlit.app/]

## ローカルでの実行方法

1. リポジトリをクローンします。
   ```bash
   git clone https://github.com/odango-limted/mtga-event-ev-jp.git
   cd mtga-event-ev-jp
   ```

2. 依存関係をインストールします。
   ```bash
   pip install -r requirements.txt
   ```

3. アプリを起動します。
   ```bash
   streamlit run app.py
   ```

## 技術スタック

- Python 3.11+
- Streamlit
- Plotly
- Pandas
- Numpy

## ライセンス
[MIT License]
このツールは、ファンコンテンツ・ポリシーに沿った非公式のファンコンテンツです。ウィザーズ社の認可/許諾は得ていません。題材の一部に、ウィザーズ・オブ・ザ・コースト社の財産を含んでいます。©Wizards of the Coast LLC
