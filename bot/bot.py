import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# Keep-alive server
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# Config
TARGET_LANGUAGES = ["en", "fr"]
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ERROR: DISCORD_TOKEN not found!")
    exit()

LIBRE_URL = "https://translate.mentality.rip/translate"

# Discord setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
        return response.json().get("translatedText")
    except Exception as e:
        print(f"Translation error ({target_lang}): {e}")
        return None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

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

@bot.command()
async def addlang(ctx, code):
    if code not in TARGET_LANGUAGES:
        TARGET_LANGUAGES.append(code)
        await ctx.send(f"✅ Added language {code}")

@bot.command()
async def removelang(ctx, code):
    if code in TARGET_LANGUAGES:
        TARGET_LANGUAGES.remove(code)
        await ctx.send(f"✅ Removed language {code}")

bot.run(TOKEN)


