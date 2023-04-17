import discord
from discord.ext import commands, tasks
import sqlite3
from discord import app_commands
import time
            
@tasks.loop(seconds=60)
async def update():
    db = sqlite3.connect("economy.sqlite")
    cursor = db.cursor()

    cursor.execute(
            f"SELECT * FROM streak")
    data = cursor.fetchall()
            
    for table in data:
        if table[2] + 86400 < int(time.time()):
            cursor.execute("UPDATE streak SET vote_streak = ? WHERE user_id = ?", (0, table[0]))
            db.commit()

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        update.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1097532170538594455:
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {message.content[0:30]}")
            data = cursor.fetchone()

            cursor.execute(f"SELECT * FROM streak WHERE user_id = {message.content[0:30]}")
            data2 = cursor.fetchone()

            try:
                wallet = data[1]

            except:
                return
            
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + 50000 * int(message.content[33:50]), message.content[0:30]))
            
            try:
                streak = data2[1]
                cursor.execute("UPDATE streak SET vote_streak = ? WHERE user_id = ?", (int(message.content[33:50]), message.content[0:30]))
                cursor.execute("UPDATE streak SET stamp = ? WHERE user_id = ?", (int(time.time()), message.content[0:30]))
                
            except:
                cursor.execute("INSERT INTO streak(user_id, vote_streak, stamp) VALUES(?, ?, ?)",
                            (message.content[0:30], 1, int(time.time())))
            db.commit()
            
    
    @app_commands.command(name="vote", description="Vote for the bot on top.gg")
    async def vote(self, inter:discord.Interaction):
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM streak WHERE user_id = {inter.user.id}")
        data = cursor.fetchone()
        
        try:
            streak = data[1]
            stamp = data[2]
            
        except:
            streak = 0
            stamp = 0
            cursor.execute("INSERT INTO streak(user_id, vote_streak, stamp) VALUES(?, ?, ?)",
                            (inter.user.id, 0, 0))
            
        if streak == 0:
            embed = discord.Embed(title="", description=f"**Vote for Holland Casino at [top.gg](https://top.gg/bot/1086017756719226890)** \n\nYou have a vote streak of **0** which will generate you **{50000:,}** casino chips and increase your streak to **1**", color=discord.Color.green(), timestamp=inter.created_at)
        else:
            if stamp + 86400 > int(time.time()):
                embed = discord.Embed(title="", description=f"You can vote again <t:{stamp + 43200}:R> which which will generate you **{50000 * streak:,}** casino chips and increase your streak to **{streak + 1}**", color=discord.Color.green(), timestamp=inter.created_at)
            else:
                embed = discord.Embed(title="", description=f"**Vote for Holland Casino at [top.gg](https://top.gg/bot/1086017756719226890)** \n\nYou have a vote streak of **{streak}** which will generate you {50000 * streak:,} casino chips", color=discord.Color.green(), timestamp=inter.created_at)
            
        await inter.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(Vote(bot))
    
