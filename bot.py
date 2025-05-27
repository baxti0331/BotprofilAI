import os
import asyncio
from telethon import TelegramClient, events
import openai

# Переменные окружения (устанавливаем в Railway)
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Инициализация
client = TelegramClient('session', API_ID, API_HASH)
openai.api_key = OPENAI_API_KEY

async def gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка OpenAI: {e}"

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    if sender.is_self:
        return  # не отвечать самому себе

    text = event.raw_text
    print(f"Новое сообщение: {text}")

    reply = await gpt_response(text)
    await event.respond(reply)

async def main():
    print("Запускаем userbot...")
    await client.start()
    print("Userbot запущен.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
