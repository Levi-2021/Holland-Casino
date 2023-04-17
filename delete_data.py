import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from discord.ui import View, Button
from asyncio import sleep


class DeleteData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete-data", description="Delete all data that the bot has from you")
    async def delete(self, inter:discord.Interaction):
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM economy WHERE user_id = {inter.user.id}")
        data = cursor.fetchone()

        db1 = sqlite3.connect("invest.sqlite")
        cursor1 = db1.cursor()
        
        try:
            wallet = data[1]
        except:
            embed = discord.Embed(title=f"Error", description=f"There is no data stored for {inter.user.mention} ({inter.user.id})", color=discord.Color.red(), timestamp=inter.created_at)
            embed.set_footer(text="Error", icon_url=inter.user.display_avatar.url)
            
            return await inter.response.send_message(embed=embed)
        
        yes = Button(label="YES", emoji="✅", style=discord.ButtonStyle.green)
        no = Button(label="NO", emoji="❌", style=discord.ButtonStyle.danger)
        
        view = View(timeout=None)
        view.add_item(yes)
        view.add_item(no)
        
        
        embed = discord.Embed(title=f"", description=f"Are you sure you want to delete all data for {inter.user.mention} ({inter.user.id})?\n\n_this can't be undone_ ", color=discord.Color.blue(), timestamp=inter.created_at)
        embed.set_footer(text="Preparing...", icon_url=inter.user.display_avatar.url)
                        
        await inter.response.send_message(embed=embed, view=view)
        
        async def yes_call(interaction:discord.Interaction):
            if interaction.user.id != inter.user.id:
                await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)
            else:
                embed = discord.Embed(title="", description=f"**DELETING ALL DATA FOR {inter.user.mention}...**", color=discord.Color.orange(), timestamp=inter.created_at)
                embed.set_footer(text="Deleting Data...", icon_url=inter.user.display_avatar.url)
                await interaction.response.edit_message(embed=embed, view=None)
                
                cursor.execute("UPDATE economy SET user_id=? WHERE user_id = ?", (0, inter.user.id))
                cursor.execute("UPDATE timestamps SET user_id=? WHERE user_id = ?", (0, inter.user.id))
                cursor1.execute("UPDATE stock SET user_id=? WHERE user_id = ?", (0, inter.user.id))

                cursor.execute("DELETE FROM economy WHERE user_id = 0")
                cursor.execute("DELETE FROM timestamps WHERE user_id = 0")
                cursor1.execute("DELETE FROM stock WHERE user_id = 0")
                db.commit()
                db1.commit()
                
                await sleep(3)
                
                embed = discord.Embed(title="Data Deleted", description=f"Successfully delete all data for {inter.user.mention} ({inter.user.id})", color=discord.Color.green(), timestamp=inter.created_at)
                embed.set_footer(text="Data Deleted Successfully", icon_url=inter.user.display_avatar.url)
                
                return await interaction.edit_original_response(embed=embed, view=None)
                
        yes.callback = yes_call
        
        async def no_call(interaction:discord.Interaction):
            if interaction.user.id != inter.user.id:
                await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)
            else:
                embed = discord.Embed(title="Data was not deleted", description=f"Data deleting was cancel by {inter.user.mention} ({inter.user.id})", color=discord.Color.red(), timestamp=inter.created_at)
                embed.set_footer(text="Data Not deleted", icon_url=inter.user.display_avatar.url)
                
                return await interaction.response.edit_message(embed=embed, view=None)
            
        no.callback = no_call
            
    @delete.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DeleteData(bot))
