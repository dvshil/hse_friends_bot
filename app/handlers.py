from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.orm import SyncORM, AsyncORM

import app.keyboards as kb

router = Router()



class Register(StatesGroup):
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
    data = await AsyncORM.send_user_profile(str(f"@{message.chat.username}"))
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
    await state.set_state(Register.name)
    await message.answer('Введи фамилию и имя', reply_markup=ReplyKeyboardRemove())


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Сколько тебе лет?')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.birthday)
    await message.answer('Укажи дату рождения')


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
    await message.answer('Как с тобой связаться?')

@router.message(Register.contact)
async def register_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(Register.photo_id)
    await message.answer('Теперь пришли фото')

@router.message(Register.photo_id)
async def register_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Фото загружено')
    data = await state.get_data()

    curr = await AsyncORM.insert_users(str(data["contact"]))
    pk = curr[0].model_dump()

    await AsyncORM.insert_profiles(str(data["name"]), int(data["age"]), str(data["birthday"]), str(data["zodiac"]),
                                   str(data["group"]),
                                   str(data["hobbies"]), str(data["contact"]), str(data["photo_id"]), int(pk["id"]))
    await message.answer_photo(photo=data["photo_id"], caption=f'{data["name"]}, '
                                                               f'{data["age"]} лет\n{data["birthday"]}, {data["zodiac"]}\n'
                                                               f'{data["hobbies"]}\n'
                                                               f'{data["group"]}\n{data["contact"]}')

    await state.clear()

    await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                         '4.Изменить текст анкеты.', reply_markup=kb.action)

