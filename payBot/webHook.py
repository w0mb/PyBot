import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import Message
from aiogram.filters import Command  # Новый способ обработки команд
from config import TOKEN  # Убедитесь, что ваш токен прописан в config.py

CERT_PATH = "../sertificates/server.crt"
KEY_PATH = "../sertificates/server.key"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
async def send_welcome(message: Message):
    await message.reply("Привет! Это бот, работающий через вебхук!")

# Регистрируем обработчик команды /start
dp.message.register(send_welcome, Command("start"))

# Старт вебхука
async def start_webhook():
    try:
        app = web.Application()

        # Регистрация SimpleRequestHandler для вебхука
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
        print("Starting webhook server...")

        # Используем asyncio.run() вместо получения текущего loop
        await web.run_app(
            app,
            host="0.0.0.0",
            port=8443,
            ssl_context={
                "certfile": CERT_PATH,
                "keyfile": KEY_PATH,
            }
        )
    except Exception as e:
        print(f"Error starting webhook server: {e}")

# Основная функция для запуска бота и вебхуков
async def main():
    print("Бот стартанул")
    
    # Запуск вебхука
    await start_webhook()

# Запуск вебхука с использованием asyncio.run
if __name__ == '__main__':
    asyncio.run(main())  # asyncio.run автоматически создает и закрывает цикл событий
