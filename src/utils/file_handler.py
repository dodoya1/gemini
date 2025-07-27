"""
ファイル保存・読み込み処理

画像・音声ファイルの保存処理を統一的に管理します。
"""

import wave

from PIL import Image  # type: ignore


def save_image(image: Image.Image, file_path: str) -> None:
    """
    画像保存の共通処理

    Args:
        image (Image.Image): 保存する画像
        file_path (str): 保存先のファイルパス
    """
    try:
        image.save(file_path)
        print(f"画像を保存しました: {file_path}")
    except Exception as e:
        print(f"画像保存エラー: {e}")


def save_audio_as_wav(audio_data: bytes, file_path: str,
                      channels: int = 1, rate: int = 24000, sample_width: int = 2) -> None:
    """
    音声ファイル保存の共通処理

    Args:
        audio_data (bytes): PCM音声データ
        file_path (str): 保存先のファイルパス
        channels (int): チャンネル数（デフォルト: 1）
        rate (int): サンプリングレート（デフォルト: 24000）
        sample_width (int): サンプル幅（デフォルト: 2）
    """
    try:
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(audio_data)
        print(f"音声ファイルを保存しました: {file_path}")
    except Exception as e:
        print(f"音声保存エラー: {e}")
