import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from discord.ui import Button, View
import random

class highlow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="high-low", description="Guess if the number is higher or lower than 5")
    @app_commands.describe(amount="Amount you wish to bet")
    async def highlow(self, inter:discord.Interaction, amount:int):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
        else:
                
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {inter.user.id} AND guild_id = {inter.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (inter.user.id, 0, 0, 0, 0, inter.guild.id, 0, 0))
                db.commit()
                won_with_gambling = 0
                spend_on_gambling = 0

            if wallet < amount:
                await inter.response.send_message("You don't have that much money in your wallet")
                return
            
            if amount < 0:
                return

            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend_on_gambling + amount, inter.user.id))

            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, inter.user.id))
            db.commit()
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

            await inter.response.send_message(embed=embed, view=view)

            async def high_call(interaction:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if inter.user.id == interaction.user.id:
                    if number > 5:
                        embed=discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet + amount * 2:,}```", inline=False)

                        await interaction.response.edit_message(embed=embed, view=None)

                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, inter.user.id))
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount* 2, inter.user.id))

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
                    await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)

            higher.callback = high_call

            async def low_call(interaction:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if inter.user.id == interaction.user.id:
                    if number < 6:
                        embed=discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="Number:", value=f"```c\n{number}```", inline=False)
                        embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                        embed.add_field(name="New Balance:", value=f"```c\n{wallet + amount * 2:,}```", inline=False)

                        await interaction.response.edit_message(embed=embed, view=None)

                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, inter.user.id))

                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount* 2, inter.user.id))

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
                    await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)

            lower.callback = low_call

    @highlow.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(highlow(bot))
