import discord
from discord.ext import commands
import sqlite3
from discord.ui import View, Select
import random


class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["rl", "RL", "Rl", "ROULETTE", "Roulette"])      
    @commands.guild_only()
    async def roulette(self, ctx:commands.Context, amount=None):
        try:
                
            if amount == None:
                return await ctx.reply("No amount was given")

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db.commit()
                wallet = 0
                spend_on_gambling = 0
                won_with_gambling = 0

            if amount == "all":
                amount = wallet

            if amount == "half":
                amount = wallet / 2

            amount = int(amount)
            if wallet < amount:
                return await ctx.reply("You do not have that much money")

            elif amount < 0:
                return await ctx.reply("Amount has to be 0 or more")

            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend_on_gambling + amount, ctx.author.id))

            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
            db.commit()

            roulette = random.randint(0, 36)

            select = Select(
                            placeholder="Choose an option",
                            options=[
                                discord.SelectOption(
                                    label="Green (36x)"),
                                discord.SelectOption(
                                    label="Black (2x)"),
                                discord.SelectOption(label="Red (2x)"),
                                discord.SelectOption(label="Odd (2x)"),
                                discord.SelectOption(label="Even (2x)"),
                                discord.SelectOption(
                                    label="1 to 18 (2x)"),
                                discord.SelectOption(
                                    label="19 to 36 (2x)"),
                                discord.SelectOption(
                                    label="1st 12 (4x)"),
                                discord.SelectOption(
                                    label="2nd 12 (4x)"),
                                discord.SelectOption(
                                    label="3rd 12 (4x)"),
                                discord.SelectOption(
                                    label="1st column (4x)"),
                                discord.SelectOption(
                                    label="2nd column (4x)"),
                                discord.SelectOption(
                                    label="3rd column (4x)")
                            ])

            async def call(inter:discord.Interaction):
                if inter.user.id == ctx.author.id:
                    if select.values[0] == "Green (36x)":
                        if roulette == 0:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value="0 | :green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 36:,} casino chips```", inline=False)
                            

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 36, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 36, ctx.author.id))
                            db.commit()
                            return
                        
                        if roulette > 18:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":black_large_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":red_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                    if select.values[0] == "Black (2x)":
                        if roulette > 16:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":black_large_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)
                            
                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                            db.commit()
                            return
                        
                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)
                            
                            await inter.response.edit_message(view=None, embed=embed)
                            return

                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":red_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)
                            
                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                    if select.values[0] == "Red (2x)":
                        if roulette ==0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return

                        
                        if roulette > 18:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":black_large_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        else:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":red_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                            db.commit()
                            return


                    if select.values[0] == "Even (2x)":
                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette > 18:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"Even ", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                            db.commit()
                            return

                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"Odd", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                    if select.values[0] == "Odd (2x)":
                        if roulette > 18:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"Odd", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                            db.commit()
                            return

                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"Even", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return

                    if select.values[0] == "1 to 18 (2x)":
                        if roulette < 19:
                            if roulette > 0:
                                embed = discord.Embed(title="You won!", color=discord.Color.green())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"1 to 18", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                                db.commit()
                                return
                            
                        if roulette == 0:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"19 to 36", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return

                    if select.values[0] == "19 to 36 (2x)":
                        if roulette > 18:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"19 to 36", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, ctx.author.id))
                            db.commit()
                            return
                            
                        if roulette == 0:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1 to 18", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                    if select.values[0] == "1st 12 (4x)":
                        if roulette == 0:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette < 13:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st 12", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 4:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                            db.commit()
                            return
                            
                        if roulette > 12:
                            if roulette < 24:

                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return
                        
                            else:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                    if select.values[0] == "2nd 12 (4x)":
                        if roulette == 0:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette < 13:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st 12", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                            
                        if roulette > 12:
                            if roulette < 24:

                                embed = discord.Embed(title="You won!", color=discord.Color.green())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"{amount:,} casino chips", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 4:,} casino chips```", inline=False)

                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                                db.commit()

                                await inter.response.edit_message(view=None, embed=embed)
                                return
                        
                            else:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                    if select.values[0] == "3rd 12 (4x)":
                        if roulette == 0:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette < 13:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st 12", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                            
                        if roulette > 12:
                            if roulette < 24:

                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"{amount:,} casino chips", inline=False)
                                embed.add_field(name="New Balance:", value=f"{wallet - amount:,} casino chips", inline=False)


                                await inter.response.edit_message(view=None, embed=embed)
                                return
                        
                            else:
                                embed = discord.Embed(title="You won!", color=discord.Color.green())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd 12", inline=False)
                                embed.add_field(name="Bet:", value=f"{amount:,} casino chips", inline=False)
                                embed.add_field(name="New Balance:", value=f"{wallet +  amount * 4:,} casino chips", inline=False)

                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                                db.commit()

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                    if select.values[0] == "1st column (4x)":

                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette < 12:
                            embed = discord.Embed(title="You won!", color=discord.Color.green())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st Column", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 4:,} casino chips```", inline=False)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                            cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                            db.commit()

                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                            
                        if roulette > 12:
                            if roulette < 24:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                            else:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                    if select.values[0] == "2nd column (4x)":
                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)


                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette < 12:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st Column", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)


                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette > 12:
                            if roulette > 24:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return
                            else:
                                embed = discord.Embed(title="You won!", color=discord.Color.green())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 4:,} casino chips```", inline=False)

                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                                db.commit()

                                await inter.response.edit_message(view=None, embed=embed)
                                return
                            
                        else:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                            await inter.response.edit_message(view=None, embed=embed)
                            return

                    if select.values[0] == "3rd column (4x)":
                        if roulette == 0:
                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f":green_square:", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)


                            await inter.response.edit_message(view=None, embed=embed)
                            return

                        if roulette < 12:

                            embed = discord.Embed(title="You lost", color=discord.Color.red())
                            embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                            embed.add_field(name="Landed On:", value=f"1st Column", inline=False)
                            embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                            embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)


                            await inter.response.edit_message(view=None, embed=embed)
                            return
                        
                        if roulette > 12:
                            if roulette < 24:
                                embed = discord.Embed(title="You lost", color=discord.Color.red())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"2nd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                                await inter.response.edit_message(view=None, embed=embed)
                                return
                            else:
                                embed = discord.Embed(title="You won!", color=discord.Color.green())
                                embed.add_field(name="Betted On:", value=select.values[0], inline=False)
                                embed.add_field(name="Landed On:", value=f"3rd Column", inline=False)
                                embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                                embed.add_field(name="New Balance:", value=f"```yaml\n{wallet + amount * 4:,} casino chips```", inline=False)

                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 4, ctx.author.id))
                                cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 4, ctx.author.id))
                                db.commit()

                                await inter.response.edit_message(view=None, embed=embed)
                                return

                else:
                    await inter.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

            select.callback = call

            view = View(timeout=None)
            view.add_item(select)

            embed = discord.Embed(title="")
            embed.set_image(url="https://as1.ftcdn.net/v2/jpg/01/44/33/66/1000_F_144336685_lIKJEs8RzqhbpOwCycZTsFT0Eywxl41M.jpg")

            await ctx.reply(embed=embed, view=view)
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Roulette(bot))
