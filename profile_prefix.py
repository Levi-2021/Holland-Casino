import discord
from discord.ext import commands
import sqlite3


class ProfilePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["PROFILE", "Profile"])
    async def profile(self, ctx:commands.Context, member:discord.Member=None):
        try:
            if ctx.guild == None:
                    embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                    return await ctx.send(embed=embed)
            else:
                    
                if member == None:
                    member = ctx.author

                db1 = sqlite3.connect("invest.sqlite")
                cursor1 = db1.cursor()

                cursor1.execute(
                    f"SELECT * FROM stock WHERE user_id = {member.id}")
                data = cursor1.fetchone()
                
                if data is None:
                    stock_amount = 0
                    
                else:
                    stock_amount = data[1]
                
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()

                cursor.execute(
                    f"SELECT * FROM economy WHERE user_id = {member.id} AND guild_id={ctx.guild.id}")
                data = cursor.fetchone()

                try:
                    wallet = data[1]
                    bank = data[2]
                    spend = data[3]
                    won = data[4]
                    profit = data[7]

                except:
                    cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (member.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                    db.commit()
                    wallet = 0
                    bank = 0
                    spend = 0
                    won = 0
                    profit = 0

                net = bank + wallet

                user_data = {  
                        "name": f"{member.name}#{member.discriminator}",  
                        "display_name": f"```c\n{member.display_name}```",
                        "spend":f"```c\n{spend:,}```",
                        "won": f"```c\n{won:,}```",
                        "profits": f"```c\n{profit:,}```",
                        "net": f"```c\n{net:,}```",
                        "stock": f"```c\n{stock_amount:,}```"
                    }

                
                embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s profile", color=discord.Color.blue())
                embed.add_field(name="Profits:", value=f"{user_data['profits']}", inline=False)
                embed.add_field(name="Amount Won:", value=f"{user_data['won']}", inline=False)
                embed.add_field(name="Amount Spend:", value=f"{user_data['spend']}", inline=False)
                embed.add_field(name="Total Casino Chips:", value=f"{user_data['net']}", inline=False)
                embed.add_field(name="Holland Casino Stock(s):", value=f"{user_data['stock']}", inline=False)
                
                await ctx.send(embed=embed)
                
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ProfilePrefix(bot))
