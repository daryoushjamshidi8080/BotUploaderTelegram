#Librarys
from pyrogram import Client,filters
import asyncio
import apis
from buttons import Buttons
from quesfuser import Response
from receivemedia import ReceiveMedia, SendMedia
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from  Sql import DatabaseManager

# Bot initialization
bot = Client(
    apis.bot_name,
    api_id=apis.app_api_id,
    api_hash=apis.app_api_hash,
    bot_token=apis.bot_api_hash
    )


# Database connection
db_manager = DatabaseManager(
    dbname='bot_uploader_telegram',
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


user_states = {}
list_file_id = []

notification = None
notif_join_channel = {} # dictionary save notification massage for join to channel


@bot.on_message(filters.command("start") and filters.private)
async def main(cleint, message):
    global user_states, list_file_id


        
    # Check if user is already in the database; if not, store their chat ID for the first interaction
    users = db_manager.fetch_user_id(message.chat.id)

    if not users:
        db_manager.insert_chat_id(message.chat.id)



    user_join_status = 0 # varibel for send not join to chanel user
    global notif_join_channel, notification


    user_id = message.from_user.id  # ID The user who sent the command
    chat_id = "@textchanell90", '@fight_club_live'  # Replace with channel username

    try:
        # get member of channel 
        member_one_channel = await bot.get_chat_member(chat_id[0], user_id)
        member_two_channel = await bot.get_chat_member(chat_id[1], user_id)


        if member_one_channel.status.name in['MEMBER', 'ADMINISTRATOR','OWNER'] and \
           member_two_channel.status.name in['MEMBER', 'ADMINISTRATOR','OWNER'] and \
            not(user_id in  [1655307519, 7221338346]):


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
    if user_join_status != 1 and not (message.chat.id in [1655307519, 7221338346]): 
        await message.reply_text(f'''
    برای استفاده از این ربات باید از لینک های
داخل کانال استفاده کنید
                                 
    برای سفارش ساخت ربات تلگرام به ایدی زیر پیام دهید
    اید: @D_jamshidi80_dev
''', reply_markup=buttons.menu_join_chanel())
        



    # send message for admin 


    if message.text == 'میخوام فیلم آپلود کنم' and message.chat.id in [1655307519, 7221338346]:
        notification =  await message.reply_text('''
            روش آپلودتو انتخاب کن 
            تکی یا دست جمعی
''', reply_markup=buttons.menu_selection())
    
    elif message.text == 'پیام دسته جمعی' and message.chat.id in [1655307519, 7221338346]:
        
        # Sending message to admin for initial prompt
        await bot.send_message(message.chat.id, "پیام خود را بفرستین")
        user_states[message.chat.id] = 'send_message'
        return



    elif message.text == 'استعلام تعداد کاربرها' and message.chat.id in [1655307519, 7221338346]:
        
        #fetch count users of database
        count = db_manager.fetch_count_users()
        #send message for admin 
        await message.reply_text(f'تعداد کاربرانی که از این ربات استفاده میکند {count}', reply_markup=buttons.menu_main())

    
    elif message.chat.id in [1655307519, 7221338346] and not(message.chat.id in user_states):
        await message.reply_text('چیکار کنم برات حاجی', reply_markup=buttons.menu_main())


    if message.chat.id in user_states :


        #get answer
        if user_states[message.chat.id] == 'send_message':
            # Fetching all chat IDs of users
            chat_id_all_users = db_manager.fetch_chat_id_all_user()

            # Sending the message to all users based on content type
            for chat_id_user in chat_id_all_users:
                if message.video:
                    await bot.send_video(chat_id_user[0], video=message.video.file_id, caption=message.caption)

                elif message.photo:
                    await bot.send_photo(chat_id_user[0], photo=message.photo.file_id, caption=message.caption)

                else:
                    await bot.send_message(chat_id_user[0], text=message.text)

            # Confirmation message to admin
            await bot.send_message(message.chat.id, "باموفقیت ارسال شد")
            
            # حذف کاربر از وضعیت
            del user_states[user_id]

            
            
        elif user_states[message.chat.id] == 'send_one_media':

            file_id =  await receive_media.get_one_media(message)#get vidio id 

            if file_id:
                db_manager.insert_path_link('0')
                path_link = db_manager.fetch_path_link()[0][0]
                db_manager.insert_path_media((file_id,path_link))
                await message.reply_text(f'''
                باموفقیت ذخیره شد 
                                                        
                https://t.me/PajPajbot?start={path_link}

    ''', reply_markup=buttons.menu_main())
                
                #send message for user
                await message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())

                
                 # حذف کاربر از وضعیت
                del user_states[user_id]
            else:

                await message.reply_text(
                    """
                    این فایل ویدیو نیست. یک ویدیو بفرستید
                    یا دکمه پایان رو بزنید.
                    """, 
                    reply_markup=buttons.menu_end()
                )
                if message.text == 'پایان':
                    del user_states[user_id]
                    await message.reply_text('اوکی اومدیم بیرون الان برات چیکار کنم ', reply_markup=buttons.menu_main())


        elif user_states[message.chat.id] == 'send_collective_media':

            

            file_id_list = await receive_media.get_one_media(message)


            if message.text == 'پایان' :

                if len(list_file_id) == 0:
                    del user_states[user_id]
                    await message.reply_text('اوکی اومدیم بیرون الان برات چیکار کنم ', reply_markup=buttons.menu_main())
                    return
                
                else:
                    db_manager.insert_path_link('0')
                    path_link = db_manager.fetch_path_link()[0][0]

                    for link in list_file_id :
                        db_manager.insert_path_media((link,path_link))

                    await message.reply_text(f'''
                    باموفقیت ذخیره شد 
                                                            
                    https://t.me/PajPajbot?start={path_link}

        ''', reply_markup=buttons.menu_main())
                    
                    #send message for user
                    await message.reply_text("میخوای چکار برات بکنم حاجی", reply_markup=buttons.menu_main())
                    del user_states[user_id]
                    list_file_id = []
                    return



            elif isinstance(file_id_list, str):
                
                list_file_id.append(file_id_list)
                await message.reply_text('ذخیره شد فیلم بعدی را ارسال کنید درصورت اتمام اپلود دکمه پایان رو بزنید', reply_markup=buttons.menu_end())

            elif file_id_list == None:

                await message.reply_text(
                """
                این فایل ویدیو نیست. یک ویدیو بفرستید
                یا دکمه پایان رو بزنید.
                اگر ویدیویی فرستادید ذخیره شده دکمه پیایان رو بزنید
                """, 
                reply_markup=buttons.menu_end()
            )
                
        


    



@bot.on_callback_query()
async def hande_callback_query(client, callback_query):
    resulte_response = None # resulte response user 
    global  notification
    # upload one movie
    if callback_query.data == 'one_upload_movie':
        await notification.delete()# delete menu


        user_states[callback_query.message.chat.id] = 'send_one_media'
        await callback_query.message.reply_text('فیلم مورد نظر خود را بفرس:', reply_markup=buttons.menu_end())# send message for user 
        return
        
            

    # get loop movie 
    elif callback_query.data == 'collective_upload_movie':
        
        await notification.delete()# delete menu
        user_states[callback_query.message.chat.id] = 'send_collective_media'
        
        notification = await callback_query.message.reply_text('فیلم مورد نظر خود را بفرس:', reply_markup=buttons.menu_end())# send message for user
        
        return
    


bot.run()