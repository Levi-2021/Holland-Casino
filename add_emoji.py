import discord
from discord.ext import commands
from discord import app_commands
from io import BytesIO
import aiohttp

class add_emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="add-emoji", description="Adds an emoji to the server (Manage emojis And Stickers required)")
    @app_commands.describe(url="Link of image that you want as emoji")
    @app_commands.describe(name="Name of the emoji")
    async def add_emoji(self, interaction: discord.Interaction, url: str, name: str):
        if interaction.guild == None:
            embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)
            
        if interaction.user.guild_permissions.manage_emojis_and_stickers:
            guild = interaction.guild
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bValue, name=name)
                        embed = discord.Embed(
                            title="Successfully added an emoji!", color=discord.Color.blue())
                        embed.add_field(name="", value=f"Emoji name: **{name}**")
                        embed.set_thumbnail(url=url)
                        await interaction.response.send_message(embed=embed)
                        await ses.close()
                    else:
                        await interaction.response.send_message(f"This did not work | {r.status}")

        else:
            embed = discord.Embed(title="Error ❌", description=f"User {interaction.user.mention} Doesn't have permissions to do that!", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


    @add_emoji.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(add_emoji(bot))