#Librarys
from pyrogram import Client,filters
import apis
from buttons import Buttons
from quesfuser import Response



# Bot initialization
bot = Client(
    apis.bot_name,
    api_id=apis.app_api_id,
    api_hash=apis.app_api_hash,
    bot_token=apis.bot_api_hash
    )

#Object button
buttons = Buttons()
#Object Response
response = Response()

@bot.on_message()
async def main(cleint, message):

    if message.text == 'میخوام فیلم آپلود کنم' and message.chat.id == 1655307519:
        await message.reply_text('''
            روش آپلودتو انتخاب کن 
            تکی یا دست جمعی
''', reply_markup=buttons.menu_selection())
    
    elif message.chat.id == 1655307519 :
        await message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_upload())




@bot.on_callback_query()
async def hande_callback_query(client, callback_query):


    # upload one movie
    if callback_query.data == 'one_upload_movie':
        await callback_query.message.reply_text('اسم جدید را بفرستید')
        resulte_response = await response.respons_text(bot, 1655307519)
        print(resulte_response)

    elif callback_query.data == 'collective_upload_movie':
        await callback_query.message.reply_text('آپلود دسته جمعی')

        




bot.run()