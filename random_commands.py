import discord
from discord import app_commands
from discord.ext import commands


class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="ping", description="Shows the latency of the bot")
    async def p(self, interaction: discord.Interaction):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
                
            latency = round(self.bot.latency * 1000, 1)
            embed = discord.Embed(title="", color=discord.Color.blue(),
                                timestamp=interaction.created_at)
            embed.add_field(name="Pong! 🏓", value=f"```yaml\n{latency} ms```", inline=True)

        await interaction.response.send_message(embed=embed)
        
    @p.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


    @app_commands.command(name="avatar", description="Shows the avatar of the user")
    @app_commands.describe(member="Member you want to get avatar of")
    async def av(self, interaction: discord.Interaction, member: discord.Member = None):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else: 
                
            user = member
            if user == None:
                user = interaction.user

            embed = discord.Embed(color=discord.Color.blue(
            ), title=f"{user}", timestamp=interaction.created_at,)
            embed.set_image(url=user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

    @av.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)
        


async def setup(bot):
    await bot.add_cog(OtherCommands(bot))