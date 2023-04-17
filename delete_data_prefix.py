import discord
from discord.ext import commands
import sqlite3
from discord.ui import Button, View
from asyncio import sleep


class DeletDataPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["delete", "DELETE", "Delete"])      
    async def deletedata(self, ctx:commands.Context):
        try:
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id}")
            data = cursor.fetchone()

            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            try:
                wallet = data[1]
                
            except:
                embed = discord.Embed(title=f"Error", description=f"There is no data stored for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.red(), timestamp=ctx.message.created_at)
                embed.set_footer(text="Error", icon_url=ctx.author.display_avatar.url)
                
                return await ctx.reply(embed=embed)
            
            yes = Button(label="YES", emoji="✅", style=discord.ButtonStyle.green)
            no = Button(label="NO", emoji="❌", style=discord.ButtonStyle.danger)
            
            view = View(timeout=None)
            view.add_item(yes)
            view.add_item(no)
            
            
            embed = discord.Embed(title=f"", description=f"Are you sure you want to delete all data for {ctx.author.mention} ({ctx.author.id})?\n\n_this can't be undone_ ", color=discord.Color.blue(), timestamp=ctx.message.created_at)
            embed.set_footer(text="Preparing...", icon_url=ctx.author.display_avatar.url)
                            
            await ctx.reply(embed=embed, view=view)
            
            async def yes_call(interaction:discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                else:
                    embed = discord.Embed(title="", description=f"**DELETING ALL DATA FOR {ctx.author.mention}...**", color=discord.Color.orange(), timestamp=ctx.message.created_at)
                    embed.set_footer(text="Deleting Data...", icon_url=ctx.author.display_avatar.url)
                    await interaction.response.edit_message(embed=embed, view=None)
                    
                    cursor.execute("UPDATE economy SET user_id=? WHERE user_id = ?", (0, ctx.author.id))
                    cursor.execute("UPDATE timestamps SET user_id=? WHERE user_id = ?", (0, ctx.author.id))
                    cursor1.execute("UPDATE stock SET user_id=? WHERE user_id = ?", (0, ctx.author.id))

                    cursor.execute("DELETE FROM economy WHERE user_id = 0")
                    cursor.execute("DELETE FROM timestamps WHERE user_id = 0")
                    cursor1.execute("DELETE FROM stock WHERE user_id = 0")
                    db.commit()
                    db1.commit()
                    
                    await sleep(3)
                    
                    embed = discord.Embed(title="Data Deleted", description=f"Successfully delete all data for {ctx.author.mention} ({ctx.author.id})", color=discord.Color.green(), timestamp=ctx.message.created_at)
                    embed.set_footer(text="Data Deleted Successfully", icon_url=ctx.author.display_avatar.url)
                    
                    return await interaction.edit_original_response(embed=embed, view=None)
                    
            yes.callback = yes_call
            
            async def no_call(interaction:discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                else:
                    embed = discord.Embed(title="Data was not deleted", description=f"Data deleting was cancel by {ctx.author.mention} ({ctx.author.id})", color=discord.Color.red(), timestamp=ctx.message.created_at)
                    embed.set_footer(text="Data Not deleted", icon_url=ctx.author.display_avatar.url)
                    
                    return await interaction.response.edit_message(embed=embed, view=None)
                
            no.callback = no_call
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(DeletDataPrefix(bot))
