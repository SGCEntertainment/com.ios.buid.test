from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import asyncio

# Данные для API Telegram
api_id = "22002174"
api_hash = "114c42a93cf610b1e8e826b7d3ad6e65"

# Чтение переменных окружения
channel_id = int(os.getenv('ChatID_Xcode', '5419377045'))  # Преобразуем строку в целое число
bot_token = os.getenv('BOT_TOKEN', '5541471253:AAFGq-cwlYERC9nSYc68_94bWOH0Fx1KkVU')  # Токен бота

session_name = StringSession()

# Создаем клиента Telegram
client = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)

# Прогресс загрузки
async def callback(current, total):
    progress_text = "Uploaded {:.2f} MB out of {:.2f} MB: {:.2%}".format(current / (1024 * 1024), total / (1024 * 1024), current / total)
    print(progress_text)

async def send_file_to_telegram():
    # Чтение переменной для имени файла
    input_name = os.getenv('INPUT_BUILDNAME', '')
    print("Input name:", input_name)

    if not input_name:
        print("Error: Build name not provided.")
        return

    # Путь к .zip файлу
    file_path_zip = os.path.join(os.getenv("GITHUB_WORKSPACE", default="."), "build", "iOS", f"{input_name}.zip")
    
    # Проверка, существует ли файл
    if not os.path.exists(file_path_zip):
        print(f"Error: File {file_path_zip} does not exist.")
        return
    
    # Получаем сущность канала
    entity = await client.get_entity(channel_id)

    # Отправка файла .zip
    await client.send_file(entity, file_path_zip, progress_callback=callback, caption="", parse_mode='html')

# Авторизация и отправка файла
with client:
    client.loop.run_until_complete(send_file_to_telegram())