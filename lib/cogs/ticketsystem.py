import asyncio
from datetime import datetime
import json
import random

from loguru import logger as log
import nextcord
from nextcord.ext.commands import Cog, command, cooldown, BucketType
from ..checks import is_dev

def generate_name(length):
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"

    use = lower_case + numbers
    length = length

    out = "".join(random.sample(use, length))


    return out

class Ticket():

        async def create(self, member: nextcord.Member, reason="Kein Grund angegeben"):

            with open(".\lib\json\support\channels.json") as f:
                data = json.load(f)

            name = generate_name(8)

            try:
                while name == data[str(name)]:
                    name = generate_name(8)
                    if name != data[str(name)]:
                        break
            except:
                pass

            ticket = str(name)

            if not data.get(ticket):
                data[ticket] = {}

            ticket_chan = await nextcord.Guild.create_text_channel(self.bot.guild,
                                                                name=ticket, category=nextcord.utils.get(self.bot.guild.categories, id=1031320994205409301),
                                                                reason="{} opened a ticket".format(member))
            
            overwrite = ticket_chan.overwrites_for(member)
            overwrite.read_messages = True

            await ticket_chan.set_permissions(member, overwrite=overwrite)

            data[ticket]["CHANNEL_ID"] = ticket_chan.id
            data[ticket]["REASON"] = reason
            data[ticket]["curr_state"] = "OPEN"
            data[ticket]["curr_owner"] = member.id
            data[ticket]["claimed_by"] = None

            msg = await ticket_chan.send("> Ticket eröffnet von {}.\n> Grund: `{}`".format(member.mention, reason))
            await msg.pin()
            await ticket_chan.purge(limit=1)

            with open(".\lib\json\support\channels.json", "w+") as f:
                json.dump(data, f, indent=4)

            return
            
        async def close(self, ticket, reason):
            with open(".\lib\json\support\channels.json") as f:
                data = json.load(f)

            ticket = str(ticket.name)

            if not data.get(ticket):
                data[ticket] = {}
            
            ticket_chan = nextcord.Guild.get_channel(self.bot.guild, data[ticket]["CHANNEL_ID"])
            # data[ticket]["curr_state"]
            # data[ticket]["curr_owner"]
            # data[ticket]["REASON"]
            data[ticket]["claimed_by"] = member.id

            with open(".\lib\json\support\channels.json", "w+") as f:
                json.dump(data, f, indent=4)

        async def open(self, ticket):
            return
        
        async def claim(self, ticket, member):
            with open(".\lib\json\support\channels.json") as f:
                data = json.load(f)

            ticket = str(ticket.name)

            if not data.get(ticket):
                data[ticket] = {}
            
            ticket_chan = nextcord.Guild.get_channel(self.bot.guild, data[ticket]["CHANNEL_ID"])
            # data[ticket]["curr_state"]
            # data[ticket]["curr_owner"]
            # data[ticket]["REASON"]
            data[ticket]["claimed_by"] = member.id

            with open(".\lib\json\support\channels.json", "w+") as f:
                json.dump(data, f, indent=4)

            await ticket_chan.send("Dieses Ticket wird von {} bearbeitet.".format(member.name))

            return
        
        async def unclaim(self, ticket, member):
            with open(".\lib\json\support\channels.json") as f:
                data = json.load(f)

            ticket = str(ticket.name)

            if not data.get(ticket):
                data[ticket] = {}
            
            ticket_chan = nextcord.Guild.get_channel(self.bot.guild, data[ticket]["CHANNEL_ID"])
            # data[ticket]["curr_state"]
            # data[ticket]["curr_owner"]
            # data[ticket]["REASON"]
            data[ticket]["claimed_by"] = None

            with open(".\lib\json\support\channels.json", "w+") as f:
                json.dump(data, f, indent=4)

            await ticket_chan.send("{} hat dieses Ticket freigegeben.".format(member.name))

            return
        
        async def delete(self, member, ticket, reason="Kein Grund angegeben"):
            with open(".\lib\json\support\channels.json") as f:
                data = json.load(f)

            ticket = str(ticket.name)

            if not data.get(ticket):
                data[ticket] = {}
            
            ticket_chan = nextcord.Guild.get_channel(self.bot.guild, data[ticket]["CHANNEL_ID"])
            # data[ticket]["curr_state"]
            ticket_owner = nextcord.Guild.get_member(self.bot.guild, data[ticket]["curr_owner"])
            ticket_reason = data[ticket]["REASON"]
            # data[ticket]["claimed_by"]

            await ticket_chan.delete()

            # todo fix this shit and make it work
            # embed = nextcord.Embed(title="Ticket `{}` wurde geschlossen".format(ticket),
            #                         #colour=nextcord.Colour(nextcord.Colour.dark_gold),
            #                            # timestamp=datetime.now
            #     )
            # embed.add_field(name="Dein Ticket Grund war:", value="> **" + ticket_reason + "**", inline=False)
            # embed.add_field(name="Dein Ticket wurde geschlossen von", value="> **" + member.name + "**", inline=False)
            # embed.add_field(name="Der Schließungsgrund ist:", value="> **" + reason + "**", inline=False)

            # embed.set_footer(text="Plutocord Supportsystem", icon_url=nextcord.Guild._icon)

            # await ticket_owner.send("HEY LISTEN!")
            # await ticket_owner.send(embed=embed)


            with open(".\lib\json\support\channels.json", "w+") as f:
                data.pop(ticket)
                json.dump(data, f, indent=4)

            return

class TicketSystem(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    #@is_dev()
    @cooldown(1, 1, BucketType.user)
    async def create_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await Ticket.create(self, ctx.author, reason)

        return
    
    @command()
    #@is_dev()
    @cooldown(1, 1, BucketType.user)
    async def claim_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await Ticket.claim(self, ctx.message.channel, ctx.author)

        return

    @command()
    #@is_dev()
    @cooldown(1, 1, BucketType.user)
    async def unclaim_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await Ticket.unclaim(self, ctx.message.channel, ctx.author)

        return

    @command()
    #@is_dev()
    @cooldown(1, 1, BucketType.user)
    async def close_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await Ticket.close(self, ctx.message.channel, reason)

        return

    @command()
    #@is_dev()
    @cooldown(1, 1, BucketType.user)
    async def open_ticket(self, ctx):
        await ctx.message.delete()
        await Ticket.open(self, ctx.message.channel)

        return

    @command()
    #@is_dev()
    @cooldown(1, 1,  BucketType.user)
    async def delete_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await Ticket.delete(self, ctx.author, ctx.message.channel, reason)

        return
   
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ticketsystem")
            

def setup(bot):
    bot.add_cog(TicketSystem(bot))
