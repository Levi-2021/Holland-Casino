import discord
from discord.ext import commands
import sqlite3


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal", "BAL", "Bal", "BALANCE", "Balance"])      
    @commands.guild_only()
    async def balance(self, ctx:commands.Context, member:discord.Member=None):
        try:
            if member is None:
                member = ctx.author

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {member.id} AND guild_id={ctx.guild.id}")
            data = cursor.fetchone()
            try:
                wallet = data[1]
                bank = data[2]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0
                

            embed = discord.Embed(title="", color=discord.Color.blue(), timestamp= ctx.message.created_at)
            embed.set_author(icon_url=member.display_avatar.url, name=f"{member.name}'s Casino Chips ")
            embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet:,}```", inline=False)
            embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
            embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
            await ctx.reply(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Balance(bot))
