import discord
from discord.ext import commands
import sqlite3


class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases=["GIVE", "Give", "SEND", "Send", "send"])      
    @commands.guild_only()
    async def give(self, ctx:commands.Context, amount=None, member:discord.Member=None):
        try:
            if member.id == 1086017756719226890:
                embed = discord.Embed(title="", description="Thanks for the money but i dont need it ^~^", color=discord.Color.blue())
                return await ctx.reply(embed=embed)
            
            if amount == None:
                return await ctx.reply("No amount was given")
            
            if member == None:
                return await ctx.reply("No member was given")
            
            if member.id == ctx.author.id:
                return await ctx.reply("You can't give yourself money")
                
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()

            try:
                userwallet = data[1]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                userwallet = 0

            if userwallet < amount:
                await ctx.reply("You don't have enough money in your wallet")
                return
            
            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {member.id}")
            data = cursor.fetchone()

            try:
                memberwallet = data[1]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (member.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                memberwallet = 0
            
            amount = round(amount*(80/100))
            
            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                        (memberwallet + amount, member.id))
            db.commit()
            
            embed = discord.Embed(description=f"{ctx.author.mention} gave you **{round(amount)}** Casino Chips", color=discord.Color.blue())
            embed.set_footer(icon_url=ctx.author.display_avatar.url, text="20% tax included")
            
            await ctx.reply(member.mention, embed=embed)
            return
        
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Give(bot))
