import random
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View


class baccarat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="baccarat", description="Play a game of baccarat")
    @app_commands.describe(amount="Amount you wish to bet")

    async def baccarat(self, interaction:discord.Interaction, amount:int):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:
            if amount < 0:
                await interaction.response.send_message("You can't bet less than 0")
                return
            
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id={interaction.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                wallet = 0
                spend_on_gambling = 0
                won_with_gambling = 0

            if wallet < amount:
                await interaction.response.send_message("You don't have enough money in your wallet")
                return

            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                        (wallet - amount, interaction.user.id))
            db.commit()

            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?",
                        (spend_on_gambling + amount, interaction.user.id))
            db.commit()


            ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '0', '0', '0']

            player_randint_1 = random.randint(0,12)
            player_randint_2 = random.randint(0,12)

            banker_randint_1 = random.randint(0,12)
            banker_randint_2 = random.randint(0,12)
            
            player = []
            banker = []

            player.append(ranks[player_randint_1])
            player.append(ranks[player_randint_2])

            banker.append(ranks[banker_randint_1])
            banker.append(ranks[banker_randint_2])

            player_total = int(player[0]) + int(player[1])
            banker_total = int(banker[0]) + int(banker[1])

            while player_total > 9:
                player = []
                ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '0', '0', '0']

                player_randint_1 = random.randint(0,12)
                player_randint_2 = random.randint(0,12)

                player.append(ranks[player_randint_1])
                player.append(ranks[player_randint_2])

                player_total = int(player[0]) + int(player[1])

            while banker_total > 9:
                banker = []
                ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '0', '0', '0']

                banker_randint_1 = random.randint(0,12)
                banker_randint_2 = random.randint(0,12)

                banker.append(ranks[banker_randint_1])
                banker.append(ranks[banker_randint_2])
                
                banker_total = int(banker[0]) + int(banker[1])

            player_button = Button(label="Player (x2)")
            banker_button = Button(label="Banker (x2)")
            tie_button = Button(label="Tie (x10)")

            view = View(timeout=None)

            view.add_item(player_button)
            view.add_item(banker_button)
            view.add_item(tie_button)

            embed = discord.Embed(title="Baccarat", color=discord.Color.blue())
            embed.add_field(name="", value="Choose an option")
            embed.set_image(url="https://eidk95seyu2.exactdn.com/en/blog/wp-content/uploads/2022/04/body-representation-of-an-online-baccarat-table-baccarat-history.jpg?strip=all&lossy=1&ssl=1&fit=805,455")

            await interaction.response.send_message(embed=embed, view=view)

            async def player_call(inter:discord.Interaction):
                if interaction.user.id == inter.user.id:

                    if player_total > banker_total:
                        embed = discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="You betted on:", value="Player (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, interaction.user.id))
                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, interaction.user.id))
                        db.commit()
                        return
                    
                    else:
                        embed = discord.Embed(title="You lost", color=discord.Color.red())
                        embed.add_field(name="You betted on:", value="Player (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        return
                        
                else:
                    await inter.response.send_message(f"You're not {interaction.user.mention}?", ephemeral=True)
                
            player_button.callback = player_call

            async def banker_call(inter:discord.Interaction):
                if interaction.user.id == inter.user.id:

                    if banker_total > player_total:
                        embed = discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="You betted on:", value="Banker (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet + amount * 2:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2, interaction.user.id))
                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 2, interaction.user.id))
                        db.commit()
                        return

                    if player_total == banker_total:
                        embed = discord.Embed(title="You tied", color=discord.Color.orange())
                        embed.add_field(name="You betted on:", value="Player (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount , interaction.user.id))
                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount , interaction.user.id))
                        db.commit()
                        return
                    
                    else:
                        embed = discord.Embed(title="You lost", color=discord.Color.red())
                        embed.add_field(name="You betted on:", value="Banker (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        return

                else:
                    await inter.response.send_message(f"You're not {interaction.user.mention}?", ephemeral=True)
            
            banker_button.callback = banker_call

            async def tie_call(inter:discord.Interaction):
                if interaction.user.id == inter.user.id:

                    if banker_total == player_total:
                        embed = discord.Embed(title="You won!", color=discord.Color.green())
                        embed.add_field(name="You betted on:", value="Tie (x10)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet + amount * 10:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 10, interaction.user.id))
                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount * 10, interaction.user.id))
                        db.commit()
                        return

                    if player_total == banker_total:
                        embed = discord.Embed(title="You tied", color=discord.Color.orange())
                        embed.add_field(name="You betted on:", value="Player (x2)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount , interaction.user.id))
                        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won_with_gambling + amount , interaction.user.id))
                        db.commit()
                        return
                    
                    else:
                        embed = discord.Embed(title="You lost", color=discord.Color.red())
                        embed.add_field(name="You betted on:", value="Tie (x10)", inline=False)
                        embed.add_field(name="Bet:", value=f"```yaml\n{amount:,} casino chips```", inline=False)
                        embed.add_field(name="Player:", value=f"{player[0]} + {player[1]} ({player_total})", inline=False)
                        embed.add_field(name="Banker:", value=f"{banker[0]} + {banker[1]} ({banker_total})", inline=False)
                        embed.add_field(name="New balance:", value=f"```yaml\n{wallet - amount:,} casino chips```", inline=False)

                        await inter.response.edit_message(view=None, embed=embed)
                        return

                else:
                    await inter.response.send_message(f"You're not {interaction.user.mention}?", ephemeral=True)
            
            tie_button.callback = tie_call

    @baccarat.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(baccarat(bot))