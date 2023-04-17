import discord
from discord.ext import commands
import sqlite3


class WithDep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["dep", "DEP", "Dep", "DEPOSIT", "Deposit"])      
    @commands.guild_only()
    async def deposit(self, ctx:commands.Context, amount=None):
        try:
                
            if amount == None:
                return await ctx.reply("No amount was given")

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                bank = data[2]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                wallet = 0
                bank = 0

            if amount == "all":
                if wallet == 0:
                    return await ctx.reply("You can't deposit 0")
                amount = wallet

            if amount == "half":
                if wallet == 0:
                    return await ctx.reply("You can't deposit 0")
                amount = wallet / 2

            amount = int(amount)
            if wallet < amount:
                return await ctx.reply("You do not have that much money")

            elif amount < 1:
                return await ctx.reply("Amount has to be 1 or more")
            
            else:

                cursor.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank + amount, ctx.author.id))
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))

                embed = discord.Embed(description=f"Successfully deposited **{amount}** pocket chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet - amount:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank + amount:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")

                await ctx.reply(embed=embed)

            db.commit()
            cursor.close()
            db.close()

        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
            
    
    @commands.command(aliases=["with", "WITH", "With", "WITHDRAW", "Withdraw"])      
    @commands.guild_only()
    async def withdraw(self, ctx:commands.Context, amount=None):
        try:
                
            if amount == None:
                return await ctx.reply("No amount was given")

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                bank = data[2]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                wallet = 0
                bank = 0

            if amount == "all":
                if bank == 0:
                    return await ctx.reply("You can't withdraw 0")
                amount = bank

            if amount == "half":
                if bank == 0:
                    return await ctx.reply("You can't withdraw 0")
                amount = bank / 2

            amount = int(amount)
            if bank < amount:
                return await ctx.reply("You do not have that much money")

            elif amount < 1:
                return await ctx.reply("Amount has to be 1 or more")
            
            else:
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
                cursor.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank - amount, ctx.author.id))
                
                embed = discord.Embed(description=f"Successfully withdrawn **{amount}** bank chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet + amount:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank - amount:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await ctx.reply(embed=embed)
                

            db.commit()
            cursor.close()
            db.close()

        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(WithDep(bot))
