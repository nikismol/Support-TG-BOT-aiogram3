from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter
from .db import *
from keyboards import *


router = Router()

aboutus = 'ЭТО БАЗА'
welcomemessage = 'Welcome'
question_first_msg = '📝 Введите ваш вопрос (Можно прикрепить фото):'
handler_button_new_question = '✉ Задать вопрос'
handler_button_about_us = '📚 Про нас'


tehchatid = '-1002483146691'
message_sended = '✉ Ваш вопрос был отослан! Ожидайте ответа от тех.поддержки.'



class Question(StatesGroup):
    text = State()

@router.message(ChatTypeFilter('private'), CommandStart())
async def client_start(message: Message):
    if db_profile_exist(message.from_user.id):
        await message.answer(welcomemessage, parse_mode='Markdown', reply_markup=mainmenu)
    else:
        db_profile_insertone({
            '_id': message.from_user.id,
            'username': message.from_user.username,
            'access': 0,
            'ban': 0
        })
        print('Новый пользователь!')
        await message.answer(welcomemessage, parse_mode='Markdown', reply_markup=mainmenu)


@router.message(ChatTypeFilter('private'), StateFilter(None))
async def client_newquestion(message: Message, state: FSMContext):
    banned = db_profile_banned(message.from_user.id)

    if banned:
        await message.answer("⚠ Вы *заблокированы* у бота!", parse_mode='Markdown')
        return

    if message.text == handler_button_new_question:
        await message.answer("📝 Введите ваш вопрос (Можно прикрепить фото):")
        await state.set_state(Question.text)
        print("Состояние установлено на FSMQuestion.text")
    if message.text == handler_button_about_us:
        await message.answer(f"{aboutus}", disable_web_page_preview=True, parse_mode='Markdown')


@router.message(ChatTypeFilter('private'), StateFilter(Question.text))
async def newquestion(message: Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные состояния

    if message.content_type == 'photo':
        data['text'] = message.caption
    else:
        data['text'] = message.text

    await state.clear()

    who = f"@{message.chat.username}" if message.chat.username else "Ник не установлен"
    question = data['text']

    await message.reply(message_sended, parse_mode='Markdown')

    if message.content_type == 'photo':
        ph = message.photo[0].file_id
        await message.bot.send_photo(tehchatid, ph,
                             caption=f"✉ | Новый вопрос\nОт: {who}\nВопрос: `{question}`\n\n📝 Чтобы ответить на вопрос введите `/ответ {message.chat.id} Ваш ответ`",
                             parse_mode='Markdown')
    else:
        await message.bot.send_message(tehchatid,
                               f"✉ | Новый вопрос\nОт: {who}\nВопрос: `{question}`\n\n📝 Чтобы ответить на вопрос введите `/ответ {message.chat.id} Ваш ответ`",
                               parse_mode='Markdown')


@router.message(ChatTypeFilter('group'), Command('get_id'))
async def client_getgroupid(message: types.Message):
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*", parse_mode='Markdown')

