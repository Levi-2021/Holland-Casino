import discord
from discord.ext import commands


class RandomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["avatar", "AVATAR", "Avatar", "AV", "Av"])      
    async def av(self, ctx:commands.Context, member: discord.Member = None):
        try:
            user = member
            if user == None:
                user = ctx.author

            embed = discord.Embed(color=discord.Color.blue(
            ), title=f"{user}", timestamp=ctx.message.created_at,)
            embed.set_image(url=user.display_avatar.url)
            await ctx.reply(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
    
    
    @commands.command(aliases=["pong", "PONG", "Pong", "PING", "Ping"])      
    async def ping(self, ctx:commands.Context):
        try:
            latency = round(self.bot.latency * 1000, 1)
            embed = discord.Embed(title="", color=discord.Color.blue(),
                                timestamp=ctx.message.created_at)
            embed.add_field(name="Pong! 🏓", value=f"```yaml\n{latency} ms```", inline=True)

            await ctx.reply(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
        
async def setup(bot):
    await bot.add_cog(RandomCommands(bot))
