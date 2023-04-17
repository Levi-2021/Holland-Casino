import discord
from discord.ext import commands
from discord.ui import View, Select


class HelpPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx:commands.Context):
        try:      
            select_games = Select(
                            placeholder="🎮 Games",
                            options=[
                                discord.SelectOption(label="/tic-tac-toe (without economy)"),
                                discord.SelectOption(label="/baccarat (with economy)"),
                                discord.SelectOption(label="/black-Jack (with economy)"),
                                discord.SelectOption(label="/high-Low (with economy)"),
                                discord.SelectOption(label="/horse-racing (with economy)"),
                                discord.SelectOption(label="/roulette (with economy)"),
                                discord.SelectOption(label="/rps (against bot or user without economy)"),
                                discord.SelectOption(label="/slot (with economy)")
                            ])

            select_economy = Select(
                            placeholder="💸 Economy",
                            options=[
                                discord.SelectOption(label="/balance"),
                                discord.SelectOption(label="/baccarat"),
                                discord.SelectOption(label="/black-Jack"),
                                discord.SelectOption(label="/high-low"),
                                discord.SelectOption(label="/horse-racing"),
                                discord.SelectOption(label="/roulette"),
                                discord.SelectOption(label="/slot"),
                                discord.SelectOption(label="/profile"),
                                discord.SelectOption(label="/withdraw"),
                                discord.SelectOption(label="/deposit"),
                                discord.SelectOption(label="/daily"),
                                discord.SelectOption(label="/hourly"),
                                discord.SelectOption(label="/leaderboard"),
                                discord.SelectOption(label="/give"),
                                discord.SelectOption(label="/invest"),
                                discord.SelectOption(label="/buy-stock"),
                                discord.SelectOption(label="/sell-stock"),
                                discord.SelectOption(label="/vote"),
                            ])
            select_general = Select(
                            placeholder="🛡️ General",
                            options=[
                                discord.SelectOption(label="/member-count"),
                                discord.SelectOption(label="/avatar"),
                                discord.SelectOption(label="/ping"),
                                discord.SelectOption(label="/stored-data"),
                                discord.SelectOption(label="/delete-data"),
                                discord.SelectOption(label="/add-emoji"),
                                discord.SelectOption(label="/vote"),
                            ])

            async def games_call(interaction:discord.Interaction):
                    if select_games.values[0] == "/tic-tac-toe (without economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/tic-tac-toe`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/tic-tac-toe [idOrMention]```", inline=False)
                        embed.add_field(name="Description", value="Play tic tac toe with a friend", inline=False)
                        embed.add_field(name="Prefix", value="`/`", inline=False)
                        embed.add_field(name="Example", value="```/tic-tac-toe @l3vi#7164 \n/tic-tac-toe 708686503873609751```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/baccarat (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/baccarat`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/baccarat [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play a game of baccarat", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino| / `", inline=False)
                        embed.add_field(name="Example", value="```/baccarat 200 \n@Holland Casino baccarat all \n@Holland Casino bac half```", inline=False)
                        embed.add_field(name="Aliases", value="`bac` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/black-Jack (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/black-Jack`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/black-Jack [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play black jack and win up to 2x", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | / `", inline=False)
                        embed.add_field(name="Example", value="```/black-Jack 200 \n@Holland Casino blackjack all \n@Holland Casino bj half```", inline=False)
                        embed.add_field(name="Aliases", value="`bj` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/high-Low (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/high-Low`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/high-Low [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Guess if the number is higher or lower than 5", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/high-Low 200 \n@Holland Casino highLow all \n@Holland Casino hl half```", inline=False)
                        embed.add_field(name="Aliases", value="`hl` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/horse-racing (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/horse-racing`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/horse-racing [<amount> <horseNum>]```", inline=False)
                        embed.add_field(name="Description", value="Bet on a horse race", inline=False)
                        embed.add_field(name="Prefix", value="`/`", inline=False)
                        embed.add_field(name="Example", value="```/high-Low 200 5 \n/high-Low 4892 2```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        
                    if select_games.values[0] == "/roulette (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/roulette`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/roulette [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play roulette and win up to 36x", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/roulette 200  \n@Holland Casino roulette all \n @Holland Casino rl half```", inline=False)
                        embed.add_field(name="Aliases", value="`rl`(only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/rps (against bot or user without economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/rps`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/rps [idOrMention]```", inline=False)
                        embed.add_field(name="Description", value="Play rock paper scissors against a friend or the bot", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/rps 708686503873609751 \n/rps @l3vi#7164 \n@Holland Casino rps @l3vi#7164 \n@Holland Casino rps 708686503873609751```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_games.values[0] == "/slot (with economy)":
                        embed = discord.Embed(title="", description="**Help command for: `/slot`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/slot [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Slot your money", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/slot 500 \n@Holland Casino gamble 200```", inline=False)
                        embed.add_field(name="Aliases", value="`gamble` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    
            select_games.callback = games_call
                
            async def economy_call(interaction:discord.Interaction):
                    if select_economy.values[0] == "/balance":
                        embed = discord.Embed(title="", description="**Help command for: `/balance`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/balance [idOrMention]```", inline=False)
                        embed.add_field(name="Description", value="Check your balance", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/balance \n@Holland Casino balance \n @Holland Casino bal```", inline=False)
                        embed.add_field(name="Aliases", value="`bal` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/baccarat":
                        embed = discord.Embed(title="", description="**Help command for: `/baccarat`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/baccarat [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play a game of baccarat", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/baccarat 200 \n@Holland Casino baccarat all \n@Holland Casino bac half```", inline=False)
                        embed.add_field(name="Aliases", value="`bac` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/black-Jack":
                        embed = discord.Embed(title="", description="**Help command for: `/black-Jack`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/black-Jack [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play black jack and win up to 2x", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/black-Jack 200 \n@Holland Casino blackjack all \n@Holland Casino bj half```", inline=False)
                        embed.add_field(name="Aliases", value="`bj` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/high-low":
                        embed = discord.Embed(title="", description="**Help command for: `/high-Low`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/high-Low [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Guess if the number is higher or lower than 5", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/high-Low 200 \n@Holland Casino highLow all \n@Holland Casino hl half```", inline=False)
                        embed.add_field(name="Aliases", value="`hl` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/horse-racing":
                        embed = discord.Embed(title="", description="**Help command for: `/horse-racing`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/horse-racing [<amount> <horseNum>]```", inline=False)
                        embed.add_field(name="Description", value="Bet on a horse race", inline=False)
                        embed.add_field(name="Prefix", value="`/`", inline=False)
                        embed.add_field(name="Example", value="```/high-Low 200 5 \n/high-Low 4892 2```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        
                    if select_economy.values[0] == "/roulette":
                        embed = discord.Embed(title="", description="**Help command for: `/roulette`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/roulette [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Play roulette and win up to 36x", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/roulette 200  \n@Holland Casino roulette all \n @Holland Casino rl half```", inline=False)
                        embed.add_field(name="Aliases", value="`rl`(only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/slot":
                        embed = discord.Embed(title="", description="**Help command for: `/slot`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/slot [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Slot your money", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/slot 500 \n@Holland Casino gamble 200```", inline=False)
                        embed.add_field(name="Aliases", value="`gamble` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/profile":
                        embed = discord.Embed(title="", description="**Help command for: `/profile`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/profile [idOrMention]```", inline=False)
                        embed.add_field(name="Description", value="Check your profile", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/profile \n@Holland Casino profile 708686503873609751```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/withdraw":
                        embed = discord.Embed(title="", description="**Help command for: `/withdraw`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/withdraw [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Withdraw your money", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/withdraw 500 \n@Holland Casino with all```", inline=False)
                        embed.add_field(name="Aliases", value="`with` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/deposit":
                        embed = discord.Embed(title="", description="**Help command for: `/deposit`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/deposit [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Deposit your money", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/deposit 500 \n@Holland Casino dep all```", inline=False)
                        embed.add_field(name="Aliases", value="`dep` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/daily":
                        embed = discord.Embed(title="", description="**Help command for: `/daily`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/daily```", inline=False)
                        embed.add_field(name="Description", value="Collect daily casino chips", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/daily-chips \n@Holland Casino daily```", inline=False)
                        embed.add_field(name="Aliases", value="`daily` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/hourly":
                        embed = discord.Embed(title="", description="**Help command for: `/hourly`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/hourly```", inline=False)
                        embed.add_field(name="Description", value="Collect hourly casino chips", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/hourly-chips \n@Holland Casino hourly```", inline=False)
                        embed.add_field(name="Aliases", value="`hourly` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/leaderboard":
                        embed = discord.Embed(title="", description="**Help command for: `/leaderboard`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/leaderboard [<type> <server>]```", inline=False)
                        embed.add_field(name="Description", value="Display the top 10 user", inline=False)
                        embed.add_field(name="Prefix", value="`/`", inline=False)
                        embed.add_field(name="Example", value="```/leaderboard Profit This server \n/leaderboard Pocket Chips all servers```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        
                    if select_economy.values[0] == "/give":
                        embed = discord.Embed(title="", description="**Help command for: `/give`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/give [<amount> idOrMention]```", inline=False)
                        embed.add_field(name="Description", value="Give someone your money (20% tax)", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/give 200 708686503873609751 \n@Holland Casino send 200 708686503873609751```", inline=False)
                        embed.add_field(name="Aliases", value="`send` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/invest":
                        embed = discord.Embed(title="", description="**Help command for: `/invest`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/invest```", inline=False)
                        embed.add_field(name="Description", value="Details about HOLLAND CASINO stocks", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/invest \n@Holland Casino invest```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/sell-stock":
                        embed = discord.Embed(title="", description="**Help command for: `/sell-stock`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/sell-stock [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Sell HOLLAND CASINO stocks", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/sell-stock 5\n@Holland Casino sell 3```", inline=False)
                        embed.add_field(name="Aliases", value="`sell` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/buy-stock":
                        embed = discord.Embed(title="", description="**Help command for: `/buy-stock`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/buy-stock [<amount>]```", inline=False)
                        embed.add_field(name="Description", value="Buy HOLLAND CASINO stocks", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/buy-stock 5\n@Holland Casino buy 3```", inline=False)
                        embed.add_field(name="Aliases", value="`buy` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_economy.values[0] == "/vote":
                        embed = discord.Embed(title="", description="**Help command for: `/vote`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/vote```", inline=False)
                        embed.add_field(name="Description", value="Vote for the bot on top.gg", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/vote \n@Holland Casino vote```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        
            select_economy.callback = economy_call
                    
            async def general_call(interaction:discord.Interaction):
                    if select_general.values[0] == "/member-count":
                        embed = discord.Embed(title="", description="**Help command for: `/member-count`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/member-count ```", inline=False)
                        embed.add_field(name="Description", value="Shows the member count of the server", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/member-count \n@Holland Casino mb ```", inline=False)
                        embed.add_field(name="Aliases", value="`mb` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_general.values[0] == "/avatar":
                        embed = discord.Embed(title="", description="**Help command for: `/avatar`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/avatar [idOrMention] ```", inline=False)
                        embed.add_field(name="Description", value="Shows the avatar of the user", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/avatar 708686503873609751 \n@Holland Casino av ```", inline=False)
                        embed.add_field(name="Aliases", value="`av` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_general.values[0] == "/ping":
                        embed = discord.Embed(title="", description="**Help command for: `/ping`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/ping```", inline=False)
                        embed.add_field(name="Description", value="Shows the latency of the bot", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/ping \n@Holland Casino pong ```", inline=False)
                        embed.add_field(name="Aliases", value="`pong` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_general.values[0] == "/stored-data":
                        embed = discord.Embed(title="", description="**Help command for: `/stored-data`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/stored-data```", inline=False)
                        embed.add_field(name="Description", value="Display all stored data the bot has from you (via DM's)", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/stored-data \n@Holland Casino data ```", inline=False)
                        embed.add_field(name="Aliases", value="`data` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                        
                    if select_general.values[0] == "/delete-data":
                        embed = discord.Embed(title="", description="**Help command for: `/delete-data`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/delete-data```", inline=False)
                        embed.add_field(name="Description", value="Delete all data that the bot has from you", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/delete-data \n@Holland Casino delete ```", inline=False)
                        embed.add_field(name="Aliases", value="`delete` (only with `@Holland Casino` prefix)", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_general.values[0] == "/add-emoji":
                        embed = discord.Embed(title="", description="**Help command for: `/add-emoji`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/add-emoji [<url> <name>]```", inline=False)
                        embed.add_field(name="Description", value="Adds an emoji to the server (Manage emojis And Stickers required)", inline=False)
                        embed.add_field(name="Prefix", value="`/`", inline=False)
                        embed.add_field(name="Example", value="```/add-emoji https://cool_guy.com cool_guy \n/add-emoji https://bad_guy.com bad_guy```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)

                    if select_general.values[0] == "/vote":
                        embed = discord.Embed(title="", description="**Help command for: `/vote`**", color=discord.Color.blue())
                        embed.add_field(name="Usage", value="```/vote```", inline=False)
                        embed.add_field(name="Description", value="Vote for the bot on top.gg", inline=False)
                        embed.add_field(name="Prefix", value="`@Holland Casino | /`", inline=False)
                        embed.add_field(name="Example", value="```/vote \n@Holland Casino vote```", inline=False)
                        embed.add_field(name="Aliases", value="`None`", inline=False)
                        
                        await interaction.response.send_message(embed=embed, view=None, ephemeral=True)
                    
                    
            select_general.callback = general_call
                

            view = View(timeout=None)
            view.add_item(select_games)
            view.add_item(select_economy)
            view.add_item(select_general)

            embed = discord.Embed(title="Holland Casino Help Page", description="In order to use the **Holland Casino** bot, use the **slash commands** or **mention the bot** followed by the command name!", color=discord.Color.blue())
            embed.add_field(name="Links", value="[Invite](https://discord.com/api/oauth2/authorize?client_id=1086017756719226890&permissions=52224&scope=bot) • [Support](https://discord.gg/EhEGmegRQd) • [Github](https://github.com/Levi-2021/Holland-Casino) • [Top GG](https://top.gg/bot/1086017756719226890)", inline=False)
            await ctx.reply(embed=embed, view=view)
        
        except Exception as e:
            embed = discord.Embed(title="Error ❌", description=f"**Unknown error detected**\n {e} \n**Please report this error in the [Support Server](https://discord.gg/EhEGmegRQd)**", color=discord.Color.red())
            return await ctx.send(embed=embed)
            

async def setup(bot):
    await bot.add_cog(HelpPrefix(bot))
