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

from text_to_speech import text_to_speech


def load_prompt_template(file_path: str) -> str:
    """
    プロンプトテンプレートファイルを読み込む

    Args:
        file_path (str): プロンプトテンプレートファイルのパス

    Returns:
        str: プロンプトテンプレートの内容
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def create_prompt(template: str, location: str) -> str:
    """
    プロンプトテンプレートにユーザーの入力した場所を挿入する

    Args:
        template (str): プロンプトテンプレート
        location (str): ユーザーが入力した場所

    Returns:
        str: 完成したプロンプト
    """
    return template + f"\n\n{location}"


def get_user_location() -> str:
    """
    ユーザーから場所の入力を受け取る

    Returns:
        str: ユーザーが入力した場所
    """
    print("どこの風景写真を生成したいですか？")
    print("例: 富士山の頂上から見た日の出")
    print("例: 火星の赤い大地")
    print("例: オーロラが輝く北極の夜空")
    print()

    while True:
        location = input("どこに行きたい？: ").strip()
        if location:
            return location
        print("場所を入力してください。")


def generate_and_save_image(prompt: str, output_path: str) -> Tuple[str, Image.Image]:
    """
    Geminiを使用して画像を生成し、保存する

    Args:
        prompt (str): 画像生成用のプロンプト
        output_path (str): 生成した画像の保存先パス

    Returns:
        Tuple[str, Image.Image]: 生成されたテキストと画像のタプル
    """
    print("\n画像を生成中...")

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

    try:
        # ユーザーから場所の入力を受け取る
        user_location = get_user_location()

        # プロンプトテンプレートを読み込む
        prompt_template = load_prompt_template('prompts/image_generation.txt')

        # プロンプトテンプレートにユーザーの入力を挿入
        final_prompt = create_prompt(prompt_template, user_location)

        # 出力ファイルパスを生成
        output_path = output_dir / 'gemini-native-image.png'

        # 画像生成と保存
        text, image = generate_and_save_image(final_prompt, str(output_path))

        print("\n=== 生成完了 ===")
        if text:
            print(f"生成されたテキスト: {text}")

            print("テキストを音声に変換中...")
            audio_path = output_dir / 'generated_text_speech.wav'
            text_to_speech(text, str(audio_path))
            print(f"音声ファイルを保存しました: {audio_path}")

        if image:
            print(f"画像を保存しました: {output_path}")
            print("画像を表示しています...")
            image.show()

    except FileNotFoundError:
        print("エラー: prompts/image_generation.txt ファイルが見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
