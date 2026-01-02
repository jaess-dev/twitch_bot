from typing import TypedDict
import asqlite
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from twitchio.ext import commands

from chatter import chat
from chatter.api import templates

from chatter.api.connection_manager import ConnectionManager
from chatter.component_registry import ComponentsRegistry
from chatter.components.component_base import ABaseComponent
from chatter.persistence.persistent_counter import PersistentCounter


class RegisterInput(TypedDict):
    counter_name: str
    url: str
    title: str
    bot_command: str
    channel_msg: str


async def register(
    app: FastAPI,
    bot: chat.Bot,
    db: asqlite.Pool,
    data: RegisterInput,
) -> None:

    pc = PersistentCounter(db, data["counter_name"])
    await pc.setup_database()

    @app.get(data["url"], response_class=HTMLResponse)
    async def get_counter(request: Request):
        counter = await pc.get_today_counter()
        return await templates.counter_overlay(request, counter, data["title"])

    class CounterComponent(ABaseComponent):
        @commands.command(name=data["bot_command"])
        async def counter_command(self, ctx: commands.Context) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await pc.increment_today_counter()
            await ctx.send(f"{data["channel_msg"]}: {counter}")

    # components are registered by name and cannot be registered twice.
    # So we change the name here based on meta properties.
    CounterComponent.__name__ = f"CounterComponent_{data["counter_name"]}"
    CounterComponent.__qualname__ = CounterComponent.__name__

    reg = ComponentsRegistry()
    reg.add_component(CounterComponent)
