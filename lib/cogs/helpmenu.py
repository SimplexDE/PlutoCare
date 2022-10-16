from typing import Optional

import nextcord
from nextcord import Embed
from nextcord.ext import menus
from nextcord.ext.commands import Cog, command, cooldown, BucketType


class buildHelpmenu(menus.ListPageSource):
    def __init__(self, data, thumbnail, botname):
        super().__init__(data, per_page=5)
        self.thumbnail = thumbnail
        self.botname = botname

    async def format_page(self, menu, entries):
        embed = Embed(title="{} Hilfemenü".format(self.botname),
                      colour=nextcord.Colour.dark_purple())
        for _item in entries:
            embed.add_field(name=_item[0],
                            value="```{}```".format(_item[1]),
                            inline=False)
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()} | <> Benötigtes Feld, [<>] Optionales Feld')
        embed.set_thumbnail(
            url=self.thumbnail)
        return embed


class Helpmenu(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help",
             brief="Zeigt Hilfemenü",
             description="Zeigt Hilfemenüs für Befehle",
             aliases=['h'],
             usage="help [<Befehl>]")
    @cooldown(1, 3, BucketType.user)
    async def help(self, ctx, cmd: Optional[str]):
        if not cmd:
            fields = []
            last_cmd = ""
            for _item in self.bot.all_commands.keys():
                _item_cmd = self.bot.get_command(_item)
                name = _item_cmd.name
                usage = _item_cmd.usage
                brief = _item_cmd.brief

                enabled = _item_cmd.enabled
                hidden = _item_cmd.hidden

                if _item_cmd == last_cmd:
                    pass

                else:
                    last_cmd = _item_cmd

                    if brief is None:
                        brief = "Keine Beschreibung..."

                    if usage is None:
                        usage = name

                    elif not enabled:
                        if any([ctx.author.id in self.bot.owner_ids]):
                            usage = "Deaktiviert..."
                            fields += [(brief, usage)]
                        pass

                    elif hidden:
                        pass

                    else:
                        fields += [(brief, usage)]

            pages = menus.ButtonMenuPages(
                source=buildHelpmenu(fields, self.bot.user.avatar, self.bot.user.name),
                clear_buttons_after=True,
            )
            await pages.start(ctx)

        if cmd:
            try:
                _item = self.bot.get_command(cmd)
            except None:
                return await ctx.send("Konnte diesen Befehl nicht finden..")
            name = _item.name
            brief = _item.brief
            desc = _item.description
            hidden = _item.hidden
            cog_name = _item.cog_name
            enabled = _item.enabled
            usage = _item.usage
            aliases = _item.aliases

            text = ""
            for _alias in aliases:
                text += "`" + _alias + "`, "
            length = len(text)
            length = length - 2
            text = text[:length]

            if desc is None or "``":
                desc = "Keine Beschreibung"

            HelpMessage = Embed(title="{} Help".format(self.bot.user.name),
                                colour=nextcord.Colour.dark_purple())

            HelpMessage.add_field(name="Informationen über {}".format(name).capitalize(),
                                  value="> `{}`\n"
                                        "\n"
                                        "> Name: `{}`\n"
                                        "> Nutzung: `{}`\n"
                                        "> Aliases: {}\n".format(desc, name, usage, text),
                                  inline=False)

            if any([ctx.author.id in self.bot.owner_ids]):
                HelpMessage.add_field(name="Erweiterte Informationen über {}".format(name).capitalize(),
                                      value="> Kurz-Beschreibung: `{}`\n"
                                            "> Versteckt: `{}`\n"
                                            "> Cog-Name: `{}`\n"
                                            "> Aktiviert: `{}`\n".format(brief, hidden, cog_name, enabled),
                                      inline=False)

            HelpMessage.set_footer(
                text="{} {} | <> Benötigtes Feld, [<>] Optionales Feld".format(self.bot.user.name, self.bot.VERSION),
                icon_url=ctx.author.avatar)

            HelpMessage.set_thumbnail(url=self.bot.user.avatar)

            await ctx.send(embed=HelpMessage)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("helpmenu")


def setup(bot):
    bot.add_cog(Helpmenu(bot))
