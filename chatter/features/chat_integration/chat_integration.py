import asyncio
from dataclasses import dataclass
import json
from typing import TypedDict
import asqlite
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from twitchio import ChannelBan, ChatMessage, ChatMessageDelete
from twitchio.ext import commands

from chatter import chat
from chatter.api import templates

from chatter.api.connection_manager import ConnectionManager
from chatter.component_registry import ComponentsRegistry
from chatter.components.component_base import ABaseComponent
from chatter.persistence.persistent_counter import PersistentCounter


class RegisterInput(TypedDict):
    pass


def get_register(timeout=0):
    async def register(
        app: FastAPI,
        bot: chat.Bot,
        db: asqlite.Pool,
    ) -> None:
        @dataclass
        class ChatMessageDto(object):
            message_id: str
            user_id: str
            message: str

        class ChatIntegrator(ABaseComponent):
            _messages: list[ChatMessageDto] = []
            _lock = asyncio.Lock()

            def __init__(self, bot: commands.AutoBot) -> None:
                super().__init__(bot)

            @commands.Component.listener()
            async def event_message(self, payload: ChatMessage) -> None:
                dto = ChatMessageDto(
                    payload.id,
                    payload.chatter.id,
                    f"[{payload.chatter.name}] {payload.text}",
                )

                async with ChatIntegrator._lock:
                    ChatIntegrator._messages.append(dto)
                    await ChatIntegrator.send_messages()

                if timeout > 0:
                    asyncio.create_task(
                        ChatIntegrator._remove_after_timeout(payload.id, timeout)
                    )

            @commands.Component.listener()
            async def event_message_delete(self, payload: ChatMessageDelete) -> None:
                async with ChatIntegrator._lock:
                    ChatIntegrator._messages = [
                        m
                        for m in ChatIntegrator._messages
                        if m.message_id != payload.message_id
                    ]
                    await ChatIntegrator.send_messages()

            @commands.Component.listener()
            async def event_ban(self, payload: ChannelBan) -> None:
                async with ChatIntegrator._lock:
                    ChatIntegrator._messages = [
                        m
                        for m in ChatIntegrator._messages
                        if m.user_id != payload.user.id
                    ]
                    await ChatIntegrator.send_messages()

            @staticmethod
            async def send_messages():
                ws = ConnectionManager()
                await ws.broadcast(
                    json.dumps(
                        {"messages": [t.message for t in ChatIntegrator._messages]}
                    )
                )

            @staticmethod
            async def _remove_after_timeout(message_id: str, timeout: int) -> None:
                await asyncio.sleep(timeout)

                async with ChatIntegrator._lock:
                    before = len(ChatIntegrator._messages)

                    ChatIntegrator._messages = [
                        m
                        for m in ChatIntegrator._messages
                        if m.message_id != message_id
                    ]

                    if len(ChatIntegrator._messages) != before:
                        await ChatIntegrator.send_messages()

        @app.get("/chat/resend")
        async def chat_messages():
            await ChatIntegrator.send_messages()

        reg = ComponentsRegistry()
        reg.add_component(ChatIntegrator)

    return register
