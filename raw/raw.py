import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class RawPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _error(self, msg):
        return discord.Embed(description="** " + msg + " **",
                             color=discord.Color.red())

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def raw(self, ctx, msg: int=None):
        if msg is None:
            return await ctx.send(embed=self._error(msg="Please provide a message ID."))
        
        try:
            msg = await ctx.fetch_message(msg)
        except commands.CommandInvokeError:
            return await ctx.send(embed=self._error(msg="Invalid message ID provided."))
        
        if not msg.embeds:
            return await ctx.send(embed=self._error(msg="Please provide the message ID of an embedded message."))

        await ctx.send(f"``` {msg.embeds[0].description} ```")
        

def setup(bot):
    bot.add_cog(RawPlugin(bot))
