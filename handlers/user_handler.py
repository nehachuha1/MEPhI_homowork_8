from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command, CommandStart

from database.database import Database
from keyboards.pagination_keyboard import build_pagination_keyboard
from lexicon.lexicon import LEXICON_RU

user_router = Router()

# cached_db = CachedDatabase()
users = dict()
db = Database()

@user_router.message(CommandStart())
async def process_start_cmd(message: Message):

    await message.answer(
        parse_mode='HTML',
        text=LEXICON_RU['START_CMD']
    )

@user_router.message(Command(commands='products'))
async def process_products_cmd(message: Message, bot: Bot):
    # cached_db.set_values(str(message.from_user.id), 1)
    users[str(message.from_user.id)] = 1

    current_kb = build_pagination_keyboard(current_page=1)
    current_product = db.get_product(1)

    await message.answer_photo(
        parse_mode='HTML',
        photo=FSInputFile(path=current_product[-2]),
        caption=LEXICON_RU['PRODUCT_CARD'].format(
            name=current_product[1],
            url=current_product[2],
            price=current_product[-1]
        ),
        reply_markup=current_kb
    )

@user_router.callback_query(F.data.in_(['PREVIOUS_PAGE', 'NEXT_PAGE']))
async def process_paginate_products(callback: CallbackQuery):
    current_page = users[str(callback.from_user.id)]

    flag = False

    if (callback.data == 'PREVIOUS_PAGE') and (current_page > 1):
        current_page -= 1
        current_product = db.get_product(current_page)

        users[str(callback.from_user.id)] = current_page
        flag = True
    elif (callback.data == 'NEXT_PAGE'):
        current_page += 1
        current_product = db.get_product(current_page)

        users[str(callback.from_user.id)] = current_page
        flag = True

    if flag:
        current_kb = build_pagination_keyboard(current_page=current_page)
        
        await callback.message.delete()
        await callback.answer('')

        await callback.message.answer_photo(
            parse_mode='HTML',
            photo=FSInputFile(path=current_product[-2]),
            caption=LEXICON_RU['PRODUCT_CARD'].format(
                name=current_product[1],
                url=current_product[2],
                price=current_product[-1]
            ),
            reply_markup=current_kb
        )
    else:
        await callback.answer(
            parse_mode='HTML',
            text=LEXICON_RU['ERROR'],
            show_alert=True
        )