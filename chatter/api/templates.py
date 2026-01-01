import json
import os
from typing import TypedDict
from fastapi import Request, Response
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
import httpx

from fastapi.staticfiles import StaticFiles


__TEMPLATES = Jinja2Templates(directory="resources/rendered")
__OVERLAYS = Jinja2Templates(directory="resources/overlays")


def mount_assets(app) -> None:
    app.mount(
        "/assets", StaticFiles(directory="resources/rendered/assets"), name="assets"
    )


async def __lookup_template(
    request: Request,
    route: str = "/",
    state: dict = {},
):
    # Serve index.html for SPA-like frontend
    return __TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "py_route": route,
            "state": state,
        },
    )


class IndexTemplateParam(TypedDict):
    msg: str
    title: str
    heading: str


async def index_template(request: Request, state: IndexTemplateParam):
    return await __lookup_template(
        request,
        "/about",
        state,
    )


async def counter_overlay(request: Request, counter: int):
    return await __lookup_template(request, "/overlay", {"team_kill_counter": counter})
