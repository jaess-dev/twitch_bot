from api import templates
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
        return templates.index_template(
            {
                "request": request,
                "title": "Send Message",
                "heading": "Send Message",
            }
        )

    @app.get("/overlay/hd2/counter", response_class=HTMLResponse)
    async def hd2_counter(request: Request):
        return templates.counter_overlay(request, 0)
