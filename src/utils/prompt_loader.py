"""
プロンプト読み込み関連の共通処理

プロンプトファイルの読み込みとテンプレート処理を統一的に管理します。
"""


def load_prompt_file(file_path: str) -> str:
    """
    プロンプトファイルを読み込む共通関数

    Args:
        file_path (str): プロンプトファイルのパス

    Returns:
        str: プロンプトの内容

    Raises:
        FileNotFoundError: ファイルが見つからない場合
        UnicodeDecodeError: ファイルの読み込みに失敗した場合
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"プロンプトファイルが見つかりません: {file_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"ファイルの読み込みに失敗しました: {file_path}")


def create_prompt_with_input(template_path: str, user_input: str) -> str:
    """
    テンプレート + ユーザー入力でプロンプト作成

    Args:
        template_path (str): プロンプトテンプレートファイルのパス
        user_input (str): ユーザーの入力内容

    Returns:
        str: 完成したプロンプト
    """
    template = load_prompt_file(template_path)
    return f"{template}\n\n{user_input}"
