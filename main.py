from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from config import TOKEN
from States import Ourstates
from user import User

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
main_dict = [[],  # str
             [],  # bool
             []]
user_mapping = dict()
user_mapping: dict[int, User]


def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(KeyboardButton("Новая задача"), KeyboardButton("Все задачи"))
    markup.add(KeyboardButton("Удалить все задачи"))
    return markup


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(text="бот - список задач (больше не придумал)")
    await message.answer(text="начни с того что добавь первую задачу(кнопка 'новая задача')",
                         reply_markup=get_main_menu())
    await Ourstates.main_state.set()


@dp.message_handler(Text("Новая задача"), state=Ourstates.main_state)
async def task_handler(message: types.Message):
    await message.answer(text="напиши текст своей задачи")
    await Ourstates.text_task.set()


@dp.message_handler(state=Ourstates.text_task)
async def text_of_task(message: types.Message):
    task = message.text
    main_dict[0].append(task)
    print(main_dict)
    main_dict[1].append("не сделано")
    print(main_dict)
    await message.answer(
        text="теперь можешь написать примечания к задаче(дата, срок выполнения и т.п.) если примечаний нет напиши '.'")
    await Ourstates.notes_task.set()


@dp.message_handler(state=Ourstates.notes_task)
async def notes_of_task(message: types.Message):
    if (message.text != "."):
        main_dict[2].append(message.text)
    else:
        main_dict[2].append(None)
    await message.answer("задача добавлена ☑️", reply_markup=get_main_menu())
    print(main_dict)
    await Ourstates.main_state.set()


@dp.message_handler(Text("Все задачи"), state=Ourstates.main_state)
async def all_task(message: types.Message):
    if (len(main_dict[0]) > 0):
        for i in range(len(main_dict[0])):
            await message.answer(
                f"Задача {i + 1} - {main_dict[0][i]} \n coстояние - {main_dict[1][i]} \n примечание - {main_dict[2][i]}")
    else:
        await message.answer("упс задач нет")


@dp.message_handler(Text("Удалить все задачи"), state=Ourstates.main_state)
async def all_task(message: types.Message):
    await message.answer("Все задачи удалены ❗️")
    user.main_dict = [[], [], []]


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )
