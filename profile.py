import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Check your profile")
    async def profile(self, inter:discord.Interaction, member:discord.Member=None):
        if inter.guild == None:
                embed = discord.Embed(title="Error ❌", description="Unable to respond to commands in DM's", color=discord.Color.red())
                return await inter.response.send_message(embed=embed)
        else:
                
            if member == None:
                member = inter.user

            db1 = sqlite3.connect("invest.sqlite")
            cursor1 = db1.cursor()

            cursor1.execute(
                f"SELECT * FROM stock WHERE user_id = {member.id}")
            data = cursor1.fetchone()
            
            if data is None:
                stock_amount = 0
                
            else:
                stock_amount = data[1]
            
            db = sqlite3.connect("economy.sqlite")
            cursor = db.cursor()

            cursor.execute(
                f"SELECT * FROM economy WHERE user_id = {member.id} AND guild_id={inter.guild.id}")
            data = cursor.fetchone()

            try:
                wallet = data[1]
                bank = data[2]
                spend = data[3]
                won = data[4]
                profit = data[7]

            except:
                cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (member.id, 0, 0, 0, 0, inter.guild.id, 0, 0))
                db.commit()
                wallet = 0
                bank = 0
                spend = 0
                won = 0
                profit = 0

            net = bank + wallet
            
            user_data = {  
                    "name": f"{member.name}#{member.discriminator}",  
                    "display_name": f"```c\n{member.display_name}```",
                    "spend":f"```c\n{spend:,}```",
                    "won": f"```c\n{won:,}```",
                    "profits": f"```c\n{profit:,}```",
                    "net": f"```c\n{net:,}```",
                    "stock": f"```c\n{stock_amount:,}```"
                }

            # background = Editor(Canvas((900, 700), color="#23272A"))
            # profile_image = await load_image_async(str(member.display_avatar.url))

            # card_right_shape = [(600, 0), (750, 700), (900, 700), (900, 0)]
            # background.polygon(card_right_shape, "#2C2F33")

            # coin_image = Editor("pictures/Holland_casino.png").resize((150, 150)).circle_image()
            # background.paste(coin_image, (720, 30))

            # poppins = Font.montserrat(size=40)
            # poppins_small = Font.montserrat(size=30)
            # poppins_small2 = Font.montserrat(size=20)

            # profile = Editor(profile_image).resize((150, 150)).circle_image()
            # background.paste(profile, (30, 30))

            # background.rectangle((30, 230), width=500, height=50, fill="#494b4f", radius=10)
            # background.rectangle((30, 325), width=530, height=50, fill="#494b4f", radius=10)
            # background.rectangle((30, 420), width=570, height=50, fill="#494b4f", radius=10)
            # background.rectangle((30, 515), width=590, height=50, fill="#494b4f", radius=10)
            # background.rectangle((30, 610), width=625, height=50, fill="#494b4f", radius=10)

            # if len(user_data["name"]) > 20:
            #     background.text((200, 40), user_data["name"], font=poppins_small2, color="white")

            # else:
            #     background.text((200, 40), user_data["name"], font=poppins, color="white")

            # if member.name == member.display_name:
            #     background.text(
            #         (200, 125), 
            #         f"AKA : None", 
            #         font=poppins_small2,
            #         color="white"
            #         )
            # else:
            #     background.text(
            #         (200, 125), 
            #         f"AKA : {user_data['display_name']}", 
            #         font=poppins_small2,
            #         color="white"
            #         )

            # background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
            
            # background.text(
            #     (40, 245),
            #     f"Profits : {user_data['profits']}",
            #     font=poppins_small,
            #     color="white"
            # )

            # background.text(
            #     (40, 340),
            #     f"Amount Won : {user_data['won']}",
            #     font=poppins_small,
            #     color="white"
            # )

            # background.text(
            #     (40, 435),
            #     f"Amount Spend : {user_data['spend']}",
            #     font=poppins_small,
            #     color="white"
            # )

            # background.text(
            #     (40, 530),
            #     f"Total Casino Chips : {user_data['net']}",
            #     font=poppins_small,
            #     color="white"
            # )

            # background.text(
            #     (40, 625),
            #     f"Holland Casino Stock(s) : {user_data['stock']}",
            #     font=poppins_small,
            #     color="white"
            # )

            # file = discord.File(fp=background.image_bytes,
            #                         filename=f"profile_{member.name}#{member.discriminator}.png")
            # await inter.response.send_message(file=file)
            
            embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s profile", color=discord.Color.blue())
            embed.add_field(name="Profits:", value=f"{user_data['profits']}", inline=False)
            embed.add_field(name="Amount Won:", value=f"{user_data['won']}", inline=False)
            embed.add_field(name="Amount Spend:", value=f"{user_data['spend']}", inline=False)
            embed.add_field(name="Total Casino Chips:", value=f"{user_data['net']}", inline=False)
            embed.add_field(name="Holland Casino Stock(s):", value=f"{user_data['stock']}", inline=False)
            
            await inter.response.send_message(embed=embed)

    @profile.error
    async def on_add_emoji_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {error} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(profile(bot))