"""
Gemini APIを使用してテキスト生成を行うスクリプト

このスクリプトは、Google Cloud の Gemini API を使用して、
テキストプロンプトに対する応答を生成します。Gemini-2.5-Flash モデルを
使用してテキスト生成を行います。

参考資料:
- Gemini API Text Generation ドキュメント
https://ai.google.dev/gemini-api/docs/text-generation?hl=ja

注意:
- 環境変数に適切なAPI keyの設定が必要です
"""

from typing import Optional

from dotenv import load_dotenv
from google import genai


def generate_text_response(prompt: str, model: str = "gemini-2.5-flash") -> Optional[str]:
    """
    Geminiを使用してテキスト応答を生成する

    Args:
        prompt (str): 生成のためのプロンプト
        model (str, optional): 使用するモデル名. デフォルトは "gemini-2.5-flash"

    Returns:
        Optional[str]: 生成されたテキスト。エラー時はNone
    """
    client = genai.Client()

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None


def load_prompt(file_path: str) -> str:
    """
    プロンプトファイルを読み込む

    Args:
        file_path (str): プロンプトファイルのパス

    Returns:
        str: プロンプトの内容
    """
    with open(file_path, 'r') as file:
        return file.read().strip()


def main():
    """メイン処理を実行する"""
    load_dotenv()

    prompt = load_prompt('prompts/text_generation.txt')
    response_text = generate_text_response(prompt)

    if response_text:
        print(response_text)
    else:
        print("テキスト生成に失敗しました。")


if __name__ == "__main__":
    main()
