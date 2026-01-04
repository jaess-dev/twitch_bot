import asyncio
import json
import logging
from types import CoroutineType
import typing
import asqlite

import twitchio
from chatter.api import api, connection_manager
from chatter import chat, component_registry
from chatter.api.templates import mount_assets
from chatter.components import basic_component

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatter.env.environment import LOGGER, Variables
from chatter.features.chat_integration import chat_integration
from chatter.features.hd2 import tk_counter, cs2_counter

import uvicorn

app = FastAPI()

mount_assets(app)
ws = connection_manager.ConnectionManager.init(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        *Variables().ALLOWED_HOSTS,
    ],  # your Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

__ACTIVE_FEATURES: list[
    typing.Callable[[FastAPI, chat.Bot, asqlite.Pool], typing.Awaitable[None]]
] = [
    tk_counter.register,
    cs2_counter.register,
    chat_integration.get_register(30),
]


async def runner() -> None:
    async with asqlite.create_pool("tokens.db") as tdb:
        tokens, subs = await chat.setup_database(tdb)

        async with chat.Bot(token_database=tdb, subs=subs) as bot:
            api.configure_api(app, bot)
            for feature_reg in __ACTIVE_FEATURES:
                await feature_reg(app, bot, tdb)

            for pair in tokens:
                await bot.add_token(*pair)

            await bot.start(load_tokens=False)


async def start_server_and_bot():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)

    await asyncio.gather(
        runner(),
        server.serve(),
    )


def main():
    twitchio.utils.setup_logging(level=logging.INFO)

    with open("resources/socials.json") as file:
        socials = json.load(file)

    registry = component_registry.ComponentsRegistry()

    registry.add_component(basic_component.BaicComponent)
    registry.add_component(basic_component.social_component_factory(socials))

    try:
        asyncio.run(start_server_and_bot())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()
