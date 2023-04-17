import discord
from discord.ext import commands
import sqlite3
import random
from discord.ui import Button, View


class HighLow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["hl", "HL", "Hl", "HIGHLOW", "Highlow"])      
    @commands.guild_only()
    async def highlow(self, ctx:commands.Context, amount=None):
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

            number = random.randint(1,10)

            higher = Button(label="Higher", emoji="🔼")
            lower = Button(label="Lower", emoji="🔽")

            view = View(timeout=None)
            view.add_item(higher)
            view.add_item(lower)

            embed = discord.Embed(title="Higher or lower", color=discord.Color.blue())
            embed.add_field(name="", value="Is the number higher or lower than 5?", inline=False)
            embed.add_field(name="", value="Higher 🔼 **(6 - 10)**", inline=False)
            embed.add_field(name="", value="Lower 🔽 **(1 - 5)**", inline=False)

            await ctx.reply(embed=embed, view=view)

            async def high_call(interaction:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if ctx.author.id == interaction.user.id:
                    if number > 5:
                        embed=discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet + amount * 2:,}```", inline=False)

                        await interaction.response.edit_message(embed=embed, view=None)

                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, interaction.user.id))
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount* 2, interaction.user.id))

                        db.commit()
                        return

                    else:
                        embed=discord.Embed(title="You lost", color=discord.Color.red())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet - amount:,}```", inline=False)
                        await interaction.response.edit_message(embed=embed, view=None)
                        return

                else:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

            higher.callback = high_call

            async def low_call(interaction:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if ctx.author.id == interaction.user.id:
                    if number < 6:
                        embed=discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet + amount * 2:,}```", inline=False)

                        await interaction.response.edit_message(embed=embed, view=None)

                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, interaction.user.id))

                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount* 2, interaction.user.id))

                        db.commit()
                        return

                    else:
                        embed=discord.Embed(title="You lost", color=discord.Color.red())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet - amount:,}```", inline=False)

                        await interaction.response.edit_message(embed=embed, view=None)
                        return

                else:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

            lower.callback = low_call
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(HighLow(bot))
