#Librarys
from pyrogram import Client,filters
import apis





# Bot initialization
bot = Client(
    apis.bot_name,
    api_id=apis.app_api_id,
    api_hash=apis.app_api_hash,
    bot_token=apis.bot_api_hash
    )


@bot.on_message()
async def main(cleint, message):
    await message.reply_text("hello world")


bot.run()