from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)



class Buttons:
    # menu button upload admin
    def menu_main(self):
        upload_button =  ReplyKeyboardMarkup(
            [
                ['میخوام فیلم آپلود کنم'],
                ['پیام دسته جمعی'],['استعلام تعداد کاربرها']
            ],resize_keyboard=True
        )

        return upload_button
    #menu end loop
    def menu_end(self):
        end_button= ReplyKeyboardMarkup(
            [
                ['پایان']
            ],resize_keyboard=True
        )
        return end_button
    # selection menu for upload movie
    def menu_selection(self):
        selection_button= InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('تکی', callback_data='one_upload_movie'),InlineKeyboardButton('دسته جمعی', callback_data='collective_upload_movie')]
            ]
        )
        return selection_button
    
    #menu join chanels 
    def menu_join_chanel(self):
        join_chanel_buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('🎬کانال اول', url="https://t.me/textchanell90")],
                [InlineKeyboardButton('🔞کانال دوم', url='https://t.me/fight_club_live')],
                
            ]
        )
        return join_chanel_buttons