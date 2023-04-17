from discord.ext import commands
import sqlite3


class setup_database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS streak(
            user_id INTERGER, vote_streak INTERGER, stamp INTERGER
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS economy(
            user_id INTERGER, wallet INTERGER, bank INTERGER, spend_on_gambling INTERGER, won_with_gambling INTERGER, guild_id INTERGER, net INTERGER, profit INTERGER
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS timestamps(
            user_id INTERGER, daily_stamp INTERGER, hourly_stamp INTERGER
        )""")
        
        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (100000000, 708686503873609751))
        db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author = message.author
        db = sqlite3.connect("economy.sqlite")
        cursor = db.cursor()

        cursor.execute(
            f"SELECT user_id FROM economy WHERE user_id = {author.id} AND guild_id = {message.guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO economy(user_id, wallet, bank, spend_on_gambling, won_with_gambling, guild_id, net, profit) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                           (author.id, 0, 0, 0, 0, message.guild.id, 0, 0))

        cursor.execute(
            f"SELECT user_id FROM timestamps WHERE user_id = {author.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO timestamps(user_id, daily_stamp, hourly_stamp) VALUES(?, ?, ?)",
                            (author.id, 0, 0))

        cursor.execute(
            f"SELECT * FROM economy WHERE user_id = {author.id}")
        data = cursor.fetchone()


        wallet = data[1]
        bank = data[2]
        spend = data[3]
        won = data[4]

        cursor.execute("UPDATE economy SET net = ? WHERE user_id = ?", (wallet + bank, author.id))

        cursor.execute("UPDATE economy SET profit = ? WHERE user_id = ?", (won - spend, author.id))

        cursor.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet, author.id))

        cursor.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank, author.id))
        
        cursor.execute("UPDATE economy SET spend_on_gambling = ? WHERE user_id = ?", (spend, author.id))

        cursor.execute("UPDATE economy SET won_with_gambling = ? WHERE user_id = ?", (won, author.id))
        
        
        db.commit()
        cursor.close()
        db.close()


async def setup(bot):
    await bot.add_cog(setup_database(bot))
