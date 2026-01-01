from typing import TypedDict
from fastapi import Request
from fastapi.templating import Jinja2Templates


__TEMPLATES = Jinja2Templates(directory="resources/templates")
__OVERLAYS = Jinja2Templates(directory="resources/overlays")


class IndexTemplateParam(TypedDict):
    msg: str
    title: str
    heading: str


def index_template(param: IndexTemplateParam):
    return __TEMPLATES.TemplateResponse(
        "index.html",
        param,
    )


def counter_overlay(request: Request, counter: int):
    return __OVERLAYS.TemplateResponse(
        "counter.html",
        {
            "request": request,
            "counter": counter,
        },
    )
