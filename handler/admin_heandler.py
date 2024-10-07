from aiogram import Router
from aiogram.types import Message
import logging
from aiogram.filters import Command

from handlers.db import db_profile_access, db_profile_exist, db_profile_updateone, db_profile_exist_usr, db_profile_get_usrname


router = Router()

errormessage = 'error_message'
lvl1name = 'Тех.поддержка'
lvl2name = 'Администратор'
lvl3name = 'Руководитель'
devid = 'dev_id'

def extract_arg(arg):
    return arg.split()[1:]


@router.message(Command(commands=["ответ"]))
async def admin_ot(message: Message):
    uid = message.from_user.id

    if db_profile_access(uid) >= 1:
        args = extract_arg(message.text)
        if len(args) >= 2:
            chatid = str(args[0])
            args.pop(0)
            answer = " ".join(args)
            await message.answer('✅ Вы успешно ответили на вопрос!')
            await message.bot.send_message(chatid,
                                   f"✉ Новое уведомление!\nОтвет от тех.поддержки:\n\n`{answer}`",
                                   parse_mode='Markdown')
        else:
            await message.answer(
                '⚠ Укажите аргументы команды\nПример: `/ответ 516712732 Ваш ответ`',
                parse_mode='Markdown')
    else:
        return

@router.message(Command(commands=["доступ"]))
async def admin_giveaccess(message: Message):
    uidown = message.from_user.id
    logging.info(f"User {uidown} called /доступ command")

    if db_profile_access(uidown) >= 3:
        args = extract_arg(message.text)
        if len(args) == 2:
            try:
                uid = int(args[0])
                access = int(args[1])
                logging.debug(f"Parsed arguments: uid={uid}, access={access}")

                if db_profile_exist(uid):
                    if access == 0:
                        outmsg = "✅ Вы успешно сняли все доступы с этого человека!"
                    elif access == 1:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl1name}* данному человеку!"
                    elif access == 2:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl2name}* данному человеку!"
                    elif access == 3:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl3name}* данному человеку!"
                    else:
                        await message.answer(
                            '⚠ Максимальный уровень доступа: *3*',
                            parse_mode='Markdown')
                        return

                    # Правильный вызов функции обновления
                    db_profile_updateone(uid, {"access": access})
                    logging.info(f"Updated access level for user {uid} to {access}")
                    await message.answer(outmsg, parse_mode='Markdown')
                else:
                    logging.warning(f"User {uid} not found in the database")
                    await message.answer(
                        "⚠ Этого пользователя *не* существует!",
                        parse_mode='Markdown')
            except ValueError as e:
                logging.error(f"Error parsing arguments: {e}")
                await message.answer("⚠ Неверные аргументы!",
                                     parse_mode='Markdown')
        else:
            await message.answer(
                '⚠ Укажите аргументы команды\nПример: `/доступ 516712372 1`',
                parse_mode='Markdown')


@router.message(Command(commands=["бан"]))
async def admin_ban(message: Message):
    uidown = message.from_user.id

    if db_profile_access(uidown) >= 2:
        args = extract_arg(message.text)
        if len(args) >= 2:  # Нужно как минимум два аргумента: uid и причина
            uid = int(args[0])
            reason = " ".join(args[1:])  # Причина — всё, что идет после uid
            if db_profile_exist(uid):
                # Обновляем статус бана и причину
                db_profile_updateone(uid, {"ban": 1, "ban_reason": reason})
                await message.answer(f'✅ Вы успешно заблокировали этого пользователя по причине: {reason}',
                                     parse_mode='Markdown')
                await message.bot.send_message(uid, f"⚠ Администратор *заблокировал* Вас в боте по причине: {reason}",
                                               parse_mode='Markdown')
            else:
                await message.answer("⚠ Этого пользователя *не* существует!",
                                     parse_mode='Markdown')
        else:
            await message.answer(
                '⚠ Укажите аргументы команды\nПример: `/бан 516272834 Нарушение правил`',
                parse_mode='Markdown')




@router.message(Command(commands=["разбан"]))
async def admin_unban(message: Message):
    uidown = message.from_user.id

    if db_profile_access(uidown) >= 2:
        args = extract_arg(message.text)
        if len(args) >= 2:  # Нужно как минимум два аргумента: uid и причина
            uid = int(args[0])
            reason = " ".join(args[1:])  # Причина — всё, что идет после uid
            if db_profile_exist(uid):
                # Обновляем статус разбана и причину
                db_profile_updateone(uid, {"ban": 0, "ban_reason": reason})
                await message.answer(f'✅ Вы успешно разблокировали этого пользователя по причине: {reason}',
                                     parse_mode='Markdown')
                await message.bot.send_message(uid, f"⚠ Администратор *разблокировал* Вас в боте по причине: {reason}",
                                               parse_mode='Markdown')
            else:
                await message.answer("⚠ Этого пользователя *не* существует!",
                                     parse_mode='Markdown')
        else:
            await message.answer(
                '⚠ Укажите аргументы команды\nПример: `/разбан 516272834 Прошло время наказания`',
                parse_mode='Markdown')


@router.message(Command(commands=["айди"]))
async def admin_id(message: Message):
    args = extract_arg(message.text)
    if len(args) == 1:
        username = args[0]
        if db_profile_exist_usr(username):
            uid = db_profile_get_usrname(username, '_id')
            await message.answer(f"🆔 {uid}")
        else:
            await message.answer("⚠ Этого пользователя *не* существует!",
                                 parse_mode='Markdown')
    else:
        await message.answer(
            '⚠ Укажите аргументы команды\nПример: `/айди nosemka`',
            parse_mode='Markdown')
