from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)



class Buttons:
    # menu button upload admin
    def menu_upload(self):
        upload_button =  ReplyKeyboardMarkup(
            [
                ['میخوام فیلم آپلود کنم']
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