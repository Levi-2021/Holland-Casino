import discord
from discord.ext import commands
from discord import app_commands


class member_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="member-count", description="Shows the member count of the server")

    async def member_count(self, inter:discord.Interaction):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
        else:
                
            online_members = []
            offline_members = []
            for member in inter.guild.members:
                if member.status is not discord.Status.offline:
                    online_members.append(member.name)
                else:
                    offline_members.append(member.name)

            real_user_count = len([x for x in inter.guild.members if not x.bot])
            membercount = inter.guild.member_count
            bot_count =  membercount - real_user_count 

            embed = discord.Embed(title=f'{membercount} members in {inter.guild.name}',
                                color=discord.Color.blue())
            embed.add_field(name="Real Users:", value=f"```c\n{real_user_count:,}```", inline=False)
            embed.add_field(name="Bots:", value=f"```c\n{bot_count:,}```", inline=False)
            embed.add_field(name="---------------------", value="", inline=False)
            embed.add_field(name="Online Members:", value=f"```c\n{len(online_members):,}```" , inline=False)
            embed.add_field(name="Offline Members:", value=f"```c\n{len(offline_members):,}```" , inline=False)
            
            await inter.response.send_message(embed=embed)
            return

    @member_count.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(member_count(bot))