import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class with_dep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="deposit", description="Deposit your money")
    @app_commands.describe(amount="Amount you wish to deposit")

    async def deposit(self, interaction:discord.Interaction, amount:int ):
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
                bank = data[2]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                wallet = 0
                bank = 0

            if wallet < amount:
                return await interaction.response.send_message("You do not have that much money")
            elif amount < 1:

                return await interaction.response.send_message("Amount has to be 1 or more")
            else:
                cursor.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank + amount, interaction.user.id))
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))

                embed = discord.Embed(description=f"Successfully deposited **{amount}** pocket chips", color=discord.Color.blue(), timestamp=interaction.created_at)
                embed.set_author(icon_url=interaction.user.display_avatar.url, name=f"{interaction.user.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet - amount:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank + amount:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await interaction.response.send_message(embed=embed)

            db.commit()
            cursor.close()
            db.close()

    @deposit.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="withdraw", description="Withdraw your money")
    @app_commands.describe(amount="Amount you wish to withdraw")

    async def withdraw(self, interaction:discord.Interaction, amount:int):
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
                bank = data[2]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0

            if bank < amount:
                return await interaction.response.send_message("You do not have that much money")
            elif amount < 1:
                return await interaction.response.send_message("Amount has to be 1 or more")
            
            else:
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount, interaction.user.id))
                cursor.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank - amount, interaction.user.id))
            
                embed = discord.Embed(description=f"Successfully withdrawn **{amount}** bank chips", color=discord.Color.blue(), timestamp=interaction.created_at)
                embed.set_author(icon_url=interaction.user.display_avatar.url, name=f"{interaction.user.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet + amount:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank - amount:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await interaction.response.send_message(embed=embed)
                

            db.commit()
            cursor.close()
            db.close()
        
    @withdraw.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(with_dep(bot))