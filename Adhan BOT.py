import discord
from discord.ext import commands
import requests
from datetime import datetime
import asyncio 


TOKEN = "MTQ3Njk1MDY1MzM5Mjc4NTU0MQ.GCTAp2.TWF1JZaGNbJlhexN4DZyIt9GTO771SMBWUBeT0"
VILLE = "Paris"
PAYS = "France"
ID_VOCAL = 1421926314159640597 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def avoir_les_prieres():
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity?city={VILLE}&country={PAYS}&method=2"
        reponse = requests.get(url)
        return reponse.json()["data"]["timings"]
    except:
        return None

@bot.event
async def on_ready():
    print(f"Le bot {bot.user} est en ligne !")
    bot.loop.create_task(boucle_priere())

async def boucle_priere():
    await bot.wait_until_ready()
    while not bot.is_closed():
        maintenant = datetime.now().strftime("%H:%M")
        horaires = avoir_les_prieres()
        if horaires:
            for p in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                if maintenant == horaires[p]:
                    channel = bot.get_channel(ID_VOCAL)
                    if channel:
                        await lancer_audio(channel)
                        await asyncio.sleep(61) 
        await asyncio.sleep(30)

async def lancer_audio(channel):
    try:

        for vc in bot.voice_clients:
            await vc.disconnect(force=True)
        

        voix = await channel.connect(timeout=20.0, reconnect=True)
        voix.play(discord.FFmpegPCMAudio("c:\\Users\\amine\\OneDrive\\Bureau\\Adhan\\adhan.mp3", executable="c:\\Users\\amine\\OneDrive\\Bureau\\Adhan\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"))
        while voix.is_playing():
            await asyncio.sleep(1)
        await voix.disconnect()
    except Exception as e:
        print(f"Erreur audio : {e}")

@bot.command()
async def test(ctx):
    print("Commande !test reçue")
    channel = bot.get_channel(ID_VOCAL)
    if channel:
        await ctx.send("⏳ Tentative de connexion...")
        await lancer_audio(channel)
        await ctx.send("✅ Test terminé")
    else:
        await ctx.send("❌ ID Vocal incorrect")

bot.run(TOKEN)