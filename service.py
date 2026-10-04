import connection


async def save_song(author_id, title, artist, audio_file_id):
    try:
        return await connection.conn.fetchval("""
            INSERT INTO songs (author_id, title, artist, audio_file_id)
            VALUES ($1, $2, $3, $4)
            RETURNING id
            """, author_id, title, artist, audio_file_id,)
    except Exception as error:
        print(f"Error in save_song: {error}")



async def all_songs():
    try:
        return await connection.conn.fetch("SELECT id, title, artist FROM songs ORDER BY id")
    except Exception as error:
        print(f"Error in all_songs: {error}")
        return []


async def find_song(song_id):
    try:
        return await connection.conn.fetchrow(
            "SELECT id, title, artist, audio_file_id FROM songs WHERE id = $1", 
            song_id, 
        )
    except Exception as error:
        print(f"Error in find_song: {error}")
     



async def artist_songs(artist):
    try:
        return await connection.conn.fetch(
            "SELECT id, title, artist FROM songs WHERE lower(artist) = lower($1) ORDER BY id",
            artist,
        )
    except Exception as error:
        print(f"Error in artist_songs: {error}")
        


async def like(user_id, song_id):
    try:
        row_id = await connection.conn.fetchval("""
            INSERT INTO playlist_items (user_id, song_id) VALUES ($1, $2)
            ON CONFLICT (user_id, song_id) DO NOTHING
            RETURNING id
            """, user_id, song_id,)
        return row_id is not None
    except Exception as error:
        print(f"Error in like: {error}")
        


async def unlike(user_id, song_id):
    try:
        row_id = await connection.conn.fetchval(
            "DELETE FROM playlist_items WHERE user_id = $1 AND song_id = $2 RETURNING id",
            user_id, song_id,
        )
        return row_id is not None
    except Exception as error:
        print(f"Error in unlike: {error}")
        



async def my_playlist(user_id):
    try:
        return await connection.conn.fetch("""
            SELECT s.id, s.title, s.artist FROM playlist_items p
            JOIN songs s ON s.id = p.song_id
            WHERE p.user_id = $1
            ORDER BY p.added_at
            """,
            user_id,
        )
    except Exception as error:
        print(f"Error in my_playlist: {error}")



async def count(user_id):
    try:
        return await connection.conn.fetchval(
            "SELECT COUNT(*) FROM playlist_items WHERE user_id = $1",
            user_id,
        )
    except Exception as error:
        print(f"Error in count: {error}")
        
        