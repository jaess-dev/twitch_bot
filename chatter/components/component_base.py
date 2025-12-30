import typing
from twitchio.ext import commands

from abc import ABC


class ABaseComponent(
    ABC,
    commands.Component,
):
    # An example of a Component with some simple commands and listeners
    # You can use Components within modules for a more organized codebase and hot-reloading.

    def __init__(self, bot: commands.AutoBot) -> None:
        # Passing args is not required...
        # We pass bot here as an example...
        self.bot = bot


ComponentConstructor = typing.Callable[[commands.AutoBot], ABaseComponent]
