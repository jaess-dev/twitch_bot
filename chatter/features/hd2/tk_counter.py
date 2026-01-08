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
            "counter_name": "hd2_death",
            "url": "/overlay/hd2",
            "api": "/api/hd2/counter",
            "title": "Deaths",
            "bot_command": "d",
            "channel_msg": "Current deaths",
            "overlay": "/overlay/hd2"
        },
    )
