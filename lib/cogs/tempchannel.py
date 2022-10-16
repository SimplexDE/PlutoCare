import asyncio
from datetime import datetime

from nextcord.ext.commands import Cog
from loguru import logger as log

global messagecache


class TempChannel(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voiceC = {}

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel is not None:
            if after.channel.id == 1030922503075405904:
                categ = after.channel.category
                guild = after.channel.guild
                reason = "Create Tempchannel for {}".format(member.name)

                try:
                    chn = await guild.create_voice_channel("🎤→{}".format(member.name),
                                                           # reason=reason,
                                                           category=categ)
                    self.voiceC[chn.id] = member.id
                except Exception as e:
                    log.error("Error during creation of tempchannel")
                    log.debug(e)
                    return False
                try:
                    await member.move_to(chn, reason=reason)
                except Exception as e:
                    log.error("Error during move")
                    chn.delete()
                    log.debug(e)

        if before.channel is not None:
            if before.channel.id in self.voiceC and len(before.channel.members) == 0:
                await before.channel.delete()

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("tempchannel")


def setup(bot):
    bot.add_cog(TempChannel(bot))
