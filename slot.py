import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random

class slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="slot", description="Slot your money")
    @app_commands.describe(amount="Amount you wish to bet")

    async def slot(self, interaction:discord.Interaction, amount:int):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
                
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
            data = cursor.fetchone()
            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                wallet = 0
                spend_on_gambling = 0
                won_with_gambling = 0

            if amount < 0:
                return await interaction.response.send_message("You can't bet less than 0")
            
            if wallet < amount:
                return await interaction.response.send_message("You don't have enough money")
            
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))
            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend_on_gambling + amount, interaction.user.id))
            db.commit()

            times_factors = random.randint(1, 5)
            earing = int(amount*times_factors)

            final = []
            for i in range(3):
                a = random.choice(["🍉", "💎", "💰"])
                final.append(a)

            if final[0] == final[1] or final[0] == final[2] or final[2] == final[0]:
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earing, interaction.user.id))
                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + earing, interaction.user.id))
                db.commit()

                embed = discord.Embed(title=f"Slot Machine", color=discord.Color.green())
                embed.add_field(name=f"You won {earing:,} casino chips", value=f"{final}")
                embed.add_field(name="----------------------------------", value=f"**Multiplier**\n X {times_factors}", inline=False)
                embed.add_field(name="----------------------------------", value=f"**New Balance**\n ```yaml\n{wallet + earing:,} pocket chips```", inline=False)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await interaction.response.send_message(embed=embed)

            else:

                embed = discord.Embed(title=f"Slot Machine", color=discord.Color.red())
                embed.add_field(name=f"You Lost {amount} casino chips", value=f"{final}")
                embed.add_field(name="----------------------------------", value=f"**New Balance**\n ```yaml\n{wallet - amount:,} pocket chips```", inline=False)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await interaction.response.send_message(embed=embed)

                cursor.close()
                db.close()
            
            
    @slot.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(slot(bot))