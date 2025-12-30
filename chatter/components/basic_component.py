import random
import twitchio
from twitchio.ext import commands

from chatter.components.component_base import ABaseComponent, ComponentConstructor


class BaicComponent(ABaseComponent):
    # An example of listening to an event
    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        """Command that replies to the invoker with Hi <name>!

        !hi
        """
        greetings = ["Hi", "Howdy", "Was geht", "alloah"]
        for greeting in greetings:
            try:
                await ctx.reply(f"{greeting} {ctx.chatter}!")
            except:
                break

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str) -> None:
        """Command which repeats what the invoker sends.

        !say <message>
        """
        await ctx.send(message)

    @commands.command()
    async def add(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which adds to integers together.

        !add <number> <number>
        """
        await ctx.reply(f"{left} + {right} = {left + right}")

    @commands.command()
    async def choice(self, ctx: commands.Context, *choices: str) -> None:
        """Command which takes in an arbitrary amount of choices and randomly chooses one.

        !choice <choice_1> <choice_2> <choice_3> ...
        """
        await ctx.reply(
            f"You provided {len(choices)} choices, I choose: {random.choice(choices)}"
        )

    @commands.command(aliases=["thanks", "thank"])
    async def give(
        self,
        ctx: commands.Context,
        user: twitchio.User,
        amount: int,
        *,
        message: str | None = None,
    ) -> None:
        """A more advanced example of a command which makes use of the powerful argument parsing, argument converters and
        aliases.

        The first argument will be attempted to be converted to a User.
        The second argument will be converted to an integer if possible.
        The third argument is optional and will consume the rest of the message.

        !give <@user|user_name> <number> [message]
        !thank <@user|user_name> <number> [message]
        !thanks <@user|user_name> <number> [message]
        """
        msg = f"with message: {message}" if message else ""
        await ctx.send(
            f"{ctx.chatter.mention} gave {amount} thanks to {user.mention} {msg}"
        )


def social_component_factory(socials: dict[str, str]) -> ComponentConstructor:
    discord = socials.get("discord")

    class SocialComponent(ABaseComponent):
        @commands.group(invoke_fallback=True)
        async def socials(self, ctx: commands.Context) -> None:
            """Group command for our social links.

            !socials
            """
            await ctx.send(",\n".join(f"{k}: {v}" for (k, v) in socials.items()))

        @socials.command(name="discord")
        async def socials_discord(self, ctx: commands.Context) -> None:
            """Sub command of socials that sends only our discord invite.

            !socials discord
            """
            if discord is None:
                return
            await ctx.send(discord)

    return SocialComponent
