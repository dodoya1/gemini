"""
音声再生処理

プラットフォーム別の音声再生機能を提供します。
"""

import subprocess
import sys
from typing import Optional


def play_audio_async(audio_file: str) -> Optional[subprocess.Popen]:
    """
    プラットフォーム別音声再生（非同期）

    Args:
        audio_file (str): 再生する音声ファイルのパス

    Returns:
        Optional[subprocess.Popen]: 音声再生プロセス。失敗時はNone
    """
    try:
        if sys.platform.startswith("darwin"):  # macOS
            return subprocess.Popen(["afplay", audio_file])
        elif sys.platform.startswith("win32"):  # Windows
            return subprocess.Popen(["start", audio_file], shell=True)
        elif sys.platform.startswith("linux"):  # Linux
            return subprocess.Popen(["aplay", audio_file])
        else:
            print(f"お使いのプラットフォーム（{sys.platform}）での音声再生はサポートされていません。")
            return None
    except FileNotFoundError:
        print("音声再生コマンドが見つかりません。")
        return None
    except Exception as e:
        print(f"音声再生エラー: {e}")
        return None
