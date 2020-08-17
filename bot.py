import bisect
import csv

import discord
from discord.ext import commands

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

with open('token.txt') as token_file:
    token = token_file.read()

with open('emoji.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    emojis = [[float(row[0]), row[1]] for row in reader]

client = commands.Bot(command_prefix = '.')

@client.event
async def on_command_error(ctx, error):
    print(error)

@client.command()
async def sentiment(ctx):
    message = ctx.message.content[len('.sentiment')+1:]
    result = analyzer.polarity_scores(message)['compound']
    emoji = emojis[bisect.bisect_left(emojis, [result, ''])][1]

    print(message)
    print(result)

    embed = discord.Embed(
        title='Sentiment Analysis',
        description=f'I rate the sentiment of this message at a {result} (-1 to +1) {emoji}',
        url='https://github.com/bfazzani/sentiment-bot',
        color=discord.Color.dark_blue(),
    )
    embed.set_footer(
        text='I am using VADER sentiment'
    )

    await ctx.send(embed=embed)


client.run(token)