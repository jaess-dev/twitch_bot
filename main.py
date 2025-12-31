import asyncio
import json
import logging

import asqlite
import twitchio
from api import api
from chatter import chat, component_registry
from chatter.components import basic_component

from fastapi import FastAPI

from chatter.env.environment import LOGGER

import uvicorn

app = FastAPI()


async def runner() -> None:
    async with asqlite.create_pool("tokens.db") as tdb:
        tokens, subs = await chat.setup_database(tdb)

        async with chat.Bot(token_database=tdb, subs=subs) as bot:
            api.configure_api(app, bot)

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
