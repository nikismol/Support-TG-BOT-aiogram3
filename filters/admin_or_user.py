import os
from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

admins_str = os.getenv('ADMINS', '')
admins = [int(admin_id) for admin_id in admins_str.split(',') if admin_id.isdigit()]

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return message.from_user.id in admins


class UserFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return message.from_user.id not in admins
