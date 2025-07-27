"""
Gemini APIを使用してテキスト生成を行うスクリプト（リファクタ済み）

このスクリプトは、Google Cloud の Gemini API を使用して、
テキストプロンプトに対する応答を生成します。Gemini-2.5-Flash モデルを
使用してテキスト生成を行います。

参考資料:
- Gemini API Text Generation ドキュメント
https://ai.google.dev/gemini-api/docs/text-generation?hl=ja

注意:
- 環境変数に適切なAPI keyの設定が必要です
"""

from api.gemini_client import GeminiClient
from utils.prompt_loader import load_prompt_file


def main():
    """メイン処理を実行する"""
    try:
        # Gemini APIクライアントの取得
        client = GeminiClient()

        # プロンプトファイルの読み込み
        prompt = load_prompt_file('prompts/text_generation.txt')

        # テキスト生成
        response_text = client.generate_text(prompt)

        if response_text:
            print(response_text)
        else:
            print("テキスト生成に失敗しました。")

    except FileNotFoundError as e:
        print(f"ファイルエラー: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
