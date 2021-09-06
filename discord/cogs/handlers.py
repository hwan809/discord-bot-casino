import discord
from discord.ext import commands
from discord.ext.commands.errors import *
from modules.helpers import PREFIX, InsufficientFundsException


class Handlers(commands.Cog, name='handlers'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user.name + " is ready")
        try:
            await self.client.change_presence(
                activity=discord.Game(f"바체바체봇 | {PREFIX}help")
                )
        except:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, CommandInvokeError):
            await self.on_command_error(ctx, error.original)
        
        elif isinstance(error, CommandNotFound):
            await ctx.invoke(self.client.get_command('help'))

        elif isinstance(error, (MissingRequiredArgument,
                                TooManyArguments, BadArgument)):
            await ctx.invoke(self.client.get_command('help'), ctx.command.name)

        elif isinstance(error, (UserNotFound, MemberNotFound)):
            await ctx.send(f"`{error.argument}`은 무엇인가요 ..?")

        elif isinstance(error, MissingPermissions):
            await ctx.send("권한이 있어야 합니다 : " + 
            ", ".join([f'`{perm}`' for perm in error.missing_perms]))

        elif isinstance(error, BotMissingPermissions):
            await ctx.send("저는 권한이 있어야 합니다 : " +
            ", ".join([f'`{perm}`' for perm in error.missing_perms]))

        elif isinstance(error, InsufficientFundsException):
            await ctx.invoke(self.client.get_command('money'))

        elif isinstance(error, CommandOnCooldown):
            s = int(error.retry_after)
            s = s % (24 * 3600)
            h = s // 3600
            s %= 3600
            m = s // 60
            s %= 60
            await ctx.send(f'`{h}시간 {m}분 {s}초 남았습니다!`\n한국 디스코드봇 리스트의 API : TODO')
        
        else:
            raise error

def setup(client: commands.Bot):
    client.add_cog(Handlers(client))