# Discord翻訳ボット - Google Gemini API使用
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai

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

# 言語リスト
languages = {
    'ja': 'Japanese',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh': 'Chinese',
    'ko': 'Korean',
    'it': 'Italian',
    'ru': 'Russian',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'pt': 'Portuguese'
}

# 現在の言語設定（from-to形式）
current_lang_from = 'ja'
current_lang_to = 'en'


async def translate_text(text):
    """Gemini APIを使用してテキストを翻訳"""
    try:
        # 双方向翻訳プロンプトを作成
        from_lang = languages[current_lang_from]
        to_lang = languages[current_lang_to]
        prompt = f"You are a bidirectional translator between {from_lang} and {to_lang}. When you receive {from_lang} text, translate it to {to_lang}. When you receive {to_lang} text, translate it to {from_lang}. Always respond with only the translated text, no explanations. Input: {text}"
        
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

@bot.command(name='translate', aliases=['t'])
async def translate(ctx, *, text):
    """手動翻訳コマンド（!translate または !t）"""
    if not text:
        await ctx.send("Please provide text to translate.")
        return
    
    # テキストを翻訳して結果を送信
    translation = await translate_text(text)
    await ctx.send(f"> {translation}")

@bot.command(name='translation')
async def toggle_translation(ctx):
    """自動翻訳モードのON/OFF切り替え"""
    global auto_translate_enabled
    auto_translate_enabled = not auto_translate_enabled
    status = "ON" if auto_translate_enabled else "OFF"
    await ctx.send(f"> Auto-translation: **{status}**")

@bot.command(name='lang')
async def set_language(ctx, lang_pair=None):
    """言語ペアの設定 (!lang ja-en, !lang ja-cn, !lang en-ja など)"""
    global current_lang_from, current_lang_to
    
    if lang_pair is None:
        # 現在の設定を表示
        from_lang = languages[current_lang_from]
        to_lang = languages[current_lang_to]
        await ctx.send(f'''
        > Current Language: **{from_lang} ↔ {to_lang}**
        **Availability:**
        `ja`: Japanese
        `en`: English
        `es`: Spanish
        `fr`: French
        `de`: German
        `zh`: Chinese
        `ko`: Korean
        `it`: Italian
        `ru`: Russian
        `ar`: Arabic
        `hi`: Hindi
        `pt`: Portuguese
        ''')
        return
    
    if '-' not in lang_pair:
        await ctx.send("> Invalid format: `!lang ja-en`")
        return
        
    from_lang, to_lang = lang_pair.split('-')
    
    if from_lang in languages and to_lang in languages:
        current_lang_from = from_lang
        current_lang_to = to_lang
        from_name = languages[from_lang]
        to_name = languages[to_lang]
        await ctx.send(f"> Language settings changed: {from_name} ↔ {to_name}")
    else:
        await ctx.send('''
        > Invalid language code.
        **Availability:**
        `ja`: Japanese
        `en`: English
        `es`: Spanish
        `fr`: French
        `de`: German
        `zh`: Chinese
        `ko`: Korean
        `it`: Italian
        `ru`: Russian
        `ar`: Arabic
        `hi`: Hindi
        `pt`: Portuguese
                       ''')

@bot.event
async def on_message(message):
    """メッセージ受信時の処理"""
    # ボット自身のメッセージは無視
    if message.author == bot.user:
        return
    
    # 自動翻訳モードがONかつコマンド以外のメッセージの場合
    if auto_translate_enabled and not message.content.startswith('!'):
        translation = await translate_text(message.content)
        await message.channel.send(f"> {translation}")
    
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