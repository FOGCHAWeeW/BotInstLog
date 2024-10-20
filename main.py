import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from datetime import datetime
from aiogram.types.web_app_info import WebAppInfo

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = '7191553960:AAHexyqtjtST84zyAy9X9NDqO_NFYFkXmwk'  # Вставьте здесь ваш токен бота
MANAGER_ID = '7330150303'  # Вставьте сюда ID менеджера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class OrderState(StatesGroup):
    waiting_for_store = State()
    waiting_for_product_info = State()
    waiting_for_size = State()
    confirming_order = State()

# Список магазинов

stores = ["POIZON", "Alibaba", "Taobao", "95"]

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["✅СДЕЛАТЬ ЗАКАЗ", "⚙️ПОМОЩЬ"]
    keyboard.add(*buttons)
    #keyboard.add(types.KeyboardButton('ОТКРЫТЬ APP', web_app=WebAppInfo(url='https://www.poizon.com/')))
    photoZastav = 'zstavTG.jpg'
    with open(photoZastav, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo, caption='🔥Wassup!'
                                                                   '\n✅Мы поможем тебе заказать и доставить товары с популярных маркетплейсов Китая'
                                                                   '\n🕒️Наша служба поддержки работает с 8:00 до 21:00 каждый день'
                                                                   '\n❗️Вперёд – это не сложно', reply_markup=keyboard)
    # await message.answer('🔥Wassup!'
    #                  '\n✅Мы поможем тебе заказать и доставить товары с популярных маркетплейсов Китая'
    #                  '\n🕒️Наша служба поддержки работает с 8:00 до 21:00 каждый день'
    #                  '\n❗️Вперёд – это не сложно', reply_markup=keyboard)





@dp.message_handler(lambda message: message.text == "✅СДЕЛАТЬ ЗАКАЗ")
async def choose_store(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for store in stores:
        keyboard.add(store)
    #keyboard.add("⬅️НАЗАД В ГЛАВНОЕ МЕНЮ")
    await message.answer("✨Выберите магазин:", reply_markup=keyboard)
    await OrderState.waiting_for_store.set()

@dp.message_handler(lambda message: message.text in stores, state=OrderState.waiting_for_store)
async def get_product_info(message: types.Message, state: FSMContext):
    await state.update_data(chosen_store=message.text)


    photoHelp95 = 'help95.jpg'
    photoHelpAlibaba = 'helpAlibaba.jpg'
    photoHelpPoizon = 'helpPoizon.jpg'
    photoHelpTaobao = 'helpTaobao.jpg'
    if message.text == 'POIZON':
        keyboardP = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bPoizon = types.KeyboardButton('🔥ОТКРЫТЬ POIZON', web_app=WebAppInfo(url='https://www.poizon.com/'))
        keyboardP.add(bPoizon)
        with open(photoHelpPoizon, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo,
                                 caption=f"✅Вы выбрали магазин: {message.text}\n🎯Отправь ссылку или название товара:", reply_markup=keyboardP)

    if message.text == 'Alibaba':
        keyboardA = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bAlibaba = types.KeyboardButton('🔥ОТКРЫТЬ Alibaba', web_app=WebAppInfo(url='https://www.alibaba.com/'))
        keyboardA.add(bAlibaba)
        with open(photoHelpAlibaba, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo,
                                 caption=f"✅Вы выбрали магазин: {message.text}\n🎯Отправь ссылку или название товара:", reply_markup=keyboardA)

    if message.text == 'Taobao':
        keyboardT = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bTaobao = types.KeyboardButton('🔥ОТКРЫТЬ Taobao', web_app=WebAppInfo(url='https://www.taobao.com/'))
        keyboardT.add(bTaobao)
        with open(photoHelpTaobao, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo,
                                 caption=f"✅Вы выбрали магазин: {message.text}\n🎯Отправь ссылку или название товара:", reply_markup=keyboardT)

    if message.text == '95':
        with open(photoHelp95, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo,
                                 caption=f"✅Вы выбрали магазин: {message.text}\n🎯Отправь ссылку или название товара:")


    # await message.answer(f"✅Вы выбрали магазин: {message.text}\n🎯Отправь ссылку или название товара:")
    await OrderState.waiting_for_product_info.set()

@dp.message_handler(state=OrderState.waiting_for_product_info)
async def get_size(message: types.Message, state: FSMContext):
    await state.update_data(product_info=message.text)
    await message.answer("🎯Введите размер товара:")
    await OrderState.waiting_for_size.set()

@dp.message_handler(state=OrderState.waiting_for_size)
async def confirm_order(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_store = user_data.get('chosen_store')
    product_info = user_data.get('product_info')
    size = message.text
    await state.update_data(size=size)

    order_details = f"📍Магазин: {chosen_store}\n📍Товар: {product_info}\n📍Размер: {size}"
    await message.answer(f"❗️Подтвердите свой заказ:\n{order_details}\n✅Нажмите 'Да' для подтверждения или 'Нет' для отмены.")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("👍ДА", "👎НЕТ")
    await message.answer("🆗Выберите действие:", reply_markup=keyboard)
    await OrderState.confirming_order.set()

@dp.message_handler(lambda message: message.text == "👍ДА", state=OrderState.confirming_order)
async def order_confirmed(message: types.Message, state: FSMContext):
    # Здесь можно отправить уведомление менеджеру
    user_data = await state.get_data()
    size = user_data.get('size')
    chosen_store = user_data.get('chosen_store')
    product_info = user_data.get('product_info')
    #size = message.text
    timeDATA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kodeTimeDATA = datetime.now().strftime("%Y%m%d%H%M%S")
    await bot.send_message(MANAGER_ID, f"Время: {timeDATA}\nЗаказ от пользователя: @{message.from_user.username}\nМагазин: {chosen_store}\nТовар: {product_info}\nРазмер: {size}"
                                       f"\nКОД ЗАКАЗА: {kodeTimeDATA}")
    await message.answer('Напишите нашему менеджеру пожалуйста https://t.me/managerinstlog'
                         f'\n📍Код вашего заказа: {kodeTimeDATA}'
                         '📍Ваш заказ передан на рассмотрение модератору')
    #await message.answer('📍Ваш заказ передан на рассмотрение модератору'
    #                                                      '\n🕒️В течение 15 минут вам напишет наш менеджер'
    #                                                      f'\n☎️В случае если вам никто не ответит напишите в тех-поддержку: https://t.me/managerinstlog'
    #                                                        '\n----------'
    #                                                        '\n❗️ЕСЛИ ЧТО ТО СЛУЧИЛОСЬ С ЗАКАЗОМ ПРОСТО НАПИШИТЕ КОД ВАШЕГО ЗАКАЗА В ТЕХ-ПОДДЕРЖКУ'
    #                                                        f'\n📍Код вашего заказа: {kodeTimeDATA}')

    await state.finish()
    await start_command(message)

@dp.message_handler(lambda message: message.text == "👎НЕТ", state=OrderState.confirming_order)
async def order_cancelled(message: types.Message, state: FSMContext):
    await message.answer("❌Ваш заказ отменен.\n🆗Вы можете начать заново.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await start_command(message)

@dp.message_handler(lambda message: message.text == "⚙️ПОМОЩЬ")
async def help_command(message: types.Message):
    await message.answer("🧰Если у вас есть вопросы, вы можете обратиться к менеджеру.\n💡Напишите сюда: https://t.me/managerinstlog")
    #await message.answer("Если у вас есть вопросы, вы можете обратиться к менеджеру. Напишите сюда: @your_manager_username.", reply_markup=types.ReplyKeyboardRemove())
# @dp.message_handler(lambda message: message.text == "Корзина")
# async def view_cart(message: types.Message):
#     await message.answer("Корзина временно пуста. Вы можете добавить товары через меню 'Сделать заказ'.", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text, state='*')
async def unknown_message(message: types.Message):
    await message.answer("Чёт я не понял, о чём ты\nНАЖМИ СЮДА 👉 /start")

    
@dp.message_handler(commands=['open'])
async def open_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("🌐 Перейти на сайт", web_app=WebAppInfo(url='https://pw4227.craftum.io/'))
    keyboard.add(button)
    
    await message.answer("📱 В ПРИЛОЖЕНИИ УДОБНЕЕ", reply_markup=keyboard)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
