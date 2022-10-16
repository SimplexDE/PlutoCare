from nextcord.ext.commands import Context, check
from loguru import logger as log

from lib.bot import OWNER_IDS

STAFF = int(1030801510222807091)
DEV = int(579111799794958377)
BOT = int(1025533293636112404)


def is_staff():
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild:
            return False

        return STAFF in ctx.author._roles  # type: ignore

    # print("DEBUG: is_staff check was called.")
    # log.debug("is_staff check was called")
    return check(predicate)


def is_dev():
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild:
            return False

        return DEV == ctx.author.id  # type: ignore

    # print("DEBUG: is_staff check was called.")
    # log.debug("is_dev check was called")
    return check(predicate)


def is_bot():
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild:
            return False

        return BOT == ctx.author.id  # type: ignore

    # print("DEBUG: is_staff check was called.")
    # log.debug("is_bot check was called")
    return check(predicate)
