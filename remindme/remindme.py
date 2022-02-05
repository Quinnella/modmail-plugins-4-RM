from discord.ext import commands
from discord.ext import tasks
import discord

import time
import random
import string

ref_rate = 5  # Updated to s/r (times per sec)


def get_id():
    return ''.join(
        [str(random.choice(' '.join(string.ascii_lowercase).split(" ") + list(range(10)))) for _ in range(10)])


class ReminderPlugin(commands.Cog):
    """
    Set Reminders
    """
    
    
    def __init__(self, bot):
        self.bot = bot
        self.data = {}

        self._check_loop.start()

    def cog_unload(self):
        self._check_loop.cancel()

    @commands.command(aliases=["reminder"])
    async def remindme(self, ctx, description, *duration):
        """
        create a reminder
        """
        
        d = time.time() + sum([int(d[0]) * {"m": 60, "h": 3600, "d": 86400, "s": 1, "w": 604800}[d[-1].lower()]
                               for d in duration])

        # Time math only supports single integer, update 4 empty split loop
        # Add If not in keys, value = 0

        i = get_id()

        self.data[i] = {"end": d, "author": ctx.author, "description": description, "id": i,
                        "reference": ctx.message.jump_url}

        await ctx.send(embed=discord.Embed(description=f"Alright, I'Il remind you at `{time.ctime(d)}`.",
                                           colour=self.bot.main_color))

    @commands.command()
    async def reminddelay(self, ctx):
        """
        delay a reminder.
        """
                                           
                                           
        await ctx.send(embed=discord.Embed(description="Your reminders max delay time is currently `{} ms`.".
                                           format(round((1 / ref_rate) * 100), ),
                                           colour=self.bot.main_color))

    @tasks.loop(seconds=1 / ref_rate)
    async def _check_loop(self):
        for g in [g for g in self.data.values() if time.time() >= float(g["end"])]:

            embed = discord.Embed(description="**Reminder:**\r\r`{}`".format(g["description"]),
                                  colour=discord.Colour.green())
            embed.add_field(name="Message:", value="[Click here]({})".format(g["reference"]))

            embed.set_footer(text="Reminder ID: {}".format(g["id"]))

            await g["author"].send(embed=embed)
            del self.data[g["id"]]


def setup(bot):
    bot.add_cog(ReminderPlugin(bot))

