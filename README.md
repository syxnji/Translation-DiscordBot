# Discord Translation Bot

Google Gemini APIを使用したDiscord翻訳ボット。日本語と英語の相互翻訳を自動で行います。

## セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定
`.env.example`を`.env`にコピーして、以下の値を設定してください：

```
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

#### Discord Bot Token の取得
1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 新しいアプリケーションを作成
3. "Bot"タブでトークンを取得
4. 必要な権限（Send Messages, Read Message History）を設定

#### Gemini API Key の取得
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. APIキーを作成

### 3. ボットの起動
```bash
python bot.py
```

## 使用方法

### コマンド

- `!translate <テキスト>` - テキストを翻訳
- `!t <テキスト>` - 翻訳の短縮コマンド  
- `!translation` - 自動翻訳のON/OFF切り替え
- `!hello` - 挨拶

### 翻訳モード

#### 1. 自動翻訳モード（推奨）
- `!translation` でON/OFF切り替え
- ON時：すべてのメッセージ（コマンド以外）を自動翻訳
- OFF時：手動コマンドのみ有効

#### 2. メッセージベース翻訳
- `translate: こんにちは` - 日本語を英語に翻訳
- `翻訳: Hello world` - 英語を日本語に翻訳

## 機能

- **自動翻訳モード**: すべてのメッセージを自動翻訳
- **自動言語検出**: 日本語と英語を自動判定
- **双方向翻訳**: 日本語→英語、英語→日本語
- **複数の入力方法**: 自動翻訳、コマンド、メッセージベース
- **エラーハンドリング**: 翻訳エラー時の適切な応答

## 例

### 自動翻訳モード
```
ユーザー: !translation
ボット: Auto-translation: ON

ユーザー: こんにちは、元気ですか？
ボット: >>> Hello, how are you?

ユーザー: Thank you very much
ボット: >>> どうもありがとうございます
```

### コマンド翻訳
```
ユーザー: !t おはようございます
ボット: >>> Good morning

ユーザー: !translate Good evening
ボット: >>> こんばんは
```

### メッセージベース翻訳
```
ユーザー: translate: ありがとう
ボット: >>> Thank you

ユーザー: 翻訳: How are you?
ボット: >>> お元気ですか？
```