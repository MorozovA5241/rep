from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)  # Создание объекта бота с использованием токена
dp = Dispatcher(
    bot=bot, storage=MemoryStorage()
)  # Создание диспетчера с использованием объекта бота и хранилища состояний в памяти


@dp.message_handler(
    commands=["start"], state="*"  # команда /start будет работать из любом состояния
)  # Обработчик команды /start для любого состояния
async def start_handler(message: types.Message, state: FSMContext):
    # у каждого пользовател есть свой словарик принадлежащий его состоянию
    # Для начала нужно передать состояние пользователя в функцию в параметре `state`
    data = await state.get_data()  # так мы можем получить этот словарь
    await state.update_data({"counter": 0})  # а так обновить
    # то же самое await state.update_data(counter=0)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1) # TODO: создать клавиатуру
    button = keyboard.add(KeyboardButton("клик"))  # TODO: создать кнопку

    await message.reply(
        text="Привет! Я бот-кликер, нажми на кнопку...", reply_markup=keyboard  # Ответить клавиуатурой
    )


@dp.message_handler(
    Text("клик"), state="*"
)
async def click_handler(message: types.Message, state: FSMContext):
    data = await state.get_data() # TODO: получить словарь пользователя из состояния `state`
    counter = data["counter"]  # это просто словарик, мы можем получить данные по ключу
    counter += 1  # Увеличим значение на один
    await state.update_data({"counter": counter})# TODO: обновить словарь пользователя в состоянии `state`

    text = f"Вы нажали {counter} раз"
    await message.answer(text)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dispatcher=dp, skip_updates=True)