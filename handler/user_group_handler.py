from string import punctuation

from aiogram import F, Router
from aiogram.types import Message

from filters.chat_types import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(['private','group', 'supergroup']))

restricted_words = {'мат', 'мат'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@router.edited_message()
@router.message()
async def censore(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, соблюдайте порядок в чате')
        await message.delete()
