from discord.ext import commands
import discord
import sqlite3


class bot_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help"))
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == ("<@1086017756719226890>"):
            total_members = (sum([len(guild.members) for guild in self.bot.guilds]))
            embed = discord.Embed(color=discord.Color.blue())
            embed.add_field(
                name="", value=f"Watching over **{len(self.bot.guilds)}** servers and **{total_members}** members \n\n> [Invite](https://discord.com/api/oauth2/authorize?client_id=1086017756719226890&permissions=52224&scope=bot) \n> [Support](https://discord.gg/EhEGmegRQd) \n> [Github](https://github.com/Levi-2021/Holland-Casino) \n> [Top GG](https://top.gg/bot/1086017756719226890)", inline=True)
            await message.reply(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        embed = discord.Embed(
            title=f"Welcome to {ctx.guild.name}!", color=discord.Color.blue())
        embed.add_field(
            name="", value=f"Bot info:\n> [Invite](https://discord.com/api/oauth2/authorize?client_id=1086017756719226890&permissions=52224&scope=bot) \n> [Support](https://discord.gg/EhEGmegRQd) \n> [Github](https://github.com/Levi-2021/Holland-Casino) \n> [Top GG](https://top.gg/bot/1086017756719226890) ", inline=True)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(bot_events(bot))