import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import random
import sqlite3

class bj(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="black-jack", description="Play black jack and win up to 2x")

    @app_commands.describe(amount="Amount you wish to bet")
    async def bj(self, interaction:discord.Interaction, amount:int):
        if interaction.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await interaction.response.send_message(embed=embed)
        else:

            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM economy WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild.id}")
            data = cursor.fetchone()
            try:
                wallet = data[1]
                spend_on_gambling = data[3]
                won_with_gambling = data[4]
            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (interaction.user.id, 0, 0, 0, 0, interaction.guild.id, 0, 0))
                db.commit()
                won_with_gambling = 0
                spend_on_gambling = 0

            if wallet < amount:
                await interaction.response.send_message("You don't have that much money in your wallet")
                return
            
            if amount < 0:
                return
            

            cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend_on_gambling + amount, interaction.user.id))

            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))
            
            dealer_card = []
            cards = []
            first_card = random.randint(2,11)
            seconds_card = random.randint(2,11)
            if first_card + seconds_card == 22:
                first_card = 1
            dealer1 = random.randint(2,11)
            dealer2 = random.randint(2,11)
            if dealer1 + dealer2 == 22:
                dealer1 = 1
            
            if dealer1 + dealer2 == 21:
                dealer2 = 1
            cards.append(first_card)
            cards.append(seconds_card)
            dealer_card.append(dealer1)
            dealer_card.append(dealer2)

            hit = Button(label="Hit", style=discord.ButtonStyle.blurple)
            stand = Button(label="Stand", style=discord.ButtonStyle.blurple)
            hit2 = Button(label="Hit", style=discord.ButtonStyle.blurple)
            stand2 = Button(label="Stand", style=discord.ButtonStyle.blurple)
            stand3 = Button(label="Stand", style=discord.ButtonStyle.blurple)

            view = View()
            hit.disabled = False
            stand.disabled = False
            view.add_item(hit)
            view.add_item(stand)

            view2 = View()
            hit2.disabled = True
            stand2.disabled = True
            view2.add_item(hit2)
            view2.add_item(stand2)

            player_cards = first_card + seconds_card
            dealer_total = dealer1 + dealer2

            if first_card == 11:
                if seconds_card == 11:
                    first_card = 1


            if player_cards == 21:
                embed = discord.Embed(title="You Won!", color=discord.Color.green())
                embed.add_field(name="Your Hand", value=f"🃏 21", inline=False)
                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                await interaction.response.send_message(embed=embed, view=view2)
                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                db.commit()
                cursor.close()
                db.close()
                return

            embed = discord.Embed(title="🃏 Black Jack 🃏", color=discord.Color.blue())
            embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
            embed.add_field(name="Dealers Hand", value=f"🃏 *Unknown Cards*")
            await interaction.response.send_message(embed=embed, view=view)

            async def hit_call(inter:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if inter.user.id == interaction.user.id:
                    view3 = View()
                    hit.disabled = False
                    stand3.disabled = False
                    view3.add_item(hit)
                    view3.add_item(stand3)
                    new_card = random.randint(2,11)
                    cards.append(new_card)

                    sum = 0;    
                    for i in range(0, len(cards)):    
                        sum = sum + cards[i];    
                    player_cards_ = sum
                    
                    if player_cards_ == 21:
                        embed = discord.Embed(title="You Won!", color=discord.Color.green())
                        embed.add_field(name="Your Hand", value=f"🃏 21", inline=False)
                        embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                        await inter.response.edit_message(embed=embed, view=view2)
                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                        cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                        db.commit()
                        cursor.close()
                        db.close()
                        return

                    elif player_cards_ > 21:
                        embed = discord.Embed(title="You Lost", color=discord.Color.red())
                        embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                        embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                        await inter.response.edit_message(embed=embed, view=view2)
                        return

                    elif player_cards_ < 21:
                        embed = discord.Embed(title="🃏 Black Jack 🃏", color=discord.Color.blue())
                        embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                        embed.add_field(name="Dealers Hand", value=f"🃏 *Unknown Cards*")
                        await inter.response.edit_message(embed=embed, view=view3)

                        async def stand3_call(inter:discord.Interaction):
                            db = sqlite3.connect("economy.sqlite")
                            cursor = db.cursor()
                            if inter.user.id == interaction.user.id:
                                dealer_total = random.randint(18, 24)

                                if dealer_total == 21:
                                    embed = discord.Embed(title="You Lost", color=discord.Color.red())
                                    embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                                    embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                    await inter.response.edit_message(embed=embed, view=view2)
                                    return

                                if dealer_total > 21:

                                    embed = discord.Embed(title="You Won!", color=discord.Color.green())
                                    embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                                    embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                    await inter.response.edit_message(embed=embed, view=view2)
                                    cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                                    cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                                    db.commit()
                                    cursor.close()
                                    db.close()
                                    return

                                if dealer_total > 17:
                                    if player_cards_ > dealer_total:
                                        embed = discord.Embed(title="You Won!", color=discord.Color.green())
                                        embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                                        embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                        await inter.response.edit_message(embed=embed, view=view2)
                                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                                        cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                                        db.commit()
                                        cursor.close()
                                        db.close()
                                        return
                                    
                                    if dealer_total > player_cards_:
                                        embed = discord.Embed(title="You Lost", color=discord.Color.red())
                                        embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                                        embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                        await inter.response.edit_message(embed=embed, view=view2)
                                        return
                                    
                                    if dealer_total == player_cards_:

                                        embed = discord.Embed(title="You Tied", color=discord.Color.orange())
                                        embed.add_field(name="Your Hand", value=f"🃏 {player_cards_}", inline=False)
                                        embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                        await inter.response.edit_message(embed=embed, view=view2)
                                        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount, interaction.user.id))
                                        cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount} WHERE user_id = {interaction.user.id}")
                                        db.commit()
                                        cursor.close()
                                        db.close()
                                        return
                            else:
                                await inter.response.send_message(f"You're not {interaction.user.mention}", ephemeral=True)
                        stand3.callback = stand3_call
                else:
                    await inter.response.send_message(f"You're not {interaction.user.mention}", ephemeral=True)
            hit.callback = hit_call


            async def stand_call(inter:discord.Interaction):
                db = sqlite3.connect("economy.sqlite")
                cursor = db.cursor()
                if inter.user.id == interaction.user.id:
                    dealer_total = random.randint(18, 24)
                    try:
                        if dealer_total == 21:
                            embed = discord.Embed(title="You Lost", color=discord.Color.red())
                            embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                            embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                            await inter.response.edit_message(embed=embed, view=view2)
                            return

                        if dealer_total > 21:

                            embed = discord.Embed(title="You Won!", color=discord.Color.green())
                            embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                            embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                            await inter.response.edit_message(embed=embed, view=view2)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                            cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                            db.commit()
                            cursor.close()
                            db.close()
                            return

                        if dealer_total > 17:
                            if player_cards > dealer_total:
                                embed = discord.Embed(title="You Won!", color=discord.Color.green())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                                db.commit()
                                cursor.close()
                                db.close()
                                return
                            
                            if dealer_total > player_cards:
                                embed = discord.Embed(title="You Lost", color=discord.Color.red())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                return
                            
                            if dealer_total == player_cards:

                                embed = discord.Embed(title="You Tied", color=discord.Color.orange())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount, interaction.user.id))
                                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount} WHERE user_id = {interaction.user.id}")
                                db.commit()
                                cursor.close()
                                db.close()
                                return
                    except:
                        if dealer_total == 21:
                            embed = discord.Embed(title="You Lost", color=discord.Color.red())
                            embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                            embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                            await inter.response.edit_message(embed=embed, view=view2)
                            return

                        if dealer_total > 21:

                            embed = discord.Embed(title="You Won!", color=discord.Color.green())
                            embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                            embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                            await inter.response.edit_message(embed=embed, view=view2)
                            cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                            cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                            db.commit()
                            cursor.close()
                            db.close()
                            return

                        if dealer_total > 17:
                            if player_cards > dealer_total:
                                embed = discord.Embed(title="You Won!", color=discord.Color.green())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount * 2 , interaction.user.id))
                                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount * 2} WHERE user_id = {interaction.user.id}")
                                db.commit()
                                cursor.close()
                                db.close()
                                return
                            
                            if dealer_total > player_cards:
                                embed = discord.Embed(title="You Lost", color=discord.Color.red())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                return
                            
                            if dealer_total == player_cards:

                                embed = discord.Embed(title="You Tied", color=discord.Color.orange())
                                embed.add_field(name="Your Hand", value=f"🃏 {player_cards}", inline=False)
                                embed.add_field(name="Dealers hand", value=f"🃏 {dealer_total}")
                                await inter.response.edit_message(embed=embed, view=view2)
                                cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet + amount , interaction.user.id))
                                cursor.execute(f"UPDATE economy SET won_with_gambling = {won_with_gambling + amount} WHERE user_id = {interaction.user.id}")
                                db.commit()
                                cursor.close()
                                db.close()
                                return
                else:
                    await inter.response.send_message(f"You're not {interaction.user.mention}", ephemeral=True)
            stand.callback = stand_call


            db.commit()
            cursor.close()
            db.close()
            return
    
    @bj.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(bj(bot))