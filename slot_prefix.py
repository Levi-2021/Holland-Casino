import discord
from discord.ext import commands
import sqlite3
import random


class Slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["SLOT", "Slot", "gamble", "GAMBLE", "Gamble"])      
    @commands.guild_only()
    async def slot(self, ctx:commands.Context, amount=None):
        try:
                
            if amount == None:
                return await ctx.reply("No amount was given")

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                wallet = 0
                spend_on_gambling = 0
                won_with_gambling = 0

            if amount == "all":
                amount = wallet

            if amount == "half":
                amount = wallet / 2

            amount = int(amount)
            if wallet < amount:
                return await ctx.reply("You do not have that much money")

            elif amount < 0:
                return await ctx.reply("Amount has to be 0 or more")

            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend_on_gambling + amount, ctx.author.id))
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
            db.commit()

            times_factors = random.randint(1, 5)
            earing = int(amount*times_factors)

            final = []
            for i in range(3):
                a = random.choice(["🍉", "💎", "💰"])
                final.append(a)

            if final[0] == final[1] or final[0] == final[2] or final[2] == final[0]:
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earing, ctx.author.id))
                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + earing, ctx.author.id))
                db.commit()

                embed = discord.Embed(title=f"Slot Machine", color=discord.Color.green())
                embed.add_field(name=f"You won {earing:,} casino chips", value=f"{final}")
                embed.add_field(name="----------------------------------", value=f"**Multiplier**\n X {times_factors}", inline=False)
                embed.add_field(name="----------------------------------", value=f"**New Balance**\n ```yaml\n{wallet + earing:,} pocket chips```", inline=False)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await ctx.reply(embed=embed)

            else:

                embed = discord.Embed(title=f"Slot Machine", color=discord.Color.red())
                embed.add_field(name=f"You Lost {earing:,} casino chips", value=f"{final}")
                embed.add_field(name="----------------------------------", value=f"**New Balance**\n ```yaml\n{wallet + earing:,} pocket chips```", inline=False)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await ctx.reply(embed=embed)

                cursor.close()
                db.close()
                
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Slot(bot))
