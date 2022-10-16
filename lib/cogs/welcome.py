from discord.ext.commands import Cog
from datetime import datetime
from loguru import logger as log

from ..db import db


class Welcome(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.welcome = 1030808110891286609

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):

        early_member_role = 1031338245327433829

        await self.bot.get_channel(self.welcome).send("Willkommen {}.".format(member.mention))
        if datetime.today() <= datetime(2022, 11, 30, hour=17):
        #     member.add_roles(early_member_role, reason="Joined before 17.11.2022")
            await self.bot.get_channel(self.welcome).send("Du kannst dir die <@&{}> Rolle abholen, da du vor dem 30.11.2022 gejoint bist!\nGehe dazu einfach in den Support und sende den Link dieser Nachricht.".format(early_member_role))
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        # await self.bot.get_channel(self.welcome).send("{} ist gegan".format(member.name))
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)


def setup(bot):
    bot.add_cog(Welcome(bot))
