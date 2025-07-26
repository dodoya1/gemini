"""
Gemini APIを使用してテキスト読み上げを行うモジュール

このモジュールは、Google Cloud の Gemini API を使用して、
テキストを音声に変換し、WAVファイルとして保存します。
"""

import wave
import subprocess
import sys

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


def play_audio(audio_file: str) -> None:
    """
    音声ファイルを再生する
    
    Args:
        audio_file (str): 再生する音声ファイルのパス
    """
    try:
        if sys.platform.startswith("darwin"):  # macOS
            subprocess.run(["afplay", audio_file], check=True)
        elif sys.platform.startswith("win32"):  # Windows
            subprocess.run(["start", audio_file], shell=True, check=True)
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["aplay", audio_file], check=True)
        else:
            print(f"お使いのプラットフォーム（{sys.platform}）での音声再生はサポートされていません。")
    except subprocess.CalledProcessError:
        print(f"音声ファイル {audio_file} の再生に失敗しました。")
    except FileNotFoundError:
        print("音声再生コマンドが見つかりません。")


def text_to_speech_and_play(text: str, output_filename: str = "output.wav", voice_name: str = "Kore") -> str:
    """
    テキストを音声に変換、保存、再生する
    
    Args:
        text (str): 読み上げるテキスト
        output_filename (str): 出力ファイル名（デフォルト: "output.wav"）
        voice_name (str): 使用する音声名（デフォルト: "Kore"）
        
    Returns:
        str: 保存されたファイルのパス
    """
    file_path = text_to_speech(text, output_filename, voice_name)
    play_audio(file_path)
    return file_path
