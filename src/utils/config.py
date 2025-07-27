"""
アプリケーション設定管理

環境変数の読み込み、デフォルト設定、出力ディレクトリの管理を行います。
"""

from pathlib import Path

from dotenv import load_dotenv


class Config:
    """アプリケーション設定クラス"""

    def __init__(self):
        load_dotenv()
        self.output_dir = Path("outputs")

    def ensure_output_directory(self) -> Path:
        """
        出力ディレクトリの作成と取得

        Returns:
            Path: 出力ディレクトリのパス
        """
        self.output_dir.mkdir(exist_ok=True)
        return self.output_dir

    def get_image_output_path(self, filename: str = "generated-image.png") -> Path:
        """
        画像出力パスの取得

        Args:
            filename (str): ファイル名

        Returns:
            Path: 画像ファイルのフルパス
        """
        return self.ensure_output_directory() / filename

    def get_audio_output_path(self, filename: str = "generated-speech.wav") -> Path:
        """
        音声出力パスの取得

        Args:
            filename (str): ファイル名

        Returns:
            Path: 音声ファイルのフルパス
        """
        return self.ensure_output_directory() / filename
