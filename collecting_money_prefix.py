import discord
from discord.ext import commands
import sqlite3
import random
import time


class collectingmoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["daily", "DAILY", "Daily"])      
    @commands.guild_only()
    async def daily_chips(self, ctx:commands.Context):
        try:
            earning = random.randint(1500, 2000)
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {ctx.author.id}")
            data = cursor.fetchone()
            
            try:
                daily_stamp = data[1]
                stamp = int(time.time()) 
                cursor.execute("UPDATE timestamps SET daily_stamp = ? WHERE user_id = ?", (stamp + 86400, ctx.author.id))
            except:
                stamp = int(time.time()) 
                cursor.execute("INSERT INTO timestamps(user_id, daily_stamp, hourly_stamp) VALUES(?, ?, ?)",
                            (ctx.author.id, stamp + 86400, 0))
                daily_stamp = 0
                
            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()
            try:
                wallet = data[1]
                bank = data[2]
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, earning, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0



                earned = wallet + earning
                embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await ctx.reply(embed=embed)

                db.commit()
                cursor.close()
                db.close()
                return
                
            if daily_stamp < int(time.time()):
                cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
                data = cursor.fetchone()
                
                try:
                    wallet = data[1]
                    bank = data[2]
                    cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
                except:
                    cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, earning, 0, 0, 0, ctx.guild.id, 0, 0))
                    db.commit()
                    wallet = 0
                    bank = 0


                earned = wallet + earning
                embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await ctx.reply(embed=embed)

                db.commit()
                cursor.close()
                db.close()
                return
            
            else:
                
                embed = discord.Embed(title="Not so fast!", color=discord.Color.red(), timestamp=ctx.message.created_at)
                embed.add_field(name=f"", value=f"The casino is out of chips for now\n\nThey will return <t:{daily_stamp}:R>")
                await ctx.reply(embed=embed)
                return
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)


    @commands.command(aliases=["hourly", "HOURLY", "Hourly"])      
    @commands.guild_only()
    async def hourly_chips(self, ctx:commands.Context):
        try:
            earning = random.randint(500, 1000)
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {ctx.author.id}")
            data = cursor.fetchone()
            
            try:
                hourly_stamp = data[2]
                stamp = int(time.time()) 
                cursor.execute("UPDATE timestamps SET hourly_stamp = ? WHERE user_id = ?", (stamp + 3600 , ctx.author.id))
            except:
                stamp = int(time.time()) 
                cursor.execute("INSERT INTO timestamps(user_id, daily_stamp, hourly_stamp) VALUES(?, ?, ?)",
                            (ctx.author.id, 0, stamp + 3600))
                hourly_stamp = 0
                    
            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()
            try:
                wallet = data[1]
                bank = data[2]
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, earning, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0



                earned = wallet + earning
                embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await ctx.reply(embed=embed)

                db.commit()
                cursor.close()
                db.close()
                return
                
            if hourly_stamp < int(time.time()):
                cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
                data = cursor.fetchone()
                
                try:
                    wallet = data[1]
                    bank = data[2]
                    cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + earning, ctx.author.id))
                except:
                    cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, earning, 0, 0, 0, ctx.guild.id, 0, 0))
                    db.commit()
                    wallet = 0
                    bank = 0


                earned = wallet + earning
                embed = discord.Embed(description=f"The casino gave you {earning:,} chips", color=discord.Color.blue(), timestamp=ctx.message.created_at)
                embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"{ctx.author.name}'s Casino Chips")
                embed.add_field(name="Pocket Chips", value=f"```yaml\n{earned:,}```", inline=False)
                embed.add_field(name="Bank Chips", value=f"```yaml\n{bank:,}```", inline=False)
                embed.add_field(name="Total Chips", value=f"```yaml\n{bank + earned:,}```", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1086018695257665606/1094698861009829969/uGgGWfD.png")
                await ctx.reply(embed=embed)

                db.commit()
                cursor.close()
                db.close()
                return
            
            else:
                
                embed = discord.Embed(title="Not so fast!", color=discord.Color.red(), timestamp=ctx.message.created_at)
                embed.add_field(name=f"", value=f"The casino is out of chips for now\n\nThey will return <t:{hourly_stamp}:R>")
                await ctx.reply(embed=embed)
                return
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(collectingmoney(bot))