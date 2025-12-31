from chatter import chat
from fastapi import FastAPI


def configure_api(
    app: FastAPI,
    bot: chat.Bot,
) -> None:

    @app.post("/say")
    async def say(msg: str):
        user_id = bot.user.id
        owner = bot.owner

        await owner.send_message(msg, user_id)
