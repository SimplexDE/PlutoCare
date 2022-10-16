from datetime import datetime

import nextcord
from nextcord import Embed
from nextcord.ext.commands import Cog


# Still work in progress, but most of the events are in here now..

def buildembed(title: str, description: str, colour: nextcord.Colour):
    return Embed(
        title=title,
        description=description,
        colour=colour,
        timestamp=datetime.utcnow()
    )


class Log(Cog):

    def __init__(self, bot):
        self.log_channel = None
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(1031329859282141284)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:

            embed = buildembed(title="Userrollen geändert",
                               description="",
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.display_name,
                                                 after.discriminator),
                             url=after.avatar)

            fields = [()]
            currentRoles = []
            newRoles = []

            for _role in before.roles:
                currentRoles += [_role]

            for _role in after.roles:
                newRoles += [_role]

            for _role in currentRoles:  # Role removed
                if _role not in newRoles:
                    fields = [("Von Rolle entfernt", _role.mention, False)]

            for _role in newRoles:  # Role added
                if _role not in currentRoles:
                    fields = [("Zu Rolle hinzugefügt", _role.mention, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = buildembed(title="Nickname aktualisiert",
                               description="",
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.display_name,
                                                 after.discriminator),
                             url=after.avatar)

            fields = [("Vorher", before.display_name, False),
                      ("Nachher", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = buildembed(title="Nutzername aktualisiert",
                               description="",
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.display_name,
                                                 after.discriminator),
                             url=after.avatar)

            fields = [("Vorher", before.name, False),
                      ("Nachher", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.discriminator != after.discriminator:
            embed = buildembed(title="Diskriminator aktualisiert",
                               description="",
                               # If you fix this, please set description to ""
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.display_name,
                                                 after.discriminator),
                             url=after.avatar)

            fields = [("Vorher", before.discriminator, False),
                      ("Nachher", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:  # TODO (on_user_update, avatar update)
            embed = buildembed(title="Updated avatar",
                               description=":warning: **THIS DOES NOT WORK CORRECTLY**",
                               # If you fix this, please set description to ""
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.display_name,
                                                 after.discriminator),
                             url=after.avatar)

            fields = [("Before", "[[before]]({})".format("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                       False),
                      ("After", "[[after]]({})".format("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                       False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        embed = buildembed(title="Nutzer beigetreten",
                           description="",
                           colour=nextcord.Colour.green())
        embed.set_author(name="{}#{}".format(member.display_name,
                                             member.discriminator),
                         url=member.avatar)

        embed.set_footer(text=self.bot.VERSION)
        await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        embed = buildembed(title="Nutzer verlassen",
                           description="",
                           colour=nextcord.Colour.red())
        embed.set_author(name="{}#{}".format(member.display_name,
                                             member.discriminator),
                         url=member.avatar)

        embed.set_footer(text=self.bot.VERSION)
        await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            pass
        if before.content != after.content:
            embed = buildembed(title="Nachricht aktualisiert",
                               description="",
                               colour=nextcord.Colour.orange())
            embed.set_author(name="{}#{}".format(after.author.display_name,
                                                 after.author.discriminator),
                             url=after.author.avatar)

            fields = [("Channel", "<#{}>({})".format(after.channel.id, after.channel.name), False),
                      ("Nachricht-ID", after.id, False),
                      ("Vorher", before.content, False),
                      ("Nachher", after.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = buildembed(title="Nachricht gelöscht",
                               description="",
                               colour=nextcord.Colour.red())
            embed.set_author(name="{}#{}".format(message.author.display_name,
                                                 message.author.discriminator),
                             url=message.author.avatar)

            fields = [("Channel", "<#{}>({})".format(message.channel.id, message.channel.name), False),
                      ("Nachricht-ID", message.id, False),
                      ("Nachricht", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name,
                                value=value,
                                inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_bulk_message_delete(self, messages):  # todo
        pass


def setup(bot):
    bot.add_cog(Log(bot))
