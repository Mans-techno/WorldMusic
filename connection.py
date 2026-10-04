import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def create_conn():
    try:
        conn = await asyncpg.create_pool(
            database = "world_music",
            host = "localhost",
            user = "postgres",
            port = 5432,
            password = os.getenv("DB_PASSWORD")
        )
        print("Connection Successful")
        return conn
    except Exception as error:
        print(f"Error connection: {error}")


async def create_tables():
    conn = await create_conn()
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id serial PRIMARY KEY,
                author_id bigint NOT NULL,
                title varchar(200) NOT NULL CHECK (length(trim(title)) > 0),
                artist varchar(200) NOT NULL CHECK (length(trim(artist)) > 0),
                audio_file_id text NOT NULL CHECK (length(audio_file_id) > 0),
                created_at timestamp NOT NULL DEFAULT now()
            );

            CREATE TABLE IF NOT EXISTS playlist_items (
                id serial PRIMARY KEY,
                user_id bigint NOT NULL,
                song_id integer NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
                added_at timestamp NOT NULL DEFAULT now(),
                UNIQUE (user_id, song_id)
            );
                """)
        print("Table created successful")
    except Exception as error:
        print(f"Error with table creating: {error}")

