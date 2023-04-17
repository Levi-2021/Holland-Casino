import os
import discord
import asyncio
from discord.ext import commands, tasks
import random
import time
import sqlite3


token = "ODk2NTE4NzAyNTUwMzc2NDg5.G78uPg.yLO9g47ObyjUcAscjIyfXg5inlY8yO08njYFCQ" # test bot
token = "MTA4NjAxNzc1NjcxOTIyNjg5MA.GREor6.qSe_8EjHVsYb6RIU-XrwAtYhrHXBjjVvgzXIgc" # main bot

intents = discord.Intents.all()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='<@1086017756719226890> ', intents=intents)

bot.remove_command("help")

async def load():
    i = 0
    prefix = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            i = i + 1
            print(f"""
                    {filename}
                  """)
            if filename.endswith('prefix.py'):
                prefix = prefix + 1

    print(f"""
          TOTAL COGS CONNECTED {i}
          """)
    print(f"""
          PREFIX COGS CONNECTED {prefix}
          """)
    print(f"""
          NORMAL COGS CONNECTED {i - prefix}
          """)
    invest.start()


@tasks.loop(seconds=1)
async def invest():
    db = sqlite3.connect("invest.sqlite")
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM invest")
    data = cursor.fetchone()
    
    if data == None:
        cursor.execute("INSERT INTO invest(stock_prize, stamp) VALUES (?, ?)",
            (50000, int(time.time())))
        db.commit()
                    
        stamp = int(time.time())
        old_stock = 50000

    else:
        stamp = data[1]
        old_stock = data[0]

    if stamp + 5 < int(time.time()):
        if old_stock < 35000:
            add = random.randint(-100, 900)

        if old_stock > 65000:
            add = random.randint(-800, 200)
        else:
            add = random.randint(-400, 600)
            
        new_stock = old_stock + add

        cursor.execute(f"UPDATE invest SET stock_prize = {new_stock}")
        cursor.execute(f"UPDATE invest SET stamp = {int(time.time())}")
        db.commit()
        


async def main():
    async with bot:
        await load()
        await bot.start(token)
asyncio.run(main())
