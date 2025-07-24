"""
Gemini APIを使用して画像生成を行うスクリプト

このスクリプトは、Google Cloud の Gemini API を使用して、
テキストプロンプトから画像を生成します。Gemini-2.0-Flash-Preview モデルを使用し、
生成された画像をローカルに保存します。

参考資料:
- Gemini API Image Generation ドキュメント
  https://ai.google.dev/gemini-api/docs/image-generation?hl=ja

注意:
- 環境変数に適切なAPI keyの設定が必要です
- プロンプトは 'prompts/image_generation.txt' から読み込まれます
"""

from io import BytesIO
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types  # type: ignore
from PIL import Image  # type: ignore


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


def generate_and_save_image(prompt: str, output_path: str) -> Tuple[str, Image.Image]:
    """
    Geminiを使用して画像を生成し、保存する

    Args:
        prompt (str): 画像生成用のプロンプト
        output_path (str): 生成した画像の保存先パス

    Returns:
        Tuple[str, Image.Image]: 生成されたテキストと画像のタプル
    """
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    text_response = ""
    generated_image = None

    # レスポンスの各パートをチェック（テキストと画像の両方が含まれる可能性がある）
    for part in response.candidates[0].content.parts:
        # テキストパートの処理
        if part.text is not None:
            text_response = part.text
        # 画像パートの処理
        elif part.inline_data is not None:
            # バイナリデータからPIL Image オブジェクトを作成
            generated_image = Image.open(BytesIO((part.inline_data.data)))
            # 指定されたパスに画像を保存
            generated_image.save(output_path)

    return text_response, generated_image


def main():
    """メイン処理を実行する"""
    load_dotenv()

    # 画像保存用ディレクトリの作成（存在しない場合）
    output_dir = Path('generated_images')
    output_dir.mkdir(exist_ok=True)

    prompt = load_prompt('prompts/image_generation.txt')
    output_path = output_dir / 'gemini-native-image.png'

    text, image = generate_and_save_image(prompt, str(output_path))

    if text:
        print(text)
    if image:
        print(f"画像を保存しました: {output_path}")
        image.show()


if __name__ == "__main__":
    main()
