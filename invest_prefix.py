import discord
from discord.ext import commands
from discord.ui import View, Button
import sqlite3


class InvestPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases=["INVEST", "Invest"])
    @commands.guild_only()
    async def invest(self, ctx: commands.Context):
        try:
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            cursor1.execute(
                f"SELECT * FROM invest")
            data = cursor1.fetchone()

            prize = data[0]
            stamp = data[1]

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {ctx.author.id}")
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
                f"SELECT * FROM economy WHERE user_id = {ctx.author.id} AND guild_id={ctx.guild.id}")
            data = cursor2.fetchone()

            try:
                wallet = data[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, "
                                "guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, 0, 0, 0, 0, ctx.message.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"<t:{stamp + 5}:R> will the new stock prize we known",
                                color=discord.Color.blue(), timestamp=ctx.message.created_at)
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

            await ctx.send(embed=embed, view=view)

            async def buy_call(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

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
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?", ephemeral=True)

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
        
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.send(embed=embed)
    

    @commands.command(aliases=["Sell", "SELL"])
    @commands.guild_only()
    async def sell(self, ctx: commands.Context, amount: int = None):
        try:
            if amount is None:
                return await ctx.send("PLease give a valid number")
            
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            db2 = sqlite3.connect("economy.sqlite")
            cursor2 = db2.cursor()

            cursor2.execute(
                f"SELECT * from economy WHERE user_id = {ctx.author.id}"
            )
            data2 = cursor2.fetchone()
            try:
                wallet = data2[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, "
                                "guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {ctx.author.id}")
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
                return await ctx.send(f"You can't sell {amount:,} stock(s)")

            if data1 is None:
                return await ctx.send("You have no stock(s) to sell")

            if amount > stock_amount:
                return await ctx.send("You do not have that much stock(s)")

            yes = Button(label="Yes", style=discord.ButtonStyle.green)
            no = Button(label="No", style=discord.ButtonStyle.danger)

            view = View()
            view.add_item(yes)
            view.add_item(no)

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"Are you sure you want to sell "
                                f"**{amount:,}** stock(s) for **{stock_prize * amount:,}**?", color=discord.Color.orange())

            await ctx.send(embed=embed, view=view)

            async def yes_call(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{ctx.author.mention} just sold {amount:,} stock(s)"
                                                    f" for {stock_prize * amount:,}", color=discord.Color.green)

                    cursor1.execute("UPDATE stock SET amount = ? WHERE user_id = ?",
                                    (stock_amount - amount, ctx.author.id))
                    cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                    (wallet + amount * stock_prize, ctx.author.id))

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            yes.callback = yes_call

            async def no_call(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{ctx.author.mention} cancelled selling "
                                                    f"**{amount:,}** stock(s) for **{stock_prize * amount:,}**",
                                        color=discord.Color.green())

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            no.callback = no_call
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.send(embed=embed)


    @commands.command(aliases=["BUY", "Buy"])
    @commands.guild_only()
    async def buy(self, ctx: commands.Context, amount: int = None):
        try:
            if amount is None:
                return await ctx.send("PLease give a valid number")
            
            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            db2 = sqlite3.connect("economy.sqlite")
            cursor2 = db2.cursor()

            cursor2.execute(
                f"SELECT * from economy WHERE user_id = {ctx.author.id}"
            )
            data2 = cursor2.fetchone()
            try:
                wallet = data2[1]

            except:
                cursor2.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling,"
                                " guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                (ctx.author.id, 0, 0, 0, 0, ctx.guild.id, 0, 0))
                db2.commit()
                wallet = 0

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {ctx.author.id}")
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
                return await ctx.send(f"You can't buy {amount:,} stock(s)")

            if wallet < amount * stock_prize:
                return await ctx.send("You don't have enough money in your wallet")

            yes = Button(label="Yes", style=discord.ButtonStyle.green)
            no = Button(label="No", style=discord.ButtonStyle.danger)

            view = View()
            view.add_item(yes)
            view.add_item(no)

            embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                description=f"Are you sure you want to buy **{amount:,}** stock(s) for"
                                            f" **{stock_prize * amount:,}**?", color=discord.Color.orange())

            await ctx.send(embed=embed, view=view)

            async def yes_call(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{ctx.author.mention} just bought {amount:,} stock(s) "
                                                    f"for {stock_prize * amount:,}", color=discord.Color.green)

                    cursor1.execute("UPDATE stock SET amount = ? WHERE user_id = ?",
                                    (stock_amount + amount, ctx.author.id))
                    cursor2.execute("UPDATE economy SET wallet = ? WHERE user_id = ?",
                                    (wallet - amount * stock_prize, ctx.author.id))

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            yes.callback = yes_call

            async def no_call(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"You're not {ctx.author.mention}?")

                else:
                    embed = discord.Embed(title="HOLLAND CASINO STOCKS",
                                        description=f"{ctx.author.mention} cancelled buying **{amount:,}** stock(s) "
                                                    f"for **{stock_prize * amount:,}**", color=discord.Color.green())

                    await interaction.response.edit_message(embed=embed, view=None)
                    return

            no.callback = no_call
            
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InvestPrefix(bot))
