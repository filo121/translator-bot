import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# --- Keep-alive server for Railway ---
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# --- Config ---
TARGET_LANGUAGES = ["en", "fr"]  # default translation languages
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable not found!")
    exit(1)

# Public LibreTranslate API
LIBRE_URL = "https://libretranslate.com/translate"

# --- Discord Intents ---
intents = discord.Intents.default()
intents.message_content = True  # MUST be True to read messages
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Helper function ---
def translate_text(text, target_lang):
    try:
        payload = {
            "q": text,
            "source": "auto",
            "target": target_lang,
            "format": "text"
        }
        response = requests.post(LIBRE_URL, data=payload, timeout=10)
        response.raise_for_status()
        translated = response.json().get("translatedText")
        return translated
    except Exception as e:
        print(f"Translation error for '{target_lang}': {e}")
        return None

# --- Discord events ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is ready to translate messages...")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots

    translations = []

    for lang in TARGET_LANGUAGES:
        translated = translate_text(message.content, lang)
        if translated and translated.lower() != message.content.lower():
            translations.append(f"🌐 ({lang}) {translated}")

    if translations:
        embed = discord.Embed(
            title="Translations",
            description="\n".join(translations),
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# --- Commands to add/remove languages dynamically ---
@bot.command()
async def addlang(ctx, code):
    if code not in TARGET_LANGUAGES:
        TARGET_LANGUAGES.append(code)
        await ctx.send(f"✅ Added language `{code}`")
    else:
        await ctx.send(f"⚠ Language `{code}` already exists.")

@bot.command()
async def removelang(ctx, code):
    if code in TARGET_LANGUAGES:
        TARGET_LANGUAGES.remove(code)
        await ctx.send(f"✅ Removed language `{code}`")
    else:
        await ctx.send(f"⚠ Language `{code}` not found.")

# --- TEMPORARY: Test translation API ---
@bot.command()
async def testapi(ctx):
    """Test translation API directly from Discord"""
    try:
        r = requests.post(
            LIBRE_URL,
            data={
                "q": "hello",
                "source": "auto",
                "target": "fr",
                "format": "text"
            },
            timeout=10
        )
        await ctx.send(f"API Response: {r.json()}")
    except Exception as e:
        await ctx.send(f"Error calling API: {e}")

# --- Run bot ---
bot.run(TOKEN)


