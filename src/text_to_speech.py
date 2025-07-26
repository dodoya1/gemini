"""
Gemini APIを使用してテキスト読み上げを行うモジュール

このモジュールは、Google Cloud の Gemini API を使用して、
テキストを音声に変換し、WAVファイルとして保存します。
"""

import wave

from google import genai
from google.genai import types  # type: ignore


def save_audio_as_wav(filename: str, pcm_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> None:
    """
    PCMデータをWAVファイルとして保存する

    Args:
        filename (str): 保存するファイル名
        pcm_data (bytes): PCM音声データ
        channels (int): チャンネル数（デフォルト: 1）
        rate (int): サンプリングレート（デフォルト: 24000）
        sample_width (int): サンプル幅（デフォルト: 2）
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)


def text_to_speech(text: str, output_filename: str = "output.wav", voice_name: str = "Kore") -> str:
    """
    テキストを音声に変換してWAVファイルとして保存する

    Args:
        text (str): 読み上げるテキスト
        output_filename (str): 出力ファイル名（デフォルト: "output.wav"）
        voice_name (str): 使用する音声名（デフォルト: "Kore"）

    Returns:
        str: 保存されたファイルのパス
    """
    client = genai.Client()

    response = client.models.generate_content(
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

    audio_data = response.candidates[0].content.parts[0].inline_data.data
    save_audio_as_wav(output_filename, audio_data)

    return output_filename
