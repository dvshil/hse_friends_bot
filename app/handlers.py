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



    await state.clear()
