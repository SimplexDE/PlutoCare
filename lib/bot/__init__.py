import asyncio
import os
import dotenv
from random import choice

import nextcord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger as log
from nextcord import Embed, Intents, Colour
from nextcord.errors import HTTPException, Forbidden
from nextcord.ext.commands import Bot as BotBase, Context
from nextcord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, \
    DisabledCommand

from ..db import db

OWNER_IDS = [
    579111799794958377,  # Simplex#7008
    587070706177802242,  # Complexity
]
MODERATOR_IDS = []
CONTRIBUTOR_IDS = [
    507517299746537472,
]
COGS = []

for file in os.listdir("./lib/cogs"):
    if file.endswith(".py"):
        if not file.startswith("-"):
            COGS += [file[:-3]]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):

    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
            # log.info("{} changed READY Status to: {}".format(cog.capitalize(), False))

    def ready_up(self, cog):
        setattr(self, cog, True)
        # log.info("{} changed READY Status to: {}".format(cog.capitalize(), True))
        log.success("Ready [{}]".format(cog.upper()))

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


dotenv.load_dotenv()

token = os.environ['TOKEN']
prefix = os.environ['PREFIX']


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = prefix
        self.VERSION = ""
        self.TOKEN = token
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.blocked = {}

        db.autosave(self.scheduler)
        super().__init__(command_prefix=prefix,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            try:
                log.info("Loading {}".format(cog))
                self.load_extension("lib.cogs.{}".format(cog))
            except Exception as e:
                log.info("Error occoured during loading of {}".format(cog))
                log.exception(e)

    def run(self, version):
        self.VERSION = version

        log.info("Starting setup...")
        self.setup()

        log.info("Initializing.")
        super().run(self.TOKEN, reconnect=True)

    async def presence_change(self):

        choices = [("nach den Blumen", nextcord.ActivityType.watching),
                   ("zum Himmel", nextcord.ActivityType.watching),
                   ("dir zu...", nextcord.ActivityType.watching),
                   ("Simplex", nextcord.ActivityType.listening),
                   ("Juox", nextcord.ActivityType.listening),
                   ("Plutocord", nextcord.ActivityType.playing)]

        sel = choice(choices)

        await bot.change_presence(status=nextcord.Status.online,
                                  activity=nextcord.Activity(
                                      type=sel[1],
                                      name="{} | {}".format(sel[0], self.VERSION)))

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("Aktuell starte ich, bitte warte einen Moment!.", delete_after=3)

    async def on_connect(self):
        await bot.change_presence(status=nextcord.Status.do_not_disturb,
                                  activity=nextcord.Activity(
                                      type=nextcord.ActivityType.playing,
                                      name="Startsequenz..."))
        log.success("Connected.")

    async def on_disconnect(self):
        log.warning("Disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Etwas ist schiefgelaufen! Bitte kontaktiere den Entwickler.")

        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, DisabledCommand):
            await ctx.send("> Dieser Befehl ist ausgeschaltet")

        elif isinstance(exc, CommandOnCooldown):
            user_id = str(ctx.message.author.id)

            if not self.blocked.get(user_id):
                self.blocked[user_id] = []

            if ctx.command.name in self.blocked[user_id]:
                return

            await ctx.send(
                f"> Dieser Befehl ist aktuell im {str(exc.type).split('.')[-1]} Cooldown.\n"
                f"> Warte noch {exc.retry_after:,.2f} Sekunden um ihn wieder auszuführen.")

            self.blocked[user_id].append(ctx.command.name)
            await asyncio.sleep(2)  # 2 Sekunden blocken
            self.blocked[user_id].remove(ctx.command.name)

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("> Überprüfe deine Befehl-Arugmente.")

        elif isinstance(exc.original, HTTPException):
            await ctx.send("> Senden der Nachricht gescheitert.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send(
                "> Mir fehlen die Benötigten Rechte für diesen Befehl.")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(1030608164367913031)
            self.scheduler.start()

            developer = ""
            # contributorList = ""
            for owner_id in OWNER_IDS:
                owner = self.get_user(owner_id)
                developer += owner.name + "#"
                developer += owner.discriminator + ", "
            developer = developer[:-2]

            embed_done = Embed(title="Ready!",
                               description="{} is ready.".format(bot.user.name),
                               colour=Colour.brand_green())

            fields = [("Developer", developer, True),
                      ("Version", "`" + self.VERSION + "`", True)]

            for name, value, inline in fields:
                embed_done.add_field(name=name,
                                     value=value,
                                     inline=inline)

            embed_done.set_footer(text="{} | {}".format(bot.user.name, self.VERSION), icon_url=bot.user.avatar)

            counter = 15
            halfcounter = round(counter / 2)

            errorsduringload = False

            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)
                counter -= 1
                if counter == halfcounter:
                    log.warning("It already took {} seconds to load.".format(halfcounter))
                if counter <= -1:
                    log.error("Errors encountered during startup, not all cogs are available.")
                    errorsduringload = True
                    break

            if errorsduringload:
                embed_done.add_field(name=":warning: Completed with errors",
                                     value="The bot started with errors,"
                                           " check console for more information",
                                     inline=False)
            else:
                embed_done.add_field(name=":white_check_mark: Completed without errors.",
                                     value="No errors during loading detected.",
                                     inline=False)

            self.scheduler.add_job(self.presence_change, CronTrigger(hour='*',
                                                                     jitter=269))
            await self.presence_change()

            log.success("Ready [{}@{}]".format(bot.user.name, self.VERSION))
            self.ready = True

            channel = self.get_channel(979750917249310720)
            await channel.send(embed=embed_done)

        else:
            log.success("Reconnected.")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
