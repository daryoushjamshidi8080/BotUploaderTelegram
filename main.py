#Librarys
from pyrogram import Client,filters
import asyncio
import apis
from buttons import Buttons
from quesfuser import Response
from receivemedia import ReceiveMedia, SendMedia
from SQL.Sql import DatabaseManager
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus


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



notification = None
notif_join_channel = {} # dictionary save notification massage for join to channel


@bot.on_message(filters.command("start") and filters.private)
async def main(cleint, message):


        
    # Check if user is already in the database; if not, store their chat ID for the first interaction
    users = db_manager.fetch_file_id(message.chat.id)

    if not users:
        db_manager.insert_chat_id(message.chat.id)



    user_join_status = 0 # varibel for send not join to chanel user
    global notif_join_channel, notification


    user_id = message.from_user.id  # ID The user who sent the command
    chat_id = "@textchanell90", '@dj_vpn80'  # Replace with channel username

    try:
        # get member of channel 
        member_one_channel = await bot.get_chat_member(chat_id[0], user_id)
        member_two_channel = await bot.get_chat_member(chat_id[1], user_id)


        if member_one_channel.status.name in['MEMBER', 'ADMINISTRATOR','OWNER'] and \
           member_two_channel.status.name in['MEMBER', 'ADMINISTRATOR','OWNER'] and \
            not(user_id == 1655307519):


            # Delete notification for join to channel
            if str(user_id) in notif_join_channel:
                key = notif_join_channel[str(user_id)]
                await key.delete() # delete notification join to channel
                


            # get movie 
            if message.text[7:]:
                #send notification
                notification = await message.reply_text(''' 
                                                        فقط ۱۰ ثانیه وقت فرواید فیلم هارو داری 
                                                        
                                                        درصورت نیاز دوباره روی لینک بزنید''')
                
                await send_media.send_medi(message.text[7:], message) # send media 


                await asyncio.sleep(5) # time sleep
                await notification.delete()# delete notification

 

    except Exception as e:
        if "USER_NOT_PARTICIPANT" in str(e):
        
            message_join_channel = await message.reply_text("برای استفاده از ربات باید عضو کانال ها شوید",reply_markup=buttons.menu_join_chanel())
            notif_join_channel[str(user_id)] = message_join_channel
            user_join_status = 1
        else:
            await message.reply_text(f"An error occurred: {e}")

    
    
    # send message for user 
    if user_join_status != 1 and not (message.chat.id == 1655307519): 
        await message.reply_text(f'''
    برای استفاده از این ربات باید از لینک های
داخل کانال استفاده کنید
                                 
    برای سفارش ساخت ربات تلگرام به ایدی زیر پیام دهید
    اید: @D_jamshidi80_dev
''', reply_markup=buttons.menu_join_chanel())
        



    # send message for admin 


    if message.text == 'میخوام فیلم آپلود کنم' and message.chat.id == 1655307519:
        notification =  await message.reply_text('''
            روش آپلودتو انتخاب کن 
            تکی یا دست جمعی
''', reply_markup=buttons.menu_selection())
    
    elif message.text == 'پیام دسته جمعی' and message.chat.id ==  1655307519:
        pass
    elif message.text == 'استعلام تعداد کاربرها':
        count = db_manager.fetch_count_users()
        await message.reply_text(f'تعداد کاربرانی که از این ربات استفاده میکند {count}', reply_markup=buttons.menu_main())

    
    elif message.chat.id == 1655307519 :
        await message.reply_text('چیکار کنم برات حاجی', reply_markup=buttons.menu_main())







    





@bot.on_callback_query()
async def hande_callback_query(client, callback_query):
    resulte_response = None # resulte response user 
    global  notification
    # upload one movie
    if callback_query.data == 'one_upload_movie':
        await notification.delete()# delete menu

        await callback_query.message.reply_text('فیلم مورد نظر خود را بفرس:')# send message for user 
        
        resulte_response = await response.respons_text(bot, 1655307519)# get response
        
        file_id =  await receive_media.get_one_media(resulte_response)#get vidio id 

        if file_id:
            db_manager.insert_path_link('0')
            path_link = db_manager.fetch_path_link()[0][0]
            db_manager.insert_path_media((file_id,path_link))
            await callback_query.message.reply_text(f'''
            باموفقیت ذخیره شد 
                                                    
            https://t.me/PajPajbot?start={path_link}

''', reply_markup=buttons.menu_main())
            
            #send message for user
            await callback_query.message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())
    
        else :
            
            #send message for user
            await callback_query.message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())

            
        

    # get loop movie 
    elif callback_query.data == 'collective_upload_movie':

        await notification.delete()# delete menu
        
        notification = await callback_query.message.reply_text('فیلم مورد نظر خود را بفرس:')# send message for user 

        resulte_response = await response.respons_text(bot, 1655307519)# get response
        file_id_list = await receive_media.get_media_collective(resulte_response)
        
        if file_id_list :
            db_manager.insert_path_link('0')
            path_link = db_manager.fetch_path_link()[0][0]

            for link in file_id_list :
                db_manager.insert_path_media((link,path_link))

            await callback_query.message.reply_text(f'''
            باموفقیت ذخیره شد 
                                                    
            https://t.me/PajPajbot?start={path_link}

''', reply_markup=buttons.menu_main())
            
            #send message for user
            await callback_query.message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())
    
        else :
            
            #send message for user
            await callback_query.message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())

            
        



bot.run()