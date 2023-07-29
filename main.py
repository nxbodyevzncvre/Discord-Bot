import discord
from discord.ext import commands
import youtube_dl
import os
import random
from simpledemotivators import Demotivator
import markovify
import time
import uuid
from discord import *
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents = intents)
client = Client()



@bot.command()
async def copy(ctx):
    with open("file.txt", "w", encoding='utf-8') as f:
        async for message in ctx.history(limit=2000):
            f.write(message.content + "\n")



global member


@bot.command(aliases = ["пидоры"])
async def members(ctx):
    for guild in bot.guilds:
        list = []
        for member in guild.members:
            list.append(member.name)

        str_mem = '\n'.join(list)
        await ctx.send(f"пидоры:\n{str_mem}")


@bot.command(aliases=["поменять_ник"])
async def nick(ctx, user: Member, nickname):
  await user.edit(nick=nickname)


@bot.command(aliases=["помогите"])
async def bothelp(ctx):
    await ctx.send("команды:\n!demotivate[фото, текст](демотиватор)\n![@юзер](кол-во сообщений юзера)\n!поменять_ник[пользователь, олд, нью](смена никнейма юзеру)")



@bot.command()
async def background_task():
    await client.wait_until_ready()
    channel = client.get_channel(888745962657423382)
    time = 5
    await asyncio.sleep(time)
    with open("text.txt", encoding='utf-8', mode='r') as f:
        text = f.read()

    text_model = markovify.NewlineText(text, state_size=1)

    for i in range(1):
        await channel.send(text_model.make_short_sentence(40))


@bot.command(aliases=['dem'])
async def demotivate(ctx):
    global snd, fst
    imageName = str(uuid.uuid4()) + '.png'

    await ctx.message.attachments[0].save(imageName)
    os.rename(imageName, "demotivator.png")
    with open("text.txt", encoding='utf-8', mode='r') as f:
        text = f.read()

    text_model = markovify.NewlineText(text, state_size=1)
    for i in range(1):
        fst = text_model.make_short_sentence(random.randint(1, 9656))
    for i in range(1):
        snd = text_model.make_short_sentence(random.randint(1, 9656))
    dem = Demotivator(str(fst), str(snd))

    time.sleep(0.5)
    dem.create('demotivator.png')
    with open('demresult.jpg', 'rb') as f:
        picture = File(f)
        await ctx.send(file=picture)
    os.remove('demotivator.png')
@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Лобби')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command(aliases = ["пинг", "п1нг", 'p1ng', "p1nк", "п1нк"])
async def ping(ctx):
    response = ["понг",
                "пошел нахрен"]
    await ctx.send(f"{random.choice(response)}")


@bot.command(aliases = ["вопрос", "test"])
async def _8ball(ctx, *, question):
    responses =["да",
                "коне   чно",
                "ахахаха, ты ебанутый? конечно да",
                "даааа",
                "обязательно",
                "заебал, конечно же да",
                "ну не знаю",
                "не уверен",
                'ахахахахаха',
                "хзз",
                "хз)",
                "неа",
                "нет ",
                "не, 0 шансов",
                "вряд ли",
                "NO"
                ]
    await ctx.send(f"Вопрос: {question}\nОтвет:{random.choice(responses)}")




@bot.command(aliases=["чистка", "почистить", "чистилка", "cl"])
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)


@bot.command(aliases=["уебашить_потихоньку", "сломать_пальчик"])
async def kick(ctx, member : discord.Member, *, reason = "долбоеб"):
    await member.kick(reason=reason)


@bot.command(aliases=["уебашить_хуесоса", "сломать_колени"])
async def ban(ctx, member : discord.Member, *, reason = "хуесос, выйди нахуй"):
    await member.ban(reason=reason)




bot.run('OTg1OTMxNjY1ODExNTk5NDIy.GbIOio.LAfQwOoPjjxCJgT-do1HZlbgK7GtvdPvdnNS-w')