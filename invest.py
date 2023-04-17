from discord import app_commands
import discord
from discord.ext import commands
import sqlite3
from discord.ui import View, Button


class Invest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("invest.sqlite")
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS invest(
            stock_prize INTERGER, stamp INTERGER
            )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS stock(
            user_id INTERGER, amount INTERGER
            )""")


    @app_commands.command(name="invest", description="Details about HOLLAND CASINO stocks")
    async def invest(self, inter: discord.Interaction):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
            
        else:
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            cursor1.execute(
                f"SELECT * FROM invest")
            data = cursor1.fetchone()

            prize = data[0]
            stamp = data[1]

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {inter.user.id}")
            data = cursor1.fetchone()

            try:
                stock_amount = data[1]
            except:
                stock_amount = 0

            buy = Button(label="Buy stock", style=discord.ButtonStyle.green)
            sell = Button(label="Sell stock", style=discord.ButtonStyle.danger)

            view = View(timeout=120)
            view.add_item(buy)
            view.add_item(sell)

            db2 = sqlite3.connect("economy.sqlite")
            cursor2 = db2.cursor()

            cursor2.execute(
                f"SELECT * FROM economy WHERE user_id = {inter.user.id} AND guild_id={inter.guild.id}")
            data = cursor2.fetchone()

            try:
                wallet = data[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, "
                                "guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (inter.user.id, 0, 0, 0, 0, inter.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"<t:{stamp + 5}:R> will the new stock prize we known",
                                color=discord.Color.blue(), timestamp=inter.created_at)
            embed.add_field(name="Holland Casino stock prize:",
                            value=f"```c\n{prize:,}```", inline=False)
            
            embed.add_field(name="", value=f"You have {stock_amount:,} stock(s)", inline=False)

            if wallet < prize:
                buy.disabled = True
                embed.set_footer(text="Not enough money in wallet to buy stocks")

            if stock_amount < 1:
                sell.disabled = True
                embed.set_footer(text="No stocks to sell")

            if sell.disabled and buy.disabled:
                embed.set_footer(text="No stocks to sell or buy")

            await inter.response.send_message(embed=embed, view=view)

            async def buy_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{interaction.user} bought **Holland Casino** "
                                                    f"stocks for **{prize:,}** casino chips",
                                        color=discord.Color.green(), timestamp=interaction.created_at)

                    cursor1.execute(
                        f"SELECT * FROM stock WHERE user_id = {interaction.user.id}")
                    data1 = cursor1.fetchone()

                    if data1 is None:
                        cursor1.execute("INSERT INTO stock(user_id, amount) VALUES(?, ?)",
                                        (interaction.user.id, 1))
                        db1.commit()
                        cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                        (wallet - prize, interaction.user.id))
                        db2.commit()

                    else:
                        cursor1.execute(f"UPDATE stock SET amount = ? WHERE user_id = ?",
                                        (stock_amount + 1, interaction.user.id))
                        db1.commit()
                        cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                        (wallet - prize, interaction.user.id))
                        db2.commit()

                    await interaction.response.edit_message(embed=embed, view=None)

            buy.callback = buy_call

            async def sell_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?", ephemeral=True)

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{interaction.user} sold **Holland Casino** stocks "
                                                    f"for **{prize:,}** casino chips",
                                        color=discord.Color.green(), timestamp=interaction.created_at)

                    cursor1.execute(f"UPDATE stock SET amount = ? WHERE user_id = ?",
                                    (stock_amount - 1, interaction.user.id))
                    db1.commit()
                    cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                    (wallet + prize, interaction.user.id))
                    db2.commit()

                    await interaction.response.edit_message(embed=embed, view=None)

            sell.callback = sell_call

            db1.commit()
            db2.commit()
            return

    @invest.error
    async def on_invest_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sell-stock", description="Sell HOLLAND CASINO stocks")
    async def stock_sell(self, inter: discord.Interaction, amount: int):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
            
        else:
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            db2 = sqlite3.connect("economy.sqlite")
            cursor2 = db2.cursor()

            cursor2.execute(
                f"SELECT * from economy WHERE user_id = {inter.user.id}"
            )
            data2 = cursor2.fetchone()
            try:
                wallet = data2[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, "
                                "guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (inter.user.id, 0, 0, 0, 0, inter.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {inter.user.id}")
            data1 = cursor1.fetchone()
            
            try:
                stock_amount = data1[1]
                
            except:
                stock_amount = 0

            cursor1.execute(
                f"SELECT * FROM invest")
            data = cursor1.fetchone()
            
            try:
                stock_prize = data[0]
                
            except:
                stock_prize = 0

            if amount < 1:
                return await inter.response.send_message(f"You can't sell {amount:,} stock(s)")

            if data1 is None:
                return await inter.response.send_message("You have no stock(s) to sell")

            if amount > stock_amount:
                return await inter.response.send_message("You do not have that much stock(s)")

            yes = Button(label="Yes", style=discord.ButtonStyle.green)
            no = Button(label="No", style=discord.ButtonStyle.danger)

            view = View()
            view.add_item(yes)
            view.add_item(no)

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"Are you sure you want to sell "
                                f"**{amount:,}** stock(s) for **{stock_prize * amount:,}**?", color=discord.Color.orange())

            await inter.response.send_message(embed=embed, view=view)

            async def yes_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{inter.user.mention} just sold {amount:,} stock(s)"
                                                    f" for {stock_prize * amount:,}", color=discord.Color.green())

                    cursor1.execute("UPDATE stock SET amount = ? WHERE user_id = ?",
                                    (stock_amount - amount, inter.user.id))
                    cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                    (wallet + amount * stock_prize, inter.user.id))

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            yes.callback = yes_call

            async def no_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{inter.user.mention} cancelled selling "
                                                    f"**{amount:,}** stock(s) for **{stock_prize * amount:,}**",
                                        color=discord.Color.green())

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            no.callback = no_call

    @stock_sell.error
    async def on_stock_sell_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy-stock", description="Buy HOLLAND CASINO stocks")
    async def stock_buy(self, inter: discord.Interaction, amount: int):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
            
        else:
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            db2 = sqlite3.connect("economy.sqlite")
            cursor2 = db2.cursor()

            cursor2.execute(
                f"SELECT * from economy WHERE user_id = {inter.user.id}"
            )
            data2 = cursor2.fetchone()
            try:
                wallet = data2[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling,"
                                " guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (inter.user.id, 0, 0, 0, 0, inter.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {inter.user.id}")
            data1 = cursor1.fetchone()
            
            try:
                stock_amount = data1[1]
                
            except:
                stock_amount = 0

            cursor1.execute(
                f"SELECT * FROM invest")
            data = cursor1.fetchone()
            
            try:
                stock_prize = data[0]
                
            except:
                stock_prize = 0

            if amount < 1:
                return await inter.response.send_message(f"You can't buy {amount:,} stock(s)")

            if wallet < amount * stock_prize:
                return await inter.response.send_message("You don't have enough money in your wallet")

            yes = Button(label="Yes", style=discord.ButtonStyle.green)
            no = Button(label="No", style=discord.ButtonStyle.danger)

            view = View()
            view.add_item(yes)
            view.add_item(no)

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"Are you sure you want to buy **{amount:,}** stock(s) for"
                                            f" **{stock_prize * amount:,}**?", color=discord.Color.orange())

            await inter.response.send_message(embed=embed, view=view)

            async def yes_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{inter.user.mention} just bought {amount:,} stock(s) "
                                                    f"for {stock_prize * amount:,}", color=discord.Color.green())

                    cursor1.execute("UPDATE stock SET amount = ? WHERE user_id = ?",
                                    (stock_amount + amount, inter.user.id))
                    cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                    (wallet - amount * stock_prize, inter.user.id))

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            yes.callback = yes_call

            async def no_call(interaction: discord.Interaction):
                if interaction.user.id != inter.user.id:
                    await interaction.response.send_message(f"You're not {inter.user.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{inter.user.mention} cancelled buying **{amount:,}** stock(s)"
                                                    f"for **{stock_prize * amount:,}**", color=discord.Color.green())

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            no.callback = no_call

    @stock_buy.error
    async def on_stock_buy_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Invest(bot))
