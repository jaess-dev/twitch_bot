import json
import asqlite
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from twitchio.ext import commands

from chatter import chat
from chatter.api import templates

from chatter.api.connection_manager import ConnectionManager
from chatter.component_registry import ComponentsRegistry
from chatter.components.component_base import ABaseComponent


async def register(
    app: FastAPI,
    bot: chat.Bot,
    db: asqlite.Pool,
) -> None:

    await __setup_database(db)

    @app.get("/overlay/hd2/counter", response_class=HTMLResponse)
    async def hd2_counter(request: Request):
        # load counter from DB
        counter = await __get_today_counter(db)
        return await templates.counter_overlay(request, counter)

    class Hd2CounterComponent(ABaseComponent):
        @commands.group(invoke_fallback=True)
        async def tk(self, ctx: commands.Context) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await _increment_today_counter(db)
            await ctx.send(f"Current Team Kills: {counter}")

    reg = ComponentsRegistry()
    reg.add_component(Hd2CounterComponent)


async def __setup_database(
    db: asqlite.Pool,
):
    # Create our token table, if it doesn't exist..
    # You should add the created files to .gitignore or potentially store them somewhere safer
    # This is just for example purposes...

    query = """CREATE TABLE IF NOT EXISTS hd2_team_kill_counter (
        counter_date TEXT PRIMARY KEY,
        counter INTEGER DEFAULT 0
    );"""
    async with db.acquire() as connection:
        await connection.execute(query)


async def __get_today_counter(db: asqlite.Pool) -> int:
    today = datetime.date.today().isoformat()
    async with db.acquire() as conn:
        row = await conn.fetchall(
            "SELECT counter FROM hd2_team_kill_counter WHERE counter_date = ?",
            (today,),
        )
        if not row:
            # create a new row for today
            await conn.execute(
                "INSERT INTO hd2_team_kill_counter (counter_date, counter) VALUES (?, ?)",
                (today, 0),
            )
            return 0
        return row[0]["counter"]


async def _increment_today_counter(db: asqlite.Pool) -> int:
    today = datetime.date.today().isoformat()
    async with db.acquire() as conn:
        # atomically increment counter
        await conn.execute(
            """
            INSERT INTO hd2_team_kill_counter(counter_date, counter)
            VALUES (?, 1)
            ON CONFLICT(counter_date) DO UPDATE SET counter = counter + 1
            """,
            (today,),
        )
        # fetch new value
        row = await conn.fetchall(
            "SELECT counter FROM hd2_team_kill_counter WHERE counter_date = ?",
            (today,),
        )

        new_counter = row[0]["counter"]

        ws = ConnectionManager()
        same = ws is ConnectionManager()
        print(same)
        # broadcast new value to all clients
        await ws.broadcast(json.dumps({"counter": new_counter}))

        return new_counter
