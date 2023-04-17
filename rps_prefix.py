import discord
from discord.ext import commands
import random
from discord.ui import Button, View
import time

class Rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rps", "RPS", "Rps"])      
    @commands.guild_only()
    async def rockpaperscissors(self, ctx:commands.Context, member:discord.Member=None):
        try:
            if member is None:
                choices = ["rock", "paper", "scissors",]
                computers_answer = random.choice(choices)

                rock = Button(
                    label="Rock", style=discord.ButtonStyle.green, emoji="🪨")
                paper = Button(
                    label="Paper", style=discord.ButtonStyle.green, emoji="🧻")
                scissors = Button(label="Scissors",
                                style=discord.ButtonStyle.green, emoji="✂️")

                view = View()
                view.add_item(rock)
                view.add_item(paper)
                view.add_item(scissors)
                embed = discord.Embed(title="Chose between rock, paper or scissors", description="", color=discord.Color.blue())
                await ctx.reply(embed=embed, view=view)

                async def button1_callback(interaction: discord.Interaction):
                    if ctx.author == interaction.user:

                        if computers_answer == "rock":
                            embed = discord.Embed(title="You Tied", description="", color=discord.Color.orange())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Rock", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "paper":
                            embed = discord.Embed(title="You Lost", description="", color=discord.Color.red())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Rock", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "scissors":
                            embed = discord.Embed(title="You Won!", description="", color=discord.Color.green())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Rock", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                    else:
                        await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                rock.callback = button1_callback

                async def button2_callback(interaction: discord.Interaction):
                    if ctx.author == interaction.user:

                        if computers_answer == "rock":
                            embed = discord.Embed(title="You Won!", description="", color=discord.Color.green())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Paper", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "paper":
                            embed = discord.Embed(title="You Tied", description="", color=discord.Color.orange())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Paper", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "scissors":
                            embed = discord.Embed(title="You Lost", description="", color=discord.Color.red())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Paper", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                    else:
                        await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                paper.callback = button2_callback

                async def button3_callback(interaction: discord.Interaction):
                    if ctx.author == interaction.user:

                        if computers_answer == "rock":
                            embed = discord.Embed(title="You Lost", description="", color=discord.Color.red())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Scissors", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "paper":
                            embed = discord.Embed(title="You Won!", description="", color=discord.Color.green())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Scissors", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                        if computers_answer == "scissors":
                            embed = discord.Embed(title="You Tied", description="", color=discord.Color.orange())
                            embed.add_field(name="Computer Answer:", value=computers_answer, inline=False)
                            embed.add_field(name="Your Answer:", value="Scissors", inline=False)

                            await interaction.response.edit_message(embed=embed, view=None)

                    else:
                        await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                scissors.callback = button3_callback

            else:
                if member.id == ctx.author.id:
                    return await ctx.reply("You can't play against yourself!")
                
                wait = int(time.time()) + 60
                
                embed = discord.Embed(
                    title="Rock Paper Scissors", description=f"{ctx.author.mention} invited you to play!", color=discord.Color.blue())
                embed.add_field(
                    name=f"", value=f"Press **ACCEPT** or **DECLINE** _ this invite will be invalid <t:{wait}:R> _", inline=True)
                
                accept = Button(label="ACCEPT", style=discord.ButtonStyle.green)
                decline = Button(label="DECLINE", style=discord.ButtonStyle.danger)
                
                view = View(timeout=60)
                view.add_item(accept)
                view.add_item(decline)

                await ctx.reply(embed=embed, view=view)
                await member.send(f"{ctx.author.mention} invited you to play **ROCK PAPER SCISSORS** in <#{ctx.channel.id}>")
                
                async def decline_call(interaction:discord.Interaction):
                    if interaction.user.id == member.id:
                        embed = discord.Embed(title="Invite declined", description=f"{member.mention} declined your invite :(", color=discord.Color.red())

                        await interaction.response.edit_message(embed=embed, view=None)
                        await ctx.author.send(f"{member.mention} declined your invite of **ROCK PAPER SCISSORS** in <#{ctx.channel.id}>")

                    else:
                        await interaction.response.send_message(f"You're not {member.mention}?", ephemeral=True)
                
                decline.callback = decline_call

                async def accept_call(interaction:discord.Interaction):
                    if interaction.user.id == member.id:

                        rock1 = Button(
                            label="Rock", style=discord.ButtonStyle.green, emoji="🪨")
                        paper1 = Button(
                            label="Paper", style=discord.ButtonStyle.green, emoji="🧻")
                        scissors1 = Button(label="Scissors",
                                        style=discord.ButtonStyle.green, emoji="✂️")

                        view2 = View(timeout=60)
                        view2.add_item(rock1)
                        view2.add_item(paper1)
                        view2.add_item(scissors1)

                        wait3 = int(time.time()) + 60

                        embed = discord.Embed(title=f"Choose an option with<t:{wait3}:R> or this button will be invalid", description=f"{member.mention}'s turn", color=discord.Color.blue())

                        await interaction.response.edit_message(embed=embed, view=view2)
                        await ctx.author.send(f"{member.mention} accepted your invite of **ROCK PAPER SCISSORS** in <#{ctx.channel.id}>")

                        rock2 = Button(
                            label="Rock", style=discord.ButtonStyle.green, emoji="🪨")
                        paper2 = Button(
                            label="Paper", style=discord.ButtonStyle.green, emoji="🧻")
                        scissors2 = Button(label="Scissors",
                                        style=discord.ButtonStyle.green, emoji="✂️")

                        view3 = View(timeout=60)
                        view3.add_item(rock2)
                        view3.add_item(paper2)
                        view3.add_item(scissors2)

                        async def rock1_call(interinter:discord.Interaction):
                            wait2 = int(time.time()) + 60
                            if interinter.user.id == member.id:
                                embed = discord.Embed(title=f"Choose an option with<t:{wait2}:R> or this button will be invalid", description=f"{ctx.author.mention}'s turn", color=discord.Color.blue())

                                await interinter.response.edit_message(embed=embed, view=view3)

                                async def rock2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="You tied", description="", color=discord.Color.orange())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **ROCK**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **ROCK**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                                rock2.callback = rock2_call

                                async def paper2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{ctx.author.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **ROCK**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **PAPER**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                                
                                paper2.callback = paper2_call

                                async def scissors2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{member.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **ROCK**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **SCISSORS**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                                
                                scissors2.callback = scissors2_call
                                
                            else:
                                await interinter.response.send_message(f"You're not {member.mention}?", ephemeral=True)

                        rock1.callback = rock1_call

                        async def paper1_call(interinter:discord.Interaction):
                            wait2 = int(time.time()) + 60
                            if interinter.user.id == member.id:
                                embed = discord.Embed(title=f"Choose an option with<t:{wait2}:R> or this button will be invalid", description=f"{ctx.author.mention}'s turn", color=discord.Color.blue())

                                await interinter.response.edit_message(embed=embed, view=view3)

                                async def rock2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{member.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **PAPER**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **ROCK**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                                rock2.callback = rock2_call

                                async def paper2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**You tied**", color=discord.Color.orange())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **PAPER**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **PAPER**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                                paper2.callback = paper2_call

                                async def scissors2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{ctx.author.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **PAPER**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **SCISSORS**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

                                scissors2.callback = scissors2_call

                            else:
                                await interinter.response.send_message(f"You're not {member.mention}?", ephemeral=True)

                        paper1.callback = paper1_call

                        async def scissors1_call(interinter:discord.Interaction):
                            wait2 = int(time.time()) + 60
                            if interinter.user.id == member.id:
                                embed = discord.Embed(title=f"Choose an option with<t:{wait2}:R> or this button will be invalid", description=f"{ctx.author.mention}'s turn", color=discord.Color.blue())

                                await interinter.response.edit_message(embed=embed, view=view3)

                                async def rock2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{ctx.author.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **SCISSORS**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **ROCK**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                                
                                rock2.callback = rock2_call

                                async def paper2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**{member.mention} won!**", color=discord.Color.green())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **SCISSORS**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **PAPER**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                                
                                paper2.callback = paper2_call

                                async def scissors2_call(interinterinter:discord.Interaction):
                                    if interinterinter.user.id == ctx.author.id:
                                        embed = discord.Embed(title="", description=f"**You tied**", color=discord.Color.orange())
                                        embed.add_field(name="---------------------", value="", inline=False)
                                        embed.add_field(name="", value=f"{member.mention} choose: **SCISSORS**", inline=False)
                                        embed.add_field(name="", value=f"{ctx.author.mention} choose: **SCISSORS**", inline=False)

                                        return await interinterinter.response.edit_message(embed=embed, view=None)
                                    else:
                                        await interinterinter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)
                                
                                scissors2.callback = scissors2_call

                            else:
                                await interinter.response.send_message(f"You're not {member.mention}?", ephemeral=True)

                        scissors1.callback = scissors1_call

                    else:
                        await interaction.response.send_message(f"You're not {member.mention}?", ephemeral=True)

                accept.callback = accept_call
                
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
    

async def setup(bot):
    await bot.add_cog(Rps(bot))
