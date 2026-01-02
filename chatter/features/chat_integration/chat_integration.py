import json
from typing import TypedDict
import asqlite
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from twitchio import ChatMessage
from twitchio.ext import commands

from chatter import chat
from chatter.api import templates

from chatter.api.connection_manager import ConnectionManager
from chatter.component_registry import ComponentsRegistry
from chatter.components.component_base import ABaseComponent
from chatter.persistence.persistent_counter import PersistentCounter


class RegisterInput(TypedDict):
    pass


async def register(
    app: FastAPI,
    bot: chat.Bot,
    db: asqlite.Pool,
) -> None:

    class ChatIntegrator(ABaseComponent):
        @commands.Component.listener()
        async def event_message(self, payload: ChatMessage) -> None:
            ws = ConnectionManager()
            # broadcast new value to all clients
            await ws.broadcast(
                json.dumps({"messages": [f"[{payload.chatter.name}] {payload.text}"]})
            )

    reg = ComponentsRegistry()
    reg.add_component(ChatIntegrator)
