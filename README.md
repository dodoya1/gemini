# gemini

Google Gemini API を使用したマルチモーダル AI アプリケーション

## 機能

- **テキスト生成**: Gemini 2.5 Flash モデルを使用したテキスト生成
- **画像生成**: Gemini 2.0 Flash Preview モデルを使用した高品質な風景写真生成
- **音声合成**: Gemini 2.5 Flash Preview TTS モデルによる日本語音声合成
- **マルチモーダル体験**: テキスト、画像、音声を組み合わせた統合体験
- **統一 API クライアント**: シングルトンパターンによる効率的な API 管理
- **モジュラー設計**: 機能別に分離された保守性の高いコード構成
- **カスタマイズ可能なプロンプトシステム**: 柔軟なプロンプト管理

## 環境セットアップ

1. Python 仮想環境の作成

```bash
python3 -m venv .venv
```

2. 仮想環境のアクティベート

```bash
source .venv/bin/activate
```

1. 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

4. 環境変数の設定

`.env`ファイルをプロジェクトのルートディレクトリに作成し、Gemini API キーを設定します：

```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

※ `your-api-key-here`は実際の Gemini API キーに置き換えてください。

## プロジェクト構成

```
gemini/
├── .env                         # 環境変数設定ファイル
├── .venv/                      # Python仮想環境
├── README.md                   # プロジェクト説明書
├── requirements.txt            # 依存パッケージ一覧
├── docs/                       # ドキュメント
│   └── image_generator_sequence.md  # 画像生成のシーケンス図
├── prompts/                    # プロンプトファイル格納ディレクトリ
│   ├── text_generation.txt    # テキスト生成用プロンプト
│   └── image_generation.txt   # 画像生成用プロンプト
├── outputs/                    # 生成ファイル保存ディレクトリ
│   ├── generated-image.png     # 生成された画像
│   └── generated-speech.wav    # 生成された音声
└── src/                        # ソースコードディレクトリ
    ├── api/                    # API関連モジュール
    │   ├── __init__.py
    │   └── gemini_client.py    # Gemini APIクライアント（統一）
    ├── utils/                  # ユーティリティモジュール
    │   ├── __init__.py
    │   ├── audio_player.py     # 音声再生機能
    │   ├── config.py           # 設定管理
    │   ├── file_handler.py     # ファイル操作
    │   └── prompt_loader.py    # プロンプト読み込み
    ├── image_generator.py      # 画像生成モジュール
    └── text_generator.py       # テキスト生成モジュール
```

## 使用方法

### テキスト生成

1. 仮想環境が有効になっていることを確認
2. 必要に応じて`prompts/text_generation.txt`のプロンプトを編集
3. 以下のコマンドを実行：

```bash
python src/text_generator.py
```

### 画像生成（メイン機能）

インタラクティブな風景写真生成体験を提供します：

1. 仮想環境が有効になっていることを確認
2. 以下のコマンドを実行：

```bash
python src/image_generator.py
```

3. **ユーザーインタラクション**：
   - プログラムが行きたい場所の入力を求めます
   - 例：「富士山の頂上から見た日の出」「火星の赤い大地」「オーロラが輝く北極の夜空」
4. **自動処理**：
   - 入力された場所をもとに高品質な風景写真を生成
   - 生成過程の説明テキストも同時に作成
   - テキストを日本語音声に変換
   - 画像表示と音声再生を同時実行

**出力**：

- 画像：`outputs/generated-image.png`
- 音声：`outputs/generated-speech.wav`

## 依存パッケージ

- **google-genai**: Gemini API クライアントライブラリ
- **python-dotenv**: 環境変数管理（API キー管理用）
- **pillow**: 画像処理ライブラリ（画像表示・操作用）

## 技術仕様

### 使用モデル

- **テキスト生成**: `gemini-2.5-flash`
- **画像生成**: `gemini-2.0-flash-preview-image-generation`
- **音声合成**: `gemini-2.5-flash-preview-tts`

### サポートプラットフォーム

- **macOS**: `afplay`コマンドを使用した音声再生
- **Windows**: `start`コマンドを使用した音声再生
- **Linux**: `aplay`コマンドを使用した音声再生

### 音声設定

- **音声品質**: 24kHz, 16-bit, モノラル
- **音声モデル**: "Kore"（日本語対応）
- **出力形式**: WAV 形式

## アーキテクチャの特徴

### 統一 API クライアント

- `GeminiClient`クラスによるシングルトンパターンの実装
- 全ての生成機能（テキスト、画像、音声）を統一的に管理
- エラーハンドリングとリトライ処理の統合

### モジュラー設計

- **API 層**: `src/api/` - Gemini API との通信処理
- **ユーティリティ層**: `src/utils/` - 共通機能（設定、ファイル処理、音声再生）
- **アプリケーション層**: `src/` - メイン機能（画像生成、テキスト生成）

### 設定管理

- 環境変数の統一管理
- 出力ディレクトリの自動作成と管理
- プラットフォーム依存処理の抽象化

## 注意事項

- 仮想環境を終了する場合は`deactivate`コマンドを実行してください
- `.env`および`.venv`ディレクトリはバージョン管理から除外されています
- **Gemini API キーは適切に管理し、公開リポジトリにコミットしないよう注意してください**
- 音声再生には各プラットフォーム対応のオーディオコマンドが必要です
- 大きな画像や長いテキストの処理には時間がかかる場合があります

## トラブルシューティング

### 音声再生に関する問題

- macOS で音声が再生されない場合は、`afplay`コマンドが利用可能か確認してください
- Linux で音声が再生されない場合は、`alsa-utils`パッケージをインストールしてください
- Windows で音声が再生されない場合は、システムの音声設定を確認してください
