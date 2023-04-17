import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import random
import time


class collecting_money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily-chips", description="Collect daily casino chips")
    async def daily(self, interaction:discord.Interaction):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
            earning = random.randint(1500, 2000)
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()
            
            cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {interaction.user.id}")
            data = cursor.fetchone()
            try:
                daily_stamp = data[1]
                stamp = int(time.time()) 
                cursor.execute("UPDATE timestamps SET daily_stamp = ? WHERE user_id = ?", (stamp + 86400, interaction.user.id))
                
            except:
                stamp = int(time.time()) 
                cursor.execute("INSERT INTO timestamps(user_id, daily_stamp, hourly_stamp) VALUES(?, ?, ?)",
                                (interaction.user.id, stamp + 86400, 0))
                db.commit()
                daily_stamp = 0
                
            cursor.execute(f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
            data = cursor.fetchone()
            
            try:
                wallet = data[1]
                bank = data[2]
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, interaction.user.id))
                
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (interaction.user.id, earning, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0
                
            if daily_stamp < int(time.time()):

                earned = wallet + earning
                embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=interaction.created_at)
                embed.set_author(icon_url=interaction.user.display_avatar.url, name=f"{interaction.user.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await interaction.response.send_message(embed=embed)

                db.commit()
                cursor.close()
                db.close()
                return
            
            else:
                
                embed = discord.Embed(title="Not so fast!", color=discord.Color.red(), timestamp=interaction.created_at)
                embed.add_field(name=f"", value=f"The casino is out of chips for now\n\nThey will return <t:{daily_stamp}:R>")
                await interaction.response.send_message(embed=embed)
                return
        
    @daily.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


    @app_commands.command(name="hourly-chips", description="Collect hourly casino chips")
    async def hourly(self, interaction:discord.Interaction):
        earning = random.randint(500, 1000)
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {interaction.user.id}")
        data = cursor.fetchone()
        
        try:
            hourly_stamp = data[2]
            stamp = int(time.time()) 
            cursor.execute("UPDATE timestamps SET hourly_stamp = ? WHERE user_id = ?", (stamp + 3600 , interaction.user.id))
        except:
            stamp = int(time.time()) 
            cursor.execute("INSERT INTO timestamps(user_id, daily_stamp, hourly_stamp) VALUES(?, ?, ?)",
                           (interaction.user.id, 0, stamp + 3600))
            hourly_stamp = 0
            
        cursor.execute(f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
        data = cursor.fetchone()
        try:
            wallet = data[1]
            bank = data[2]
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, interaction.user.id))
        except:
            cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, earning, 0, 0, 0, interaction.guild.id, 0, 0))
            db.commit()
            wallet = 0
            bank = 0



            earned = wallet + earning
            embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=interaction.created_at)
            embed.set_author(icon_url=interaction.user.display_avatar.url, name=f"{interaction.user.name}'s Casino Chips")
            embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
            embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
            embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
            await interaction.response.send_message(embed=embed)

            db.commit()
            cursor.close()
            db.close()
            return
            
        if hourly_stamp < int(time.time()):
            cursor.execute(f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
            data = cursor.fetchone()
            
            try:
                wallet = data[1]
                bank = data[2]
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, interaction.user.id))
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, earning, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0


            earned = wallet + earning
            embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=interaction.created_at)
            embed.set_author(icon_url=interaction.user.display_avatar.url, name=f"{interaction.user.name}'s Casino Chips")
            embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
            embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
            embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
            await interaction.response.send_message(embed=embed)

            db.commit()
            cursor.close()
            db.close()
            return
        
        else:
            
            embed = discord.Embed(title="Not so fast!", color=discord.Color.red(), timestamp=interaction.created_at)
            embed.add_field(name=f"", value=f"The casino is out of chips for now\n\nThey will return <t:{hourly_stamp}:R>")
            await interaction.response.send_message(embed=embed)
            return

    @hourly.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(collecting_money(bot))