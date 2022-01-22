from os import environ

from nextcord.ext.commands import Context, check


STAFF = 922228778279763968


def is_staff():
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild: return False

        return STAFF in ctx.author._roles  # type: ignore
    return check(predicate)