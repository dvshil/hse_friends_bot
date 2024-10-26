from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.orm import AsyncORM

import app.keyboards as kb



router = Router()



class Register(StatesGroup):
    tg_id = State()
    name = State()
    age = State()
    birthday = State()
    zodiac = State()
    group = State()
    hobbies = State()
    contact = State()
    photo_id = State()




@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Я помогу найти тебе друзей😇', reply_markup=kb.start_1)


@router.message(F.text == 'Моя анкета')
async def output_profile(message: Message):
    data = await AsyncORM.send_user_profile(int(message.chat.id))
    if data:
        user_dto = data[0].model_dump()
        await message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                                       f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n{user_dto["hobbies"]}\n'
                                                                       f'{user_dto["group"]}\n{user_dto["contact"]}')
        await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                             '4.Изменить текст анкеты.', reply_markup=kb.action)
    else:
        await message.answer('Вы еще не добавляли свою анкету. Предлагаю это исправить ;)',
                             reply_markup=kb.regg)


@router.message(F.text == 'Давай начнем😜')
async def output_or_fill(message: Message):
    await message.answer('Предлагаю посмотреть твою анкету или заполнить, если её еще нет :)',
                         reply_markup=kb.start_2)


@router.message(Command('myprofile'))
async def my_profile(message: Message):
    await output_profile(message)


@router.message(F.text == 'Заполнить анкету')
async def reg_start(message: Message, state: FSMContext):
    await state.set_state(Register.tg_id)
    await state.update_data(tg_id=int(message.chat.id))
    await state.set_state(Register.name)
    await message.answer('Введи фамилию и имя', reply_markup=ReplyKeyboardRemove())


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Сколько тебе лет?')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    if str(message.text).isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Register.birthday)
        await message.answer('Укажи дату рождения')
    else:
        await message.answer('Попробуй еще раз')


@router.message(Register.birthday)
async def register_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await state.set_state(Register.zodiac)
    await message.answer('Кто ты по знаку зодиака?')


@router.message(Register.zodiac)
async def register_zodiac(message: Message, state: FSMContext):
    await state.update_data(zodiac=message.text)
    await state.set_state(Register.group)
    await message.answer('Из какой ты группы?', reply_markup=kb.group)

@router.message(Register.group)
async def register_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Register.hobbies)
    await message.answer('Расскажи о себе и кого хочешь найти',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Register.hobbies)
async def register_hobbies(message: Message, state: FSMContext):
    await state.update_data(hobbies=message.text)
    await state.set_state(Register.contact)
    await message.answer('Введи свой username в телеграмме в формате @user')

@router.message(Register.contact)
async def register_contact(message: Message, state: FSMContext):
    if str(f"@{message.chat.username}") == str(message.text):
        await state.update_data(contact=message.text)
        await state.set_state(Register.photo_id)
        await message.answer('Теперь пришли фото')
    else:
        await message.answer('Такого username не существует! Попробуй снова')

@router.message(Register.photo_id, F.photo)
async def register_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Фото загружено')
    await message.answer('Так выглядит твоя анкета:')
    data = await state.get_data()

    # curr = await AsyncORM.insert_users(str(data["contact"]))
    # pk = curr[0].model_dump()

    await AsyncORM.insert_profiles(str(data["name"]), int(data["age"]), str(data["birthday"]), str(data["zodiac"]),
                                   str(data["group"]),
                                   str(data["hobbies"]), str(data["contact"]), str(data["photo_id"]), int(data["tg_id"]))
    await message.answer_photo(photo=data["photo_id"], caption=f'{data["name"]}, '
                                                            f'{data["age"]} лет\n{data["birthday"]}, {data["zodiac"]}\n'
                                                               f'{data["hobbies"]}\n'
                                                            f'{data["group"]}')
    await state.clear()

    await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                         '4.Изменить текст анкеты.', reply_markup=kb.action)

@router.message(Register.photo_id, ~F.photo)
async def form_photo(message: Message, state: FSMContext):
    await message.answer('Отправь фото!')



@router.callback_query(F.data == 'Да')
async def yes(callback: CallbackQuery):
    await callback.answer('got you')
    # передать в функцию первичный ключ
    get_pk = await AsyncORM.getting_pk(int(callback.from_user.id))
    pk_dto = get_pk[0].model_dump()
    pk = pk_dto["id"]

    get_like_id = await AsyncORM.getting_like_id(int(pk))
    like_id_dto = get_like_id[0].model_dump()
    like_id = like_id_dto["like_id"]

    data = await AsyncORM.convert_likes_to_dto(int(like_id))
    if len(data) > 1:

        user_dto = data[0].model_dump()

        await callback.message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                                                f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n'
                                                                                f'{user_dto["hobbies"]}\n'
                                                                                f'{user_dto["group"]}\n{user_dto["contact"]}')
        await callback.message.answer('Приятного общения!', reply_markup=kb.next_user)

        await AsyncORM.remove_one_like(int(pk), int(user_dto["user_id"]))

    else:
        user_dto = data[0].model_dump()

        await callback.message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                                                f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n'
                                                                                f'{user_dto["hobbies"]}\n'
                                                                                f'{user_dto["group"]}\n{user_dto["contact"]}')
        await callback.message.answer('Приятного общения!')

        await AsyncORM.remove_one_like(int(pk), int(user_dto["user_id"]))
        await callback.message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                             '4.Изменить текст анкеты.', reply_markup=kb.action)


@router.callback_query(F.data == 'Нет')
async def no(callback: CallbackQuery):
    await callback.answer('')
    get_pk = await AsyncORM.getting_pk(int(callback.from_user.id))
    pk_dto = get_pk[0].model_dump()
    pk = pk_dto["id"]
    await AsyncORM.remove_all_likes(int(pk))
    await callback.message.answer('')
    await callback.message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                                  '4.Изменить текст анкеты.', reply_markup=kb.action)



@router.message(F.text.contains('1') | F.text.contains('👎') | F.text.contains('👍') | F.text.contains('💌'))
async def see_profiles(message: Message, bot: Bot):

    if message.text == '👍':

        pk = await AsyncORM.getting_pk_by_like_id(int(message.chat.id))
        pk_dto = pk[0].model_dump()

        user_id = await AsyncORM.getting_user_id_by_pk(int(pk_dto["profile_id"]))
        user_past_dto = user_id[0].model_dump()

        await bot.send_message(user_past_dto["user_id"],
                               'Вы понравились одному человеку, хотите посмотреть его анкету?',
                               reply_markup=kb.show_user)



    # elif message.text == '💌':
    #     pk = await AsyncORM.getting_pk_by_like_id(int(message.chat.id))
    #     pk_dto = pk[0].model_dump()
    #
    #     user_id = await AsyncORM.getting_user_id_by_pk(int(pk_dto["profile_id"]))
    #     user_past_dto = user_id[0].model_dump()
    #
    #     await bot.send_message(user_past_dto["user_id"],
    #                            '',
    #                            reply_markup=kb.show_user)




    elif message.text == '👎':
        try:
            # # удалить пред запись в лайкс
            pk = await AsyncORM.getting_pk_by_like_id(int(message.chat.id))
            pk_dto = pk[0].model_dump()

            await AsyncORM.delete_last_note_in_likes(int(message.chat.id), int(pk_dto["profile_id"]))
        except IndexError:

            pass



    data = await AsyncORM.convert_users_to_dto(int(message.chat.id))  # start sending profiles
    user_dto = data[0].model_dump()
    await AsyncORM.insert_likes(int(message.chat.id), int(user_dto["id"]))

    await message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                            f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n{user_dto["hobbies"]}\n'
                                                            f'{user_dto["group"]}',
                               reply_markup=kb.profile_view)

@router.message(F.text.in_(['💤']))
async def sleepy(message: Message):
    await message.answer('Подождем пока кто-нибудь увидит твою анкету ;)')
    await message.answer('1. Смотреть анкеты.', reply_markup=kb.sleep_mode)


@router.message(F.text == '2')
async def restart_reg(message: Message, state: FSMContext):
    await AsyncORM.delete_profile(int(message.chat.id))
    await reg_start(message, state)




class UpdatePhoto(StatesGroup):
    photo_id = State()

@router.message(F.text == '3')
async def edit_photo(message: Message, state: FSMContext):
    await state.set_state(UpdatePhoto.photo_id)
    # await AsyncORM.update_photo(str(f"@{message.chat.username}"), )
    await message.answer('Теперь пришли фото')

@router.message(UpdatePhoto.photo_id, F.photo)
async def upd_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Фото загружено')
    data = await state.get_data()
    await AsyncORM.update_photo(int(message.chat.id), str(data["photo_id"]))

    await state.clear()

    await message.answer('Так выглядит твоя анкета:')
    prof = await AsyncORM.send_user_profile(int(message.chat.id))
    user_dto = prof[0].model_dump()
    await message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                                   f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n{user_dto["hobbies"]}\n'
                                                                   f'{user_dto["group"]}')
    await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                         '4.Изменить текст анкеты.', reply_markup=kb.action)

@router.message(UpdatePhoto.photo_id, ~F.photo)
async def incorrect_photo_id(message: Message, state: FSMContext):
    await message.answer('Отправь фото!')


class UpdateHobbies(StatesGroup):
    hobbies = State()

@router.message(F.text == '4')
async def edit_hobbies(message: Message, state: FSMContext):
    await state.set_state(UpdateHobbies.hobbies)
    await message.answer('Расскажи о себе и кого хочешь найти')

@router.message(UpdateHobbies.hobbies)
async def upd_hobby(message: Message, state: FSMContext):
    await state.update_data(hobbies=message.text)
    await message.answer('Текст анкеты изменён')
    data = await state.get_data()
    await AsyncORM.update_hobby(int(message.chat.id), str(data["hobbies"]))
    await state.clear()

    await message.answer('Так выглядит твоя анкета:')
    prof = await AsyncORM.send_user_profile(int(message.chat.id))
    user_dto = prof[0].model_dump()
    await message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                                   f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n{user_dto["hobbies"]}\n'
                                                                   f'{user_dto["group"]}')
    await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                         '4.Изменить текст анкеты.', reply_markup=kb.action)
