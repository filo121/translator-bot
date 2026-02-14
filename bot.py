import discord
from discord.ext import commands
from googletrans import Translator
import os

# -----------------------------
# Config
# -----------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("ERROR: DISCORD_TOKEN not set!")
    exit(1)

TARGET_LANGUAGES = ["en", "fr", "es"]  # Add any language codes you want

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

# -----------------------------
# Helper function
# -----------------------------
def translate_text(text, target_lang):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error for '{target_lang}': {e}")
        return None

# -----------------------------
# Events
# -----------------------------
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

# -----------------------------
# Commands
# -----------------------------
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
        await ctx.send("Error: Translation failed.")

# -----------------------------
# Run bot
# -----------------------------
bot.run(TOKEN)


