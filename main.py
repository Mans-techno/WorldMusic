import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
import connection
import service
from keyboards import catalog_kb, playlist_kb, card_kb
from states import fsm_router


load_dotenv()
token = os.getenv("BOT_TOKEN")

bot = Bot(token)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
callback_router = Router()


def get_id(text):
    if text and text.strip().isdigit() and int(text) > 0:
        return int(text)
    return None


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🎵 World Music 🎵\n\n"
        "Добавляй треки в каталог и собирай свой плейлист\n\n"
        "Список команд: /help"
    )



@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer("Нет активного ввода")
        return
    await state.clear()
    await message.answer("❌ Отменено")



@router.message(Command("songs"))
async def songs(message: Message):
    rows = await service.all_songs()
    if not rows:
        await message.answer("Каталог пуст\nДобавьте трек: /add_song")
        return
    for row in rows:
        await message.answer(f"#{row['id']} {row['title']} — {row['artist']}", reply_markup=catalog_kb(row["id"]))



@router.message(Command("song"))
async def song(message: Message, command: CommandObject):
    song_id = get_id(command.args)
    if song_id is None:
        await message.answer("Укажите id\nНапример: /song 3")
        return
    row = await service.find_song(song_id)
    if not row:
        await message.answer("Трек не найден")
        return
    await message.answer_audio(row["audio_file_id"], caption=f"{row['title']} — {row['artist']}", reply_markup=card_kb(row["id"]))



@router.message(Command("playlist"))
async def playlist(message: Message):
    rows = await service.my_playlist(message.from_user.id)
    if not rows:
        await message.answer("Плейлист пуст")
        return
    for row in rows:
        await message.answer(f"#{row['id']} {row['title']} — {row['artist']}", reply_markup=playlist_kb(row["id"]))


@router.message(Command("playlist_stats"))
async def playlist_stats(message: Message):
    count = await service.count(message.from_user.id)
    await message.answer(f"📊 Треков в плейлисте: {count}")



@router.message(Command("artist"))
async def artist(message: Message, command: CommandObject):
    if not command.args or not command.args.strip():
        await message.answer("Пример: /artist Исполнитель")
        return
    rows = await service.artist_songs(command.args.strip())
    if not rows:
        await message.answer("Исполнитель с таким именем не найден")
        return
    for row in rows:
        await message.answer(f"#{row['id']} {row['title']} — {row['artist']}", reply_markup=catalog_kb(row["id"]))



@callback_router.callback_query(F.data.startswith("song:"))
async def song_buttons(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) != 3 or get_id(parts[2]) is None:
        await callback.answer("Неправильная кнопка")
        return
    action = parts[1]
    song_id = int(parts[2])

    row = await service.find_song(song_id)
    if not row:
        await callback.answer("Трек не найден")
        return

    if action == "play":
        await callback.answer()
        await callback.message.answer_audio(row["audio_file_id"], caption=f"{row['title']} — {row['artist']}")
    elif action == "add":
        if await service.like(callback.from_user.id, song_id):
            await callback.answer("❤️ Добавлено в плейлист")
        else:
            await callback.answer("Трек уже в плейлисте")
    elif action == "del":
        if await service.unlike(callback.from_user.id, song_id):
            await callback.answer("🗑️ Удалено из плейлиста")
        else:
            await callback.answer("Этого трека нет в плейлисте")
    else:
        await callback.answer("Некорректная кнопка")



@router.message(Command("help"))
async def help(message: Message):
    await message.answer("""
===== Команды =====
        
/add_song — добавить трек
/songs — каталог
/song <id> — отправить трек
/playlist — мой плейлист
/playlist_stats — сколько треков в плейлисте
/artist <исполнител> — треки исполнителя
/cancel — отменить ввод
/help — справка
    """)



async def main():
    connection.conn = await connection.create_conn()
    await connection.create_tables()
    dp.include_router(router)
    dp.include_router(fsm_router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
