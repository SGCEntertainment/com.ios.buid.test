from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.types import PeerChannel
import asyncio
import os

# Ваши данные API Telegram
api_id = "22002174"
api_hash = "114c42a93cf610b1e8e826b7d3ad6e65"

channel_id = '-1001990817644'
bot_token = '5541471253:AAFGq-cwlYERC9nSYc68_94bWOH0Fx1KkVU'
session_name = StringSession()

# Создайте клиента Telegram
client = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)     

# Printing upload progress
async def callback(current, total):
    progress_text = "Uploaded {:.2f} MB out of {:.2f} MB: {:.2%}".format(current / (1024 * 1024), total / (1024 * 1024), current / total)
    print(progress_text)

async def send_file_to_telegram():
    
    input_name = os.environ['INPUT_BUILDNAME']
    print("Input name:", input_name)
    
    input_caption = os.environ['INPUT_CAPTION']
    print("Input caption:", input_caption)

    file_path_apk = os.getenv("GITHUB_WORKSPACE", default=".") + "/build/Android/" + input_name + ".apk"
    file_path_aab = os.getenv("GITHUB_WORKSPACE", default=".") + "/build/Android/" + input_name + ".aab"
    entity = await client.get_entity(PeerChannel(int(channel_id)))

    # Отправьте APK с использованием токена бота
    await client.send_file(entity, file_path_apk, progress_callback=callback, caption=input_caption, parse_mode='html', attributes=[DocumentAttributeVideo(0, 0, 0, supports_streaming=True)])
    
    # Отправьте AAB с использованием токена бота
    await client.send_file(entity, file_path_aab, progress_callback=callback, caption=input_caption, parse_mode='html', attributes=[DocumentAttributeVideo(0, 0, 0, supports_streaming=True)])

# Авторизуйтесь и выполните отправку файла
with client:
    client.loop.run_until_complete(send_file_to_telegram())