import asyncio
import random

from aiogram import Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from narrator.ttt_bot.tic_tac_toe.game import TicTacToeGame


dp = Dispatcher()


async def humanlike_delay():
    await asyncio.sleep(0.2 + 0.8 * random.random())


@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await humanlike_delay()
    await message.answer("🤖: Hello, friend!")
    await humanlike_delay()
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="Yes 🙂", callback_data="user_wants_to_play"),
        types.InlineKeyboardButton(
            text="No 😕", callback_data="user_doesnt_want_to_play"
        ),
    )
    await message.answer(
        "🤖: Have some time to play tic-tac-toe with me?",
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(text="user_doesnt_want_to_play")
async def user_doesnt_want_to_play(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("🤖: Ok then")
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="I've changed my mind. I want to play 😕",
            callback_data="user_wants_to_play",
        )
    )
    await callback.message.answer(
        "🤖: Type /start or press the below button if you change your mind",
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(text="user_wants_to_play")
async def user_wants_to_play(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("🤖: Nice!")
    await humanlike_delay()
    await callback.message.answer("🤖: You play X-s, I play O-s")
    await humanlike_delay()
    await callback.message.answer("🤖: Let me draw the field...")
    await humanlike_delay()
    await humanlike_delay()

    ttt = TicTacToeGame()

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=ttt.make_kb())

    await callback.message.answer(
        "🤖: Here it is",
        reply_markup=keyboard,
    )
    await humanlike_delay()
    await callback.message.answer("🤖: Your turn")

    player = 1
    while ttt.status == ("Ongoing", 0):
        await humanlike_delay()
        await humanlike_delay()
        ttt.move_ai(player)
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=ttt.make_kb())
        await callback.message.answer(
            "🤖:",
            reply_markup=keyboard,
        )
        player = 3 - player

    if ttt.status == ("Tie", 0):
        await humanlike_delay()
        await callback.message.answer("🤖: It's a tie!")
    elif ttt.status[0] == "Win":
        await humanlike_delay()
        await callback.message.answer(f"🤖: Player {ttt.status[1]} wins!")
    await humanlike_delay()
    await callback.message.answer("🤖: Type /start to play again")


TIC_TAC_TOE_DISPATCHER = dp
