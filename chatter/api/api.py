from chatter.api import templates
from chatter import chat
from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse


def configure_api(
    app: FastAPI,
    bot: chat.Bot,
) -> None:

    @app.post("/say")
    async def say(msg: str):
        user_id = bot.user.id
        owner = bot.owner

        await owner.send_message(msg, user_id)

    @app.get("/control", response_class=HTMLResponse)
    async def control(request: Request):
        return await templates.index_template(
            request,
            {
                "msg": "hello there!",
            },
        )


