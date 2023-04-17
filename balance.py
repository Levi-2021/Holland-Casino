import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your balance")

    async def bal(self, interaction:discord.Interaction, member:discord.Member=None):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
            if member is None:
                member = interaction.user

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {member.id} AND guild_id = {interaction.guild.id}")
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

            embed = discord.Embed(title="", color=discord.Color.blue(), timestamp=interaction.created_at)
            embed.set_author(icon_url=member.display_avatar.url, name=f"{member.name}'s Casino Chips ")
            embed.add_field(name="Pocket Chips", value=f"```yaml\n{wallet:,}```", inline=False)
            embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
            embed.add_field(name="Total Chips", value=f"```yaml\n{bank + wallet:,}```", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
            await interaction.response.send_message(embed=embed)

    @bal.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(balance(bot))