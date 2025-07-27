"""
Gemini API専用クライアント

このモジュールは、Google Gemini APIとの連携を統一的に管理します。
シングルトンパターンを使用してAPIクライアントのインスタンスを管理し、
各種生成機能（テキスト、画像、音声）の共通処理を提供します。
"""

from io import BytesIO
from typing import Optional, Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types  # type: ignore
from PIL import Image  # type: ignore


class GeminiClient:
    """Gemini APIクライアントのシングルトン"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """クライアントの初期化"""
        load_dotenv()
        self.client = genai.Client()

    def generate_text(self, prompt: str, model: str = "gemini-2.5-flash") -> Optional[str]:
        """
        テキスト生成の共通処理

        Args:
            prompt (str): 生成のためのプロンプト
            model (str, optional): 使用するモデル名. デフォルトは "gemini-2.5-flash"

        Returns:
            Optional[str]: 生成されたテキスト。エラー時はNone
        """
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"テキスト生成エラー: {e}")
            return None

    def generate_image_and_text(self, prompt: str) -> Tuple[Optional[str], Optional[Image.Image]]:
        """
        画像+テキスト生成の共通処理

        Args:
            prompt (str): 画像生成用のプロンプト

        Returns:
            Tuple[Optional[str], Optional[Image.Image]]: 生成されたテキストと画像のタプル
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            text_response = None
            generated_image = None

            # レスポンスの各パートをチェック
            for part in response.candidates[0].content.parts:
                # テキストパートの処理
                if part.text is not None:
                    text_response = part.text
                # 画像パートの処理
                elif part.inline_data is not None:
                    generated_image = Image.open(
                        BytesIO(part.inline_data.data))

            return text_response, generated_image

        except Exception as e:
            print(f"画像・テキスト生成エラー: {e}")
            return None, None

    def generate_speech(self, text: str, voice_name: str = "Kore") -> Optional[bytes]:
        """
        音声生成の共通処理

        Args:
            text (str): 読み上げるテキスト
            voice_name (str): 使用する音声名（デフォルト: "Kore"）

        Returns:
            Optional[bytes]: 生成された音声データ（PCM形式）。エラー時はNone
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                )
            )

            return response.candidates[0].content.parts[0].inline_data.data

        except Exception as e:
            print(f"音声生成エラー: {e}")
            return None
