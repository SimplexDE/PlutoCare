import nextcord
from nextcord.ext.commands import command, Cog
from nextcord.ext.commands import cooldown, BucketType


class Misc(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="echo",
             brief="Wiederholt deine Argumente.",
             description="",
             aliases=['say'],
             usage="echo <Text>")
    @cooldown(2, 15, BucketType.user)
    async def echo_cmd(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.trigger_typing()
        await ctx.send("> " + text + "\n\n*Gesendet von {}*".format(ctx.author.mention),
                       allowed_mentions=nextcord.AllowedMentions(everyone=False,
                                                                 users=False,
                                                                 roles=False))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


def setup(bot):
    bot.add_cog(Misc(bot))
