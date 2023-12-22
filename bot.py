from discord.ext import commands
from django.core.files.storage import default_storage
import discord
import os

from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import openai
bot = commands.Bot(command_prefix="", intents = discord.Intents.all())

openai.api_key = <key>
TOKEN = <bot_token>
CHANNEL_ID = <discord_channel_id>
OPENAI_TOKEN = <openai_token>

def get_emoji_unicode(input_sentence):
    # Construct the prompt
    prompt = f"Output the unicode including the U+ for only one emoji, excluding the hotdog emoji, that represents this sentence: {input_sentence}"

    # Make the API request
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the appropriate GPT-3 engine
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(response)
    # Extract Unicode from the response
    generated_text = response.choices[0].message.content
    emoji_unicode = extract_unicode_from_text(generated_text)

    return emoji_unicode

def extract_unicode_from_text(text):
    # Implement logic to extract Unicode from the generated text
    # This will depend on the structure of the model's output

    # For illustration purposes, let's assume the Unicode is enclosed in square brackets
    start_index = text.find("U+")
    if start_index == -1:
        return None
    return text[start_index + 2: start_index + 7]

@bot.event
async def on_ready():
    print("Hello world!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello!")

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
      return

    URL = 'https://emojik.vercel.app/s/1f32d_'
    print("received message")
    print(ctx.content)
    await ctx.channel.send("helloooo!")
    if 'hotdog' in ctx.content:
      print("detected hotdog keyword!!!")
      input_sentence = ctx.content
      emoji_unicode = get_emoji_unicode(input_sentence)
      URL += emoji_unicode.lower()
      URL += '?size=512'

      response = requests.get(URL)
      img = Image.open(BytesIO(response.content))
      file_name = "out.png"
      directory_path = <path of output file>
      file_path = os.path.join(directory_path, file_name)
      img.save(file_path)
      await ctx.channel.send(file=discord.File(file_path))

bot.run(TOKEN)
