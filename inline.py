from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

task_callback_data = CallbackData("task", "number")


def inline_button(cnt: int):
    inline_kb = InlineKeyboardMarkup()
    for i in range(cnt):
        inline_btn = InlineKeyboardButton(f'задача {i + 1}', callback_data=task_callback_data.new(number=i))
        inline_kb.add(inline_btn)
    return inline_kb
