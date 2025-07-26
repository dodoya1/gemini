# Image Generator シーケンス図

このドキュメントは、`src/image_generator.py` の処理フローを表すシーケンス図です。

## 概要

`image_generator.py` は以下の主要な処理を行います：

1. ユーザーからの入力の受付
2. プロンプトテンプレートの読み込みと結合
3. Gemini API を使用した画像・テキスト生成
4. 生成されたテキストの音声変換
5. 画像表示と音声再生の同時実行

## シーケンス図

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Main as main()
    participant UserInput as get_user_location()
    participant PromptLoader as load_prompt_template()
    participant PromptCreator as create_prompt()
    participant ImageGen as generate_and_save_image()
    participant GeminiAPI as Gemini API
    participant TTS as text_to_speech()
    participant AudioPlayer as play_audio_async()
    participant ImageViewer as image.show()

    Note over Main: プログラム開始
    Main->>Main: load_dotenv()
    Main->>Main: output_dir.mkdir(exist_ok=True)

    Main->>UserInput: get_user_location()
    UserInput->>User: どこの風景写真を生成したいですか？
    User->>UserInput: 場所を入力（例：富士山の頂上）
    UserInput->>Main: user_location

    Main->>PromptLoader: load_prompt_template('prompts/image_generation.txt')
    PromptLoader->>Main: prompt_template

    Main->>PromptCreator: create_prompt(template, user_location)
    PromptCreator->>Main: final_prompt

    Main->>ImageGen: generate_and_save_image(final_prompt, output_path)

    Note over ImageGen: 画像生成処理開始
    ImageGen->>User: "画像を生成中..."
    ImageGen->>GeminiAPI: models.generate_content()
    Note over GeminiAPI: gemini-2.0-flash-preview-image-generation<br/>モデルで画像とテキストを生成
    GeminiAPI->>ImageGen: response (text + image)

    ImageGen->>ImageGen: Image.open(BytesIO(image_data))
    ImageGen->>ImageGen: generated_image.save(output_path)
    ImageGen->>Main: (text_response, generated_image)

    Note over Main: 音声変換処理
    alt テキストが生成された場合
        Main->>User: "テキストを音声に変換中..."
        Main->>TTS: text_to_speech(text, audio_file_path)
        Note over TTS: gemini-2.5-flash-preview-tts<br/>モデルで音声生成
        TTS->>TTS: save_audio_as_wav()
        TTS->>Main: audio_file_path
        Main->>User: "音声ファイルを保存しました"
    end

    Note over Main: 画像表示と音声再生
    Main->>User: "画像を表示し、音声を再生しています..."

    par 並行処理
        Main->>AudioPlayer: play_audio_async(audio_file_path)
        Note over AudioPlayer: プラットフォーム別コマンド<br/>(afplay/start/aplay)で非同期再生
    and
        Main->>ImageViewer: image.show()
        Note over ImageViewer: デフォルト画像ビューアで表示
    end

    Note over Main: 処理完了
```
