import discord
from discord.ext import commands
import time
import sqlite3


class VotePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["VOTE", "Vote"])
    async def vote(self, ctx:commands.Context):
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM streak WHERE user_id = {ctx.author.id}")
        data = cursor.fetchone()
        
        try:
            streak = data[1]
            stamp = data[2]
            
        except:
            streak = 0
            stamp = 0
            cursor.execute("INSERT INTO streak(user_id, vote_streak, stamp) VALUES(?, ?, ?)",
                            (ctx.author.id, 0, 0))
            
        if streak == 0:
            embed = discord.Embed(title="", description=f"**Vote for Holland Casino at [top.gg](https://top.gg/bot/1086017756719226890)** \n\nYou have a vote streak of **0** which will generate you **{50000:,}** casino chips and increase your streak to **1**", color=discord.Color.green(), timestamp=ctx.message.created_at)
        else:
            if stamp + 86400 > int(time.time()):
                embed = discord.Embed(title="", description=f"You can vote again <t:{stamp + 43200}:R> which which will generate you **{50000 * streak:,}** casino chips and increase your streak to **{streak + 1}**", color=discord.Color.green(), timestamp=ctx.message.created_at)
            else:
                embed = discord.Embed(title="", description=f"**Vote for Holland Casino at [top.gg](https://top.gg/bot/1086017756719226890)** \n\nYou have a vote streak of **{streak}** which will generate you {50000 * streak:,} casino chips", color=discord.Color.green(), timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VotePrefix(bot))
