from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import service


fsm_router = Router()


class AddSong(StatesGroup):
    title = State()
    artist = State()
    audio = State()


def check_text(message):
    if not message.text or not message.text.strip():
        return None
    if message.text.startswith("/"):
        return None
    return message.text.strip()


@fsm_router.message(Command("add_song"))
async def add_song(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddSong.title)
    await message.answer("Введите название трека:")


@fsm_router.message(AddSong.title)
async def get_title(message: Message, state: FSMContext):
    title = check_text(message)
    if not title:
        await message.answer("Название должно быть текстом\nВведите название трека:")
        return
    await state.update_data(title=title)
    await state.set_state(AddSong.artist)
    await message.answer("Введите исполнителя:")


@fsm_router.message(AddSong.artist)
async def get_artist(message: Message, state: FSMContext):
    artist = check_text(message)
    if not artist:
        await message.answer("Ты тупой где ты видел исполнителя с цифрой\nВведите исполнителя:")
        return
    await state.update_data(artist=artist)
    await state.set_state(AddSong.audio)
    await message.answer("Отправ аудиофайл:")


@fsm_router.message(AddSong.audio, F.audio)
async def get_audio(message: Message, state: FSMContext):
    data = await state.get_data()
    song_id = await service.save_song(message.from_user.id, data["title"], data["artist"], message.audio.file_id)
    await state.clear()
    await message.answer(f"✅ Трек сохранён маладец\nid: {song_id}")


@fsm_router.message(AddSong.audio)
async def wrong_audio(message: Message):
    await message.answer("Я принимаю только аудиофайл")
