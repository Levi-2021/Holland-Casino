from typing import Literal
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
import time
from asyncio import sleep

class horse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="horse-racing", description="Bet on a horse race")
    @app_commands.describe(horse="Horse you want to bet on")
    @app_commands.describe(amount="Amount you wish to bet")
    async def horse(self, inter:discord.Interaction, amount:int, horse: Literal[1, 2, 3, 4, 5]):
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

            winning_horse = random.randint(1,7)
            wait_time = int(time.time() + 5)

            embed = discord.Embed(title="The horses are racing!", description=f"_Winner will be known in <t:{wait_time}:R> _", color=discord.Color.blue())
            embed.set_image(url="https://www.sportsengine.com/sites/default/files/styles/webp_1024_w/public/images/shutterstock_96722374.jpg.webp?itok=3W1m7r7p")
            await inter.response.send_message(embed=embed)

            await sleep(5)

            if winning_horse == horse:
                embed = discord.Embed(title="You won!", color=discord.Color.green())
                embed.add_field(name="Horse Betted On:", value=f"```c\nHorse {horse}```", inline=False)
                embed.add_field(name="Winning Horse:", value=f"```c\nHorse {winning_horse}```", inline=False)
                embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                embed.add_field(name="New Balance:", value=f"```c\n{wallet + amount * 6:,}```", inline=False)

                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 6 , inter.user.id))
                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 6} WHERE user_id = {inter.user.id}")
                db.commit()

                return await inter.edit_original_response(embed=embed)
            
            else:
                embed = discord.Embed(title="You lost", color=discord.Color.red())
                embed.add_field(name="Horse Betted On:", value=f"```c\nHorse {horse}```", inline=False)
                embed.add_field(name="Winning Horse:", value=f"```c\nHorse {winning_horse}```", inline=False)
                embed.add_field(name="Bet:", value=f"```c\n{amount:,}```", inline=False)
                embed.add_field(name="New Balance:", value=f"```c\n{wallet - amount:,}```", inline=False)

                return await inter.edit_original_response(embed=embed)

    @horse.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(horse(bot))