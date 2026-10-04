from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def catalog_kb(song_id):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="▶️ Слушать", callback_data=f"song:play:{song_id}"),
        InlineKeyboardButton(text="❤️ В плейлист", callback_data=f"song:add:{song_id}"),
    ]])

def playlist_kb(song_id):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="▶️ Слушать", callback_data=f"song:play:{song_id}"),
        InlineKeyboardButton(text="🗑️ Удалить из плейлиста", callback_data=f"song:del:{song_id}"),
    ]])


def card_kb(song_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❤️ В плейлист", callback_data=f"song:add:{song_id}")],
        [InlineKeyboardButton(text="🗑️ Удалить из плейлиста", callback_data=f"song:del:{song_id}")],
    ])

