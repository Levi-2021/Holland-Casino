import discord
from discord.ext import commands
from discord import app_commands
import sqlite3


class StoredData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stored-data", description="Display all stored data the bot has from you (via DM's)")
    async def stored(self, inter:discord.Interaction):
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM economy WHERE user_id = {inter.user.id}")
        data = cursor.fetchall()
        
        await inter.response.send_message(f"I've sent you a DM {inter.user.mention}")
        
        embed = discord.Embed(title="", description=f"All economy data stored for {inter.user.mention} ({inter.user.id})", color=discord.Color.blue(), timestamp=inter.created_at)
        embed.set_footer(text=f"ALL ECONOMY DATA STORED FOR {inter.user}", icon_url=inter.user.display_avatar.url)
        
        for table in data:
            embed.add_field(name="", value=f"**Guild ID:** \n{table[5]} \n**User ID:** \n{table[0]}\n**Pocket Chips:** \n{table[1]:,} \n**Bank Chips:** \n{table[2]:,} \n**Total Chips:** \n{table[6]:,} \n**Total spend on gambling:** \n{table[3]:,} \n**Total won with gambling:** \n{table[4]:,} \n**Profits** \n{table[7]:,}", inline=False)
            embed.add_field(name="-------------------", value="", inline=False)
            
        await inter.user.send(embed=embed)

        cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {inter.user.id}")
        data = cursor.fetchall()
        
        embed = discord.Embed(title="", description=f"All timestamp data stored for {inter.user.mention} ({inter.user.id})", color=discord.Color.blue(), timestamp=inter.created_at)
        embed.set_footer(text=f"ALL TIMESTAMP DATA STORED FOR {inter.user}", icon_url=inter.user.display_avatar.url)
        
        for table in data:
            embed.add_field(name="", value=f"**User ID:** \n{table[0]} \n**Hourly Timestamp: **\n{table[2]} \n**Daily Timestamp: **\n{table[1]}", inline=False)
            embed.add_field(name="-------------------", value="", inline=False)
            
        await inter.user.send(embed=embed)
    
        db1 = sqlite3.connect("invest.sqlite")
        cursor1 = db1.cursor()
        
        cursor1.execute(f"SELECT * FROM stock WHERE user_id = {inter.user.id}")
        data = cursor1.fetchall()
        
        embed = discord.Embed(title="", description=f"All stock data stored for {inter.user.mention} ({inter.user.id})", color=discord.Color.blue(), timestamp=inter.created_at)
        embed.set_footer(text=f"ALL STOCK DATA STORED FOR {inter.user}", icon_url=inter.user.display_avatar.url)
        
        for table in data:
            embed.add_field(name="", value=f"**User ID:** \n{table[0]} \n**Stock Amount: **\n{table[1]}", inline=False)
            embed.add_field(name="-------------------", value="", inline=False)
            
        await inter.user.send(embed=embed)
        
    
    @stored.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(StoredData(bot))
