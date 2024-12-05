import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import Message
from aiogram.handlers import CommandHandler  # Импортируем обработчик команд
from config import TOKEN  # Убедитесь, что токен у вас прописан в config.py

CERT_PATH = "../sertificates/server.crt"
KEY_PATH = "../sertificates/server.key"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
async def send_welcome(message: Message):
    await message.reply("Привет! Это бот, работающий через вебхук!")

# Регистрируем обработчик команды /start
dp.register(CommandHandler("start", send_welcome))

# Старт вебхука
async def start_webhook(loop):
    try:
        app = web.Application()

        # Регистрация SimpleRequestHandler для вебхука
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
        print("Starting webhook server...")

        # Используем переданный цикл событий (loop)
        await web.run_app(
            app,
            host="0.0.0.0",
            port=8443,
            ssl_context={
                "certfile": CERT_PATH,
                "keyfile": KEY_PATH,
            },
            loop=loop  # Указываем текущий цикл событий
        )
    except Exception as e:
        print(f"Error starting webhook server: {e}")

# Основная функция для запуска бота и вебхуков
async def main():
    print("Бот стартанул")

    # Создаем задачи для всех функций
    loop.create_task(start_webhook(loop))  # Передаем текущий loop в start_webhook

# Запуск вебхука в текущем цикле событий
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Ждем выполнения задач
