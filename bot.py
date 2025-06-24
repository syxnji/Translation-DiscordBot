# Discord翻訳ボット - Google Gemini API使用
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# 環境変数の読み込み
load_dotenv()

# Discord botの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を読み取る権限

bot = commands.Bot(command_prefix='!', intents=intents)

# Gemini APIの設定
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# 自動翻訳モードの状態管理
auto_translate_enabled = False

def detect_language(text):
    """テキストの言語を自動判定（日本語 or 英語）"""
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]')
    return 'japanese' if japanese_pattern.search(text) else 'english'

async def translate_text(text):
    """Gemini APIを使用してテキストを翻訳"""
    try:
        # 言語を自動判定
        language = detect_language(text)
        
        # 判定結果に基づいてプロンプトを作成
        if language == 'japanese':
            prompt = f"Translate this Japanese text to English and respond with only the English translation: {text}"
        else:
            prompt = f"Translate this English text to Japanese and respond with only the Japanese translation: {text}"
        
        # Gemini APIで翻訳実行
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# ===============================
# イベントハンドラー
# ===============================

@bot.event
async def on_ready():
    """ボット起動時の処理"""
    print(f'{bot.user} has connected to Discord!')

# ===============================
# コマンド定義
# ===============================

@bot.command(name='hello')
async def hello(ctx):
    """挨拶コマンド"""
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command(name='translate', aliases=['t'])
async def translate(ctx, *, text):
    """手動翻訳コマンド（!translate または !t）"""
    if not text:
        await ctx.send("Please provide text to translate.")
        return
    
    # テキストを翻訳して結果を送信
    translation = await translate_text(text)
    await ctx.send(f">>> {translation}")

@bot.command(name='translation')
async def toggle_translation(ctx):
    """自動翻訳モードのON/OFF切り替え"""
    global auto_translate_enabled
    auto_translate_enabled = not auto_translate_enabled
    status = "ON" if auto_translate_enabled else "OFF"
    await ctx.send(f"Auto-translation: {status}")

@bot.event
async def on_message(message):
    """メッセージ受信時の処理"""
    # ボット自身のメッセージは無視
    if message.author == bot.user:
        return
    
    # 自動翻訳モードがONかつコマンド以外のメッセージの場合
    if auto_translate_enabled and not message.content.startswith('!'):
        translation = await translate_text(message.content)
        await message.channel.send(f">>> {translation}")
    # メッセージベース翻訳（translate: または 翻訳: で始まる場合）
    elif message.content.startswith('translate:') or message.content.startswith('翻訳:'):
        text_to_translate = message.content.split(':', 1)[1].strip()
        if text_to_translate:
            translation = await translate_text(text_to_translate)
            await message.channel.send(f">>> {translation}")
    
    # コマンドの処理を実行
    await bot.process_commands(message)

# ===============================
# メイン実行部分
# ===============================

if __name__ == '__main__':
    # 環境変数の取得
    token = os.getenv('DISCORD_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    # 必要な環境変数のチェック
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables")
        exit(1)
    if not gemini_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        exit(1)
    
    # ボットを起動
    bot.run(token)