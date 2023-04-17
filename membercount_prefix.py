import discord
from discord.ext import commands


class Membercount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(aliases=["mb", "MB", "Mb", "MEMBERCOUNT", "Membercount"])      
    @commands.guild_only()
    async def membercount(self, ctx:commands.Context):
        try:
            online_members = []
            offline_members = []
            for member in ctx.guild.members:
                if member.status is not discord.Status.offline:
                    online_members.append(member.name)
                else:
                    offline_members.append(member.name)

            real_user_count = len([x for x in ctx.guild.members if not x.bot])
            membercount = ctx.guild.member_count
            bot_count =  membercount - real_user_count 

            embed = discord.Embed(title=f'{membercount} members in {ctx.guild.name}',
                                color=discord.Color.blue())
            embed.add_field(name="Real Users:", value=f"```c\n{real_user_count:,}```", inline=False)
            embed.add_field(name="Bots:", value=f"```c\n{bot_count:,}```", inline=False)
            embed.add_field(name="---------------------", value="", inline=False)
            embed.add_field(name="Online Members:", value=f"```c\n{len(online_members):,}```" , inline=False)
            embed.add_field(name="Offline Members:", value=f"```c\n{len(offline_members):,}```" , inline=False)
            
            await ctx.reply(embed=embed)
            return
        
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Membercount(bot))
