from typing import Literal
import discord
from discord import app_commands
from discord.ext import commands
import sqlite3


class leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="Display the top 10 user")
    @app_commands.describe(type="Specify type of leaderboard")
    @app_commands.describe(server="Specify server")

    async def leaderboard(self, inter: discord.Interaction, type: Literal['Bank Chips', 'Pocket Chips', 'Total Chips', 'Won With gambling', 'Spend On Gambling', 'Profit'], server: Literal['All Servers', 'This Server']):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
        else:
            
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            if server == 'This Server':
                if type == 'Bank Chips':
                    cursor.execute(
                        f"SELECT user_id, bank FROM economy where guild_id = {inter.guild.id} ORDER BY bank DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Pocket Chips':
                    cursor.execute(
                        f"SELECT user_id, wallet FROM economy where guild_id = {inter.guild.id} ORDER BY wallet DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Total Chips':
                    cursor.execute(
                        f"SELECT user_id, net FROM economy where guild_id = {inter.guild.id} ORDER BY net DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Won With Gambling':
                    cursor.execute(
                        f"SELECT user_id, won_with_gambling FROM economy where guild_id = {inter.guild.id} ORDER BY won_with_gambling LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Spend On Gambling':
                    cursor.execute(
                        f"SELECT user_id, spend_on_gambling FROM economy where guild_id = {inter.guild.id} ORDER BY spend_on_gambling LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Profit':
                    cursor.execute(
                        f"SELECT user_id, profit FROM economy where guild_id = {inter.guild.id} ORDER BY Profit DESC LIMIT 10")
                    data = cursor.fetchall()

            if server == 'All Servers':
                if type == 'Bank Chips':
                    cursor.execute(
                        f"SELECT user_id, bank FROM economy ORDER BY bank DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Pocket Chips':
                    cursor.execute(
                        f"SELECT user_id, wallet FROM economy ORDER BY wallet DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Total Chips':
                    cursor.execute(
                        f"SELECT user_id, net FROM economy ORDER BY net DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Won With Gambling':
                    cursor.execute(
                        f"SELECT user_id, won_with_gambling FROM economy ORDER BY won_with_gambling DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Spend On Gambling':
                    cursor.execute(
                        f"SELECT user_id, spend_on_gambling FROM economy ORDER BY spend_on_gambling DESC LIMIT 10")
                    data = cursor.fetchall()

                if type == 'Profit':
                    cursor.execute(
                        f"SELECT user_id, profit FROM economy ORDER BY Profit DESC LIMIT 10")
                    data = cursor.fetchall()

            if data:
                em = discord.Embed(title=f"{type} Leaderboard | {server}", description="Top 10 users",  color=discord.Color.blue())
                count = 0
                for table in data:
                    count += 1
                    em.add_field(name=f"", value=f"{count}. <@{table[0]}>\n{type} - **{table[1]:,}**", inline=False)
                return await inter.response.send_message(embed=em)
            else:
                return await inter.response.send_message("There are no users stored in the leaderboard")

    @leaderboard.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(leaderboard(bot))
