import discord
from discord.ext import commands
from discord import app_commands
import sqlite3


class Storeddata(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases=["data", "DATA", "Data"])      
    async def storeddata(self, ctx:commands.Context):
        try:
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id}")
            data = cursor.fetchall()


            try:
                user_id = data[0]

            except:
                embed = discord.Embed(title="Error ❌", description=f"No data stored for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.red())
                return await ctx.reply(embed=embed)
            
            await ctx.reply(f"I've sent you a DM {ctx.author.mention}")
            
            embed = discord.Embed(title="", description=f"All economy data stored for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.blue(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f"ALL ECONOMY DATA STORED FOR {ctx.author}", icon_url=ctx.author.display_avatar.url)
            
            for table in data:
                embed.add_field(name="", value=f"Guild ID: \n{table[5]} \n**User ID:** \n{table[0]}\n**Pocket Chips:** \n{table[1]:,} \n**Bank Chips:** \n{table[2]:,} \n**Total Chips:** \n{table[6]:,} \n**Total spend on gambling:** \n{table[3]:,} \n**Total won with gambling:** \n{table[4]:,} \n**Profits** \n{table[7]:,}", inline=False)
                embed.add_field(name="-------------------", value="", inline=False)
                
            await ctx.author.send(embed=embed)

            cursor.execute(f"SELECT * FROM timestamps WHERE user_id = {ctx.author.id}")
            data = cursor.fetchall()
            
            embed = discord.Embed(title="", description=f"All timestamp data stored for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.blue(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f"ALL TIMESTAMP DATA STORED FOR {ctx.author}", icon_url=ctx.author.display_avatar.url)
            
            for table in data:
                embed.add_field(name="", value=f"**User ID:** \n{table[0]} \n**Hourly Timestamp: **\n{table[2]} \n**Daily Timestamp: **\n{table[1]}", inline=False)
                embed.add_field(name="-------------------", value="", inline=False)
                
            await ctx.author.send(embed=embed)

            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()
            
            cursor1.execute(f"SELECT * FROM stock WHERE user_id = {ctx.author.id}")
            data = cursor1.fetchall()
            
            embed = discord.Embed(title="", description=f"All stock data stored for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.blue(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f"ALL STOCK DATA STORED FOR {ctx.author}", icon_url=ctx.author.display_avatar.url)
            
            for table in data:
                embed.add_field(name="", value=f"**User ID:** \n{table[0]} \n**Stock Amount: **\n{table[1]}", inline=False)
                embed.add_field(name="-------------------", value="", inline=False)
                
            await ctx.send(embed=embed)
    
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Storeddata(bot))
