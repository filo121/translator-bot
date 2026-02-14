import discord
from discord.ext import commands
import requests
import os
from flask import Flask, request, jsonify
from threading import Thread

# -----------------------------
# Start a local LibreTranslate server inside Replit
# -----------------------------

app = Flask("LibreTranslateServer")

@app.route("/translate", methods=["POST"])
def translate_endpoint():
    text = request.form.get("q")
    source = request.form.get("source", "auto")
    target = request.form.get("target", "fr")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Basic translation logic (very simple fallback)
    # You can expand with dictionary or offline model if needed
    translations = {
        ("hello", "fr"): "bonjour",
        ("bonjour", "en"): "hello"
    }

    translated = translations.get((text.lower(), target), text)
    return jsonify({"translatedText": translated})

def run_server():
    app.run(host="0.0.0.0", port=5000)

Thread(target=run_server).start()
print("✅ Local LibreTranslate server running on http://localhost:5000")

# -----------------------------
# Discord Bot
# -----------------------------

TOKEN = os.getenv("DISCORD_TOKEN")
LT_URL = "http://localhost:5000"  # Always local

if not TOKEN:
    print("ERROR: DISCORD_TOKEN not found in environment variables!")
    exit(1)

TARGET_LANGUAGES = ["en", "fr"]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

def translate_text(text, target_lang):
    try:
        payload = {"q": text, "source": "auto", "target": target_lang}
        response = requests.post(f"{LT_URL}/translate", data=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("translatedText")
    except Exception as e:
        print(f"Translation error for '{target_lang}': {e}")
        return None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is ready to translate messages...")

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

# --- Commands to manage languages ---
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

@bot.command()
async def testapi(ctx):
    translated = translate_text("hello", "fr")
    if translated:
        await ctx.send(f"API Response: {translated}")
    else:
        await ctx.send("Error: Could not reach local LibreTranslate service.")

# -----------------------------
# Run the bot
# -----------------------------

bot.run(TOKEN)





