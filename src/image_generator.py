"""
Gemini APIを使用して画像生成を行うスクリプト（リファクタ済み）

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

from api.gemini_client import GeminiClient
from utils.audio_player import play_audio_async
from utils.config import Config
from utils.file_handler import save_audio_as_wav, save_image
from utils.prompt_loader import create_prompt_with_input


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


def main():
    """メイン処理を実行する"""
    try:
        # 設定とクライアントの初期化
        config = Config()
        client = GeminiClient()

        # ユーザーからの入力(行きたい場所)を受け取る
        user_location = get_user_location()

        # プロンプト作成
        final_prompt = create_prompt_with_input(
            'prompts/image_generation.txt', user_location)

        # 画像・テキスト生成
        print("\n画像を生成中...")
        text, image = client.generate_image_and_text(final_prompt)

        if not image:
            print("画像生成に失敗しました。")
            return

        print("\n=== 生成完了 ===")

        # 画像保存
        image_path = config.get_image_output_path()
        save_image(image, str(image_path))

        # 音声生成・保存
        audio_file_path = None
        if text:
            print(f"生成されたテキスト: {text}")
            print("テキストを音声に変換中...")

            audio_data = client.generate_speech(text)
            if audio_data:
                audio_file_path = config.get_audio_output_path()
                save_audio_as_wav(audio_data, str(audio_file_path))

        # 画像表示と音声再生を同時開始
        print("画像を表示し、音声を再生しています...")

        # 音声再生を非同期で開始
        if audio_file_path:
            play_audio_async(str(audio_file_path))

        # 画像を表示
        image.show()

    except FileNotFoundError as e:
        print(f"ファイルエラー: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
