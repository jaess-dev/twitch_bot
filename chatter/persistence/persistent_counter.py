import datetime
import json
import asqlite

from chatter.api.connection_manager import ConnectionManager


class PersistentCounter(object):
    def __init__(self, db: asqlite.Pool, name: str):
        self.__db = db
        self.__name = name

    async def setup_database(self) -> None:
        # Create our token table, if it doesn't exist..
        # You should add the created files to .gitignore or potentially store them somewhere safer
        # This is just for example purposes...

        query = """CREATE TABLE IF NOT EXISTS counters (
            counter_name TEXT NOT NULL,
            counter_date TEXT NOT NULL,
            counter INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (counter_name, counter_date)
        );"""
        async with self.__db.acquire() as connection:
            await connection.execute(query)

    async def get_today_counter(self) -> int:
        today = datetime.date.today().isoformat()
        async with self.__db.acquire() as conn:
            row = await conn.fetchall(
                "SELECT counter FROM counters WHERE counter_date = ? and counter_name = ?",
                (today, self.__name),
            )
            if not row:
                # create a new row for today
                await conn.execute(
                    "INSERT INTO counters (counter_name, counter_date, counter) VALUES (?, ?, ?)",
                    (self.__name, today, 0),
                )
                return 0
            return row[0]["counter"]

    async def increment_today_counter(self) -> int:
        today = datetime.date.today().isoformat()
        async with self.__db.acquire() as conn:
            # atomically increment counter
            await conn.execute(
                """
                INSERT INTO counters(counter_name, counter_date, counter)
                VALUES (?, ?, 1)
                ON CONFLICT(counter_name, counter_date) DO UPDATE SET counter = counter + 1
                """,
                (self.__name, today),
            )
            # fetch new value
            row = await conn.fetchall(
                "SELECT counter FROM counters WHERE counter_date = ? and counter_name = ?",
                (today, self.__name),
            )

            new_counter = row[0]["counter"]

            ws = ConnectionManager()
            same = ws is ConnectionManager()
            # broadcast new value to all clients
            await ws.broadcast(json.dumps({"counter": new_counter}))

            return new_counter
