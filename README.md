# gemini

Google Gemini API を使用したテキスト生成および画像生成 AI アプリケーション

## 機能

- テキスト生成 (Gemini 2.5 Flash モデル使用)
- 画像生成 (Gemini 2.0 Flash Preview モデル使用)
- カスタマイズ可能なプロンプトシステム

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
├── .env                    # 環境変数設定ファイル
├── .venv/                 # Python仮想環境
├── prompts/              # プロンプトファイル格納ディレクトリ
│   └── image_generation.txt  # 画像生成用プロンプト
├── requirements.txt      # 依存パッケージ一覧
└── src/                 # ソースコードディレクトリ
    ├── text_generator.py   # テキスト生成モジュール
    └── image_generator.py  # 画像生成モジュール
```

## 使用方法

### テキスト生成

1. 仮想環境が有効になっていることを確認
2. 必要に応じて`prompts/text_generation.txt`のプロンプトを編集
3. 以下のコマンドを実行：

```bash
python src/text_generator.py
```

### 画像生成

1. 仮想環境が有効になっていることを確認
2. 必要に応じて`prompts/image_generation.txt`のプロンプトを編集
3. 以下のコマンドを実行：

```bash
python src/image_generator.py
```

画像は自動的に`generated_images/gemini-native-image.png`として保存され、生成後に表示されます。

## 依存パッケージ

- google-genai: Gemini API クライアント
- python-dotenv: 環境変数管理
- pillow: 画像処理

## 注意事項

- 仮想環境を終了する場合は`deactivate`コマンドを実行してください
- `.env`および`.venv`ディレクトリはバージョン管理から除外されています
- Gemini API キーは適切に管理し、公開リポジトリにコミットしないよう注意してください
