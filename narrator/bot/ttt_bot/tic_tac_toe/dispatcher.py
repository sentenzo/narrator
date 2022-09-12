import asyncio
import random

from aiogram import Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage


from narrator.bot.ttt_bot.tic_tac_toe.game import TicTacToeGame

storage = MemoryStorage()

dp = Dispatcher(storage=storage)


async def humanlike_delay():
    await asyncio.sleep(0.2 + 0.8 * random.random())


class TttMove(CallbackData, prefix="move"):
    player: int
    i: int
    j: int


def make_ttt_kb(
    ttt: TicTacToeGame, blocked: bool = False
) -> types.InlineKeyboardMarkup:
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            t = [" ▫ ", " x ", " o "][ttt._board[i][j]]
            if not blocked and ttt._board[i][j] == 0:
                cd = TttMove(player=1, i=i, j=j).pack()  # f"ttt:{i}:{j}"
            else:
                cd = "illegal_move"
            row.append(InlineKeyboardButton(text=t, callback_data=cd))
        buttons.append(row)
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


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


GAMES = {}


@dp.callback_query(text="user_wants_to_play")
async def user_wants_to_play(callback: types.CallbackQuery):
    await callback.answer()
    ttt = TicTacToeGame()
    GAMES[callback.from_user.id] = ttt
    await callback.message.answer(
        "🤖:",
        reply_markup=make_ttt_kb(ttt),
    )


@dp.callback_query(text="illegal_move")
async def illegal_move(callback: types.CallbackQuery):
    await callback.answer("🤖: Illegal move!")


@dp.callback_query(TttMove.filter())
async def move(callback: types.CallbackQuery, callback_data: TttMove):
    if not callback.from_user.id in GAMES:
        raise IndexError()
    ttt: TicTacToeGame = GAMES[callback.from_user.id]
    await callback.answer()
    ttt.move_manually(callback_data.i, callback_data.j)
    await callback.message.delete()

    board = await callback.message.answer(
        "🤖:",
        reply_markup=make_ttt_kb(ttt, blocked=True),
    )

    if ttt.status == ("Ongoing", 0):
        await humanlike_delay()
        await humanlike_delay()
        ttt.move_ai()
        await board.delete()
        await callback.message.answer(
            "🤖:",
            reply_markup=make_ttt_kb(ttt),
        )

    elif ttt.status == ("Tie", 0):
        await humanlike_delay()
        await callback.message.answer("🤖: It's a tie!")
        await callback.message.answer("🤖: Type /start to play again")
    elif ttt.status[0] == "Win":
        await humanlike_delay()
        await callback.message.answer(f"🤖: Player {ttt.status[1]} wins!")
        await callback.message.answer("🤖: Type /start to play again")

    # await callback.message.answer(callback_data.pack())


TIC_TAC_TOE_DISPATCHER = dp
