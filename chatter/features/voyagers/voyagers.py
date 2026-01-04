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
            "counter_name": "voyagers_deaths",
            "url": "/overlay/voyagers",
            "title": "Tode",
            "bot_command": "fell",
            "channel_msg": "Aktuelle Tode",
            "overlay": "/overlay/voyagers"
        },
    )

