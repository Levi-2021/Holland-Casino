import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="give", description="Give someone your money (20% tax)")
    @app_commands.describe(member="User you want to give the money")
    @app_commands.describe(amount="Amount you wish to give the user")
    async def give(self, interaction:discord.Interaction, amount:int,  member:discord.Member):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
                
            if member.id == 1086017756719226890:
                embed = discord.Embed(title="", description="Thanks for the money but i dont need it ^~^", color=discord.Color.blue())
                return await interaction.response.send_message(embed=embed)
            
            if member.id == interaction.user.id:
                return await interaction.response.send_message("You can't give yourself money")
            
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id={interaction.guild.id}")
            data = cursor.fetchone()

            try:
                userwallet = data[1]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                userwallet = 0

            if userwallet < amount:
                await interaction.response.send_message("You don't have enough money in your wallet")
                return
            

            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {member.id}")
            data = cursor.fetchone()

            try:
                memberwallet = data[1]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (member.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                memberwallet = 0
            
            round(amount*(80/100))
            
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                        (memberwallet + amount, member.id))
            db.commit()
            
            embed = discord.Embed(description=f"{interaction.user.mention} gave you **{round(amount)}** Casino Chips", color=discord.Color.blue())
            embed.set_footer(icon_url=interaction.user.display_avatar.url, text="20% tax included")
            
            await interaction.response.send_message(member.mention, embed=embed)
            return

    @give.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(give(bot))
