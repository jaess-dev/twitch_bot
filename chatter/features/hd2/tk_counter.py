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
            "counter_name": "hd2_team_kill",
            "url": "/overlay/hd2/counter",
            "title": "Team Kills",
            "bot_command": "tk",
            "channel_msg": "Current team kills",
        },
    )


# async def register(
#     app: FastAPI,
#     bot: chat.Bot,
#     db: asqlite.Pool,
# ) -> None:

#     pc = PersistentCounter(db, "hd2_team_kill")
#     await pc.setup_database()

#     @app.get("/overlay/hd2/counter", response_class=HTMLResponse)
#     async def hd2_counter(request: Request):
#         # load counter from DB
#         counter = await pc.get_today_counter()
#         return await templates.counter_overlay(request, counter)

#     class Hd2CounterComponent(ABaseComponent):
#         @commands.group(invoke_fallback=True)
#         async def tk(self, ctx: commands.Context) -> None:
#             """Increment Team Kill counter with !tk"""
#             counter = await pc.increment_today_counter()
#             await ctx.send(f"Current Team Kills: {counter}")

#     reg = ComponentsRegistry()
#     reg.add_component(Hd2CounterComponent)
