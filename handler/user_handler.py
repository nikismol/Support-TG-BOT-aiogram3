from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter
from db import db_profile_exist, db_profile_insertone

router = Router()
router.message.filter(ChatTypeFilter(['private']))

class Question(StatesGroup):
    text = State()



@router.message(ChatTypeFilter('private'), CommandStart())
async def start_handler(message: Message):
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
