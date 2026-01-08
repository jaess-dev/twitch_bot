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
    overlay: str | None


async def register(
    app: FastAPI,
    bot: chat.Bot,
    db: asqlite.Pool,
    data: RegisterInput,
) -> None:

    pc = PersistentCounter(db, data["counter_name"])
    await pc.setup_database()

    @app.get(data["url"], response_class=HTMLResponse)
    async def get_overlay(request: Request):
        counter = await pc.get_today_counter()
        if (ov:=data.get("overlay")) is None:
            ov = "overlay/hd2"
        return await templates.counter_overlay(request, counter, data["title"], ov)

    class CounterComponent(ABaseComponent):
        @commands.group(name=data["bot_command"], invoke_fallback=True)
        # @commands.is_moderator()
        async def counter(self, ctx: commands.Context[chat.Bot]) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await pc.get_today_counter()
            await ctx.send(f"{data["channel_msg"]}: {counter}")

        @counter.command(name="+")
        @commands.is_moderator()
        async def counter_add(self, ctx: commands.Context[chat.Bot]) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await pc.increment_today_counter()
            await ctx.send(f"{data["channel_msg"]}: {counter}")

        @counter.command(name="-")
        @commands.is_moderator()
        async def counter_sub(self, ctx: commands.Context[chat.Bot]) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await pc.decrement_today_counter()
            await ctx.send(f"{data["channel_msg"]}: {counter}")

        @counter.command(name="set")
        @commands.is_moderator()
        async def counter_set(self, ctx: commands.Context[chat.Bot], val: int) -> None:
            """Increment Team Kill counter with !tk"""
            counter = await pc.set_today_counter(val)
            await ctx.send(f"{data["channel_msg"]}: {counter}")

        @counter.command(name="reset")
        @commands.is_moderator()
        async def counter_reset(self, ctx: commands.Context[chat.Bot]) -> None:
            """ """
            counter = await pc.reset_counter_today()
            await ctx.send(f"{data["channel_msg"]}: {counter}")

    # components are registered by name and cannot be registered twice.
    # So we change the name here based on meta properties.
    CounterComponent.__name__ = f"CounterComponent_{data["counter_name"]}"
    CounterComponent.__qualname__ = CounterComponent.__name__

    reg = ComponentsRegistry()
    reg.add_component(CounterComponent)
