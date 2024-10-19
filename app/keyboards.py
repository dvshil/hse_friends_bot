from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)




start_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Давай начнем😜')]], one_time_keyboard=True,
                           resize_keyboard=True)
group = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='КНТ-4')],
                                      [KeyboardButton(text='КНТ-5')],
                                      [KeyboardButton(text='КНТ-6')]],
                            one_time_keyboard=True, resize_keyboard=True)
