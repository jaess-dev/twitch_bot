import asqlite
from fastapi import FastAPI

from chatter import chat
from chatter.features.hd2 import counter


async def register(
    app: FastAPI,
    bot: chat.Bot,
    db: asqlite.Pool,
):
    return await counter.register(
        app,
        bot,
        db,
        {
            "counter_name": "cs2_counter",
            "url": "/overlay/cs2/counter",
            "title": "TOTAL KILLS",
            "bot_command": "csk",
            "channel_msg": "Current CS 2 kills",
        },
    )