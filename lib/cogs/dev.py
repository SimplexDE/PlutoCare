import asyncio
from typing import Optional

import nextcord
from loguru import logger as log
from nextcord import Embed, HTTPException

from nextcord.ext.commands import Cog, command
from lib.checks import is_dev


class Dev(Cog):

    def __init__(self, bot):
        self.log_channel = None
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(1031329859282141284)
            self.bot.cogs_ready.ready_up("dev")

    @command(name="modulemanager",
             brief="Modul-Managment",
             # description="",
             aliases=['mm', 'm'],
             usage="modulemanager <Aktion> <Cog> [<Kategorie>]",
             hidden=True)
    @is_dev()
    async def modulemanager(self, ctx, action: str, cog: str, category: Optional[str]):

        message_process = None
        message_done = None
        message = None

        no_error = ":green_circle:"
        error = ":red_circle:"
        unk = ":orange_circle:"

        status_msg = "`Aktion`: **{}**\n" \
                     "`Datei`: **{}**\n\n" \
                     "`Gültigkeit`: **{}**"
        status_msg_categ = "`Aktion`: **{}**\n" \
                           "`Datei`: **{}**\n" \
                           "`Kategorie`: **{}**\n\n" \
                           "`Gültigkeit`: **{}**"
        title_msg = "Module-Manager | Tool"

        blocked = False
        error_during_action = False
        error_before_action = False

        message_process = Embed(title=title_msg,
                                description=status_msg.format(
                                    action,
                                    cog,
                                    unk),
                                colour=nextcord.Colour.orange())
        message = await ctx.send(embed=message_process)

        if action.lower() in ("load", "unload", "reload"):

            path = "lib.cogs."

            if action.lower() == "load":
                try:
                    if category:
                        self.bot.load_extension(path + category + "." + cog)
                    if not category:
                        self.bot.load_extension(path + cog)
                except Exception as e:
                    log.error(e)
                    blocked = True
                    error_during_action = True

            elif action.lower() == "unload":
                try:
                    if category:
                        self.bot.unload_extension(path + category + "." + cog)
                    if not category:
                        self.bot.unload_extension(path + cog)
                except Exception as e:
                    log.error(e)
                    blocked = True
                    error_during_action = True

            elif action.lower() == "reload":
                try:
                    if category:
                        self.bot.reload_extension(path + category + "." + cog)
                    if not category:
                        self.bot.reload_extension(path + cog)
                except Exception as e:
                    log.error(e)
                    blocked = True
                    error_during_action = True

        else:
            blocked = True
            error_before_action = True

        if blocked:

            if error_during_action:
                action += " - {}".format(error)
                cog += " - {}".format(unk)
                if category:
                    category += " - {}".format(unk)

            if error_before_action:
                action += " - {}".format(no_error)
                cog += " - {}".format(error)
                if category:
                    category += " - {}".format(unk)

            if category:
                message_done = Embed(title=title_msg,
                                     description=status_msg_categ.format(
                                         action,
                                         cog,
                                         category,
                                         error),
                                     colour=nextcord.Colour.brand_red())

            if not category:
                message_done = Embed(title=title_msg,
                                     description=status_msg.format(
                                         action,
                                         cog,
                                         error),
                                     colour=nextcord.Colour.brand_red())

        else:
            if category:
                message_done = Embed(title=title_msg,
                                     description=status_msg_categ.format(
                                         action,
                                         cog,
                                         category,
                                         no_error),
                                     colour=nextcord.Colour.brand_green())

            if not category:
                message_done = Embed(title=title_msg,
                                     description=status_msg.format(
                                         action,
                                         cog,
                                         no_error),
                                     colour=nextcord.Colour.brand_green())

        await message.edit(embed=message_done)

    @command(name="devecho",
             brief="Siehe ECHO Befehl.",
             # description="",
             aliases=['devsay'],
             usage="devecho <Channel-ID> <Text>",
             hidden=True)
    @is_dev()
    async def devecho_cmd(self, ctx, channel_id: nextcord.TextChannel, *, text):
        await ctx.message.delete()
        chn = channel_id
        await chn.trigger_typing()
        await chn.send(text,
                       allowed_mentions=nextcord.AllowedMentions(everyone=True,
                                                                 users=True,
                                                                 roles=True))

    @command(name="listservers",
             brief="List servers",
             usage="listservers",
             hidden=True,
             disabled=True)
    @is_dev()
    async def listservers_cmd(self, ctx):
        emb = Embed(title="Gildenliste", description="LOL")
        for guild in self.bot.guilds:
            emb.add_field(name=guild.name,
                          value="Owner: {}\nID: {}\nMembers: {}\nHuman Members: 0".format(guild.owner,
                                                                                          guild.id,
                                                                                          guild.member_count))
        await ctx.send(embed=emb)

    @command(name="getserver",
             hidden=True,
             disabled=True)
    @is_dev()
    async def getserver_cmd(self, ctx, serverid):
        for guild in self.bot.guilds:
            search = "{}".format(guild.id)
            if serverid == search:
                OWNER = guild.owner
                MEMBERS = guild.member_count
                NAME = guild.name

                permissionList = ""

                emb_1 = Embed(title="Inspecting `{}`... | Standard Information".format(NAME))
                emb_1.add_field(name="Owner", value="Name & Tag: {}".format(OWNER))
                emb_1.add_field(name="Membercount", value="{}".format(MEMBERS))
                emb_1.add_field(name="Bot-Permissions", value=permissionList)

                emb_2 = Embed(title="Inspecting {}... | Detailed Information".format(NAME))

                featureList = ""
                emojiList = ""
                for feature in guild.features:
                    featureList += "{}, ".format(feature)
                for emoji in await guild.fetch_emojis:
                    emojiList += "{}, ".format(emoji)

                fields = [{"name": "Server ID", "value": guild.id, "inline": False},
                          {"name": "MFA Level", "value": guild.mfa_level, "inline": False},
                          {"name": "Features", "value": featureList, "inline": False},
                          {"name": "Emojis", "value": emojiList, "inline": False},
                          ]
                for field in fields:
                    try:
                        emb_2.add_field(name=field["name"], value=field["value"], inline=field["inline"])
                    except Exception as e:
                        emb_2.add_field(name="This Field failed...", value=e, inline=False)
                await ctx.send(embed=emb_1)
                await ctx.send(embed=emb_2)

    command(name="leaveserver",
            hidden=True,
            disabled=True)
    is_dev()

    async def leaveserver_cmd(self, ctx, serverid):
        for guild in self.bot.guilds:
            if guild == serverid:
                try:
                    await guild.leave
                    await ctx.send("Success!\n\nI left server {}".format(guild.name))
                except HTTPException as e:
                    await ctx.send("Failed")


def setup(bot):
    bot.add_cog(Dev(bot))
