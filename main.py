from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from button import get_main_menu
from aiogram.dispatcher.filters import Text
from config import TOKEN
from states import Ourstates
from datetime import datetime
import random
from user import User
from inline import inline_button, task_callback_data
import datetime
from pathlib import Path

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_mapping = dict()
user_mapping: dict[int, User]
picture = [Path('picture/1.jpg'), Path('picture/2.jpg'), Path('picture/3.jpg'), Path('picture/4.jpg'),
           Path('picture/5.jpg')]
storge = MemoryStorage()


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message):
    user_id = message.from_id

    if user_id not in user_mapping:
        user_mapping[user_id] = User(user_id=user_id, main_dict=[[], [], []], alarm=None)
    await message.answer(text=" добро пожаловать в бот - список задач")
    await message.answer(text="начни с того что добавь первую задачу(кнопка 'новая задача')",
                         reply_markup=get_main_menu())
    await Ourstates.main_state.set()


@dp.message_handler(Text("Новая задача"), state=Ourstates.main_state)
async def task_handler(message: types.Message):
    await message.answer(text="напиши текст своей задачи")
    await Ourstates.text_task.set()


@dp.message_handler(state=Ourstates.text_task)
async def text_of_task(message: types.Message):
    user_id = message.from_id
    task = message.text
    dict = user_mapping[user_id].main_dict
    dict[0].append(task)
    dict[1].append(None)
    user_mapping[user_id].main_dict = dict

    await message.answer(
        text="теперь можешь написать примечания к задаче если примечаний нет напиши '.'")
    await Ourstates.notes_task.set()


@dp.message_handler(state=Ourstates.notes_task)
async def notes_of_task(message: types.Message):
    user_id = message.from_id
    dict = user_mapping[user_id].main_dict
    if (message.text != "."):
        dict[2].append(message.text)
    else:
        dict[2].append(None)

    user_mapping[user_id].main_dict = dict
    await message.answer("задача добавлена ☑️", reply_markup=get_main_menu())
    await Ourstates.main_state.set()


@dp.message_handler(Text("Все задачи"), state=Ourstates.main_state)
async def all_task(message: types.Message):
    user_id = message.from_id
    dict = user_mapping[user_id].main_dict
    if (len(dict[0]) > 0):
        for i in range(len(dict[0])):
            timer = dict[1][i]
            if (timer == None):
                timer = "нет будильника"
            if (dict[2][i] == None):
                notes = "примечаний нет"
            else:
                notes = dict[2][i]
            await message.answer(
                f"Задача {i + 1} - {dict[0][i]} \n будильник - {timer} \n примечание - {notes}")
    else:
        await message.answer("упс задач нет")
    user_mapping[user_id].main_dict = dict


@dp.message_handler(Text("Удалить все задачи"), state=[Ourstates.main_state, Ourstates.remid_state])
async def deleate_all_task(message: types.Message):
    user_id = message.from_id
    await message.answer("Все задачи удалены ❗️")
    user_mapping[user_id].main_dict = [[], [], []]


@dp.message_handler(Text("У меня нет мотивации"), state=Ourstates.main_state)
async def quote(message: types.Message):
    cnt = random.randint(0, 4)
    with open(picture[cnt], "rb") as photo:
        await message.answer_photo(photo, reply_markup=get_main_menu())


@dp.message_handler(Text("удалить конкретную задачу"), state=Ourstates.main_state)
async def delete_task(message: types.Message):
    user_id = message.from_id
    if len(user_mapping[user_id].main_dict[0]) == 0:
        await message.answer("задач нет :(", reply_markup=get_main_menu())
        await Ourstates.main_state.set()
    else:
        inline_kb = inline_button(len(user_mapping[user_id].main_dict[0]))
        await message.answer("Выбери задачу", reply_markup=inline_kb)
        await Ourstates.del_state.set()


@dp.callback_query_handler(task_callback_data.filter(), state=Ourstates.del_state)
async def delete_task_finish(call: types.CallbackQuery, callback_data: dict):
    number = callback_data["number"]
    # str
    number = int(number)
    user_id = call.from_user.id

    for i in range(3):
        del_dict = user_mapping[user_id].main_dict
        del del_dict[i][number]
    await bot.send_message(chat_id=user_id, text="задача удалена", reply_markup=get_main_menu())
    await Ourstates.main_state.set()


@dp.message_handler(Text("Поставить напоминание"), state=Ourstates.main_state)
async def start_timer(message: types.Message):
    user_id = message.from_id
    if (user_mapping[user_id].alarm_state == True):
        await message.answer("к сожелению я не могу ставить больше одного будильника")
        await Ourstates.main_state.set()
    else:
        if len(user_mapping[user_id].main_dict[0]) == 0:
            await message.answer("задач нет :(", reply_markup=get_main_menu())
            await Ourstates.main_state.set()
        else:
            inline_kb = inline_button(len(user_mapping[user_id].main_dict[0]))
            await message.answer("Выбери задачу", reply_markup=inline_kb)
            await Ourstates.remid_state.set()


@dp.callback_query_handler(task_callback_data.filter(), state=Ourstates.remid_state)
async def timer_task_finish(call: types.CallbackQuery, callback_data: dict):
    number = callback_data["number"]
    # str
    number = int(number)
    user_id = call.from_user.id
    user_mapping[user_id].del_num = number - 1
    await bot.send_message(chat_id=user_id,
                           text="я горжусь тобой теперь напиши время формата ЧЧ:ММ я росчитываю на тебя")
    await Ourstates.remid_state_1.set()


@dp.message_handler(state=Ourstates.remid_state_1)
async def set_timer(message: types.Message):
    user_id = message.from_id
    alarm_time = message.text
    try:
        datetime.datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        await message.reply("Неверный формат времени! Используйте ЧЧ:ММ.")
        return
    user_mapping[user_id].main_dict[1][user_mapping[user_id].del_num] = alarm_time
    user_mapping[user_id].alarm = alarm_time
    await message.answer("будильник установлен жди и бойся", reply_markup=get_main_menu())
    user_mapping[user_id].alarm_state = True
    await Ourstates.main_state.set()


async def check_alarms():
    while True:

        for user_id, user in user_mapping.items():
            alarm_time = user_mapping[user_id].alarm
            if alarm_time is not None:
                current_time = datetime.datetime.now().strftime("%H:%M")
                alarm_time_obj = datetime.datetime.strptime(alarm_time, "%H:%M").strftime("%H:%M")
                print(str(current_time))
                print(str(alarm_time_obj))
                if str(current_time) == str(alarm_time_obj):
                    await bot.send_message(user_id,
                                           f"Пора {user_mapping[user_id].main_dict[0][user_mapping[user_id].del_num]}")
                    user_mapping[user_id].alarm = None  # Удаление будильника после срабатывания
                    user_mapping[user_id].main_dict[1][user_mapping[user_id].del_num] = None
                    user_mapping[user_id].alarm_state = False
        await asyncio.sleep(10)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(check_alarms())
        executor.start_polling(dp, skip_updates=True, loop=loop)
    finally:
        loop.close()
