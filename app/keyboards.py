from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)




start_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Давай начнем😜')]], one_time_keyboard=True,
                           resize_keyboard=True)

start_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Моя анкета')],
                                        [KeyboardButton(text='Заполнить анкету')]],
                              one_time_keyboard=True, resize_keyboard=True)

group = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='КНТ-4')],
                                      [KeyboardButton(text='КНТ-5')],
                                      [KeyboardButton(text='КНТ-6')]],
                            one_time_keyboard=True, resize_keyboard=True)

action = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2'),
                                        KeyboardButton(text='3'), KeyboardButton(text='4')]],
                             one_time_keyboard=True, resize_keyboard=True)

regg = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Заполнить анкету')]],
                           one_time_keyboard=True, resize_keyboard=True)

profile_view = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='👍'),
                                             KeyboardButton(text='💌'),
                                   KeyboardButton(text='👎'),
                                              KeyboardButton(text='💤')]],
                                   resize_keyboard=True)

show_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='Да'), InlineKeyboardButton(text='Нет', callback_data='Нет')]
])

next_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Следующая анкета', callback_data='Да')]
])

sleep_mode = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1')]], resize_keyboard=True)