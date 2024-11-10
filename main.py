#Librarys
from pyrogram import Client,filters
import apis
from buttons import Buttons
from quesfuser import Response
from receivemedia import ReceiveMedia, SendMedia
from SQL.Sql import DatabaseManager



# Bot initialization
bot = Client(
    apis.bot_name,
    api_id=apis.app_api_id,
    api_hash=apis.app_api_hash,
    bot_token=apis.bot_api_hash
    )


# Database connection
db_manager = DatabaseManager(
    dbname='uploader_bot_telegram',
    user='postgres',
    password='12345',
    host='127.0.0.1',
    port='5432'
)

#Object button
buttons = Buttons()
#Object Response
response = Response()
#Object get medie 
receive_media = ReceiveMedia(bot, response, buttons)
#send media 
send_media = SendMedia(db_manager) 




@bot.on_message()
async def main(cleint, message):

    if message.text == 'میخوام فیلم آپلود کنم' and message.chat.id == 1655307519:
        await message.reply_text('''
            روش آپلودتو انتخاب کن 
            تکی یا دست جمعی
''', reply_markup=buttons.menu_selection())
    
    elif message.chat.id == 1655307519 :
        await message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_upload())


    # get movie 
    try:
        await send_media.send_medi(message.text[7:], message)
        print(message.text[7:])
    except:
        pass





@bot.on_callback_query()
async def hande_callback_query(client, callback_query):
    resulte_response = None # resulte response user 

    # upload one movie
    if callback_query.data == 'one_upload_movie':

        await callback_query.message.reply_text('فیلم مورد نظر خود را بفرس:')# send message for user 

        resulte_response = await response.respons_text(bot, 1655307519)# get response

        file_id =  await receive_media.get_one_media(resulte_response)#get vidio id 

        if file_id:
            db_manager.insert_path_link('0')
            path_link = db_manager.fetch_path_link()[0][0]
            db_manager.insert_path_media((file_id,path_link))
            await callback_query.message.reply_text(f'https://t.me/PajPajbot?start={path_link}', reply_markup=buttons.menu_upload())
        


    elif callback_query.data == 'collective_upload_movie':
        await callback_query.message.reply_text('''
    فیلم های مورد نضر خود رو وارد کن
    در آخر دکمه پایان را بزن
 ''', reply_markup=buttons.menu_end())
        




bot.run()