from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(KeyboardButton("Новая задача"), KeyboardButton("Все задачи"))
    markup.row(KeyboardButton("Удалить все задачи"), KeyboardButton("удалить конкретную задачу"))
    markup.add(KeyboardButton("У меня нет мотивации"))
    markup.add(KeyboardButton("Поставить напоминание"))
    return markup