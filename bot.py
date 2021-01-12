# bot.py
import aiocron
import csv
import datetime
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

advent_calendar = {}
trivia = {}

with open('themes.csv') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        advent_calendar[line[0]] = line[1]

files_to_read = ['webaccessibility.csv', 'photography.csv']
for file_to_read in files_to_read:
    with open(file_to_read) as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            trivia[line[0]] = line[1]

channel_ids = []
trivia_channel_ids = []


@aiocron.crontab('15 5 * * *')
async def cronjob1():
    today = datetime.date.today().strftime('%Y-%m-%d')
    theme = advent_calendar[today]
    for channel_id in channel_ids:
        await client.get_channel(channel_id).send(f"Dzisiejszy temat to: {theme}")


@aiocron.crontab('0 7 * * *')
async def cronjob2():
    today = datetime.date.today().strftime('%Y-%m-%d')
    trivia_of_the_day = trivia[today]
    for channel_id in trivia_channel_ids:
        await client.get_channel(channel_id).send(trivia_of_the_day)


@aiocron.crontab('45 10 * * tue,thu')
async def cronjob3():
    today = datetime.date.today().strftime('%Y-%m-%d')
    for channel_id in channel_ids:
        await client.get_channel(channel_id).send("Za kwadrans kawka na głosowym! ☕")


@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord server {guild}!')
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                if 'music' in channel.name:
                    channel_ids.append(channel.id)
                if 'ciekawostka-dnia' in channel.name:
                    trivia_channel_ids.append(channel.id)
                if 'wydarzenia' in channel.name:
                    await cronjob3()



client.run(TOKEN)
