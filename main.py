import logging
import json
from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.json import json

bot = Bot(token="5812496639:AAFqraVCQ0SGbdv3XeD2AiUe5pihMHPaScE")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class jobwork(StatesGroup):
    addition_user = State()


@dp.message_handler(commands='start', state='*')
async def start_processing(message: types.Message, state: FSMContext):
    await message.answer('Приветствуем, наш дорогой покупатель!🌹'
                         'Мы благодарим Вас за выбор нашего бренда!'
                         'Для получения подарка-отправьте «+» в чат нашего бота.')
    await state.set_state(jobwork.addition_user.state)


@dp.message_handler(text='+', state=jobwork.addition_user.state)
async def user_add_processing(message: types.Message, state: FSMContext):
    with open('result.json', 'rt', encoding='utf-8') as file:
        data_dict = json.loads(file.read())
    data_dict[str(message.from_user.id)] = ''
    file = open('file.pdf', 'rb')
    await message.answer(f'Твой подарок это я!')
    await bot.send_document(chat_id=message.from_user.id, document=file)
    with open('result.json', 'w', encoding='utf-8') as fp:
        json.dump(data_dict, fp, indent=4, ensure_ascii=False)


@dp.message_handler(lambda message: message.chat.id == -1001861320737, content_types=ContentTypes().ANY)
async def rrrara(message: types.Message):
    with open('result.json', 'rt', encoding='utf-8') as file:
        data_dict = json.loads(file.read())
    for key in data_dict.keys():
        try:
            if message.text is not None:
                try:
                    await bot.send_message(chat_id=key,text=message.text)
                except IndexError:
                    pass
            elif message.document is not None:
                try:
                    await bot.send_document(chat_id=key, document=message.document.file_id, caption=message.caption)
                except IndexError:
                    pass
            elif message.photo is not None:
                try:
                    await bot.send_photo(chat_id=key, photo=message.photo[-1].file_id, caption=message.caption)
                except IndexError:
                    pass
        except KeyError as _KE:
            print('key', _KE)
        except BotBlocked:
            pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
