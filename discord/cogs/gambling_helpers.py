import discord
from discord.ext import commands
from discord.ext.commands.converter import RoleConverter
from modules.economy import Economy
from modules.helpers import *

import math

class GamblingHelpers(commands.Cog, name='General'):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.economy = Economy()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def set(
        self,
        ctx: commands.Context,
        user_id: int=None,
        money: int=0,
        credits: int=0
    ):
        if money:
            self.economy.set_money(user_id, money)
        if credits:
            self.economy.set_credits(user_id, credits)

    @commands.command(
        brief=f"디스코드 봇 추천을 하고 ${DEFAULT_BET*B_MULT} 를 획득하세요! \n{B_COOLDOWN}시간 마다 사용 가능합니다.",
        usage="add"
    )
    @commands.cooldown(1, B_COOLDOWN*3600, type=commands.BucketType.user)
    async def add(self, ctx: commands.Context):
        amount = DEFAULT_BET*B_MULT
        self.economy.add_money(ctx.author.id, amount)
        await ctx.send(f"당신의 자산에 ${amount}를 추가했습니다!\n{B_COOLDOWN}시간 후에 다시 획득 가능합니다.")

    @commands.command(
        brief=f"돈이 뒤지게 없을 때 사용할 만한 명령어.\n1분마다 ${DEFAULT_BET*LB_MULT} 를 얻으세요.",
        usage="gugeol"
    )
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def gugeol(self, ctx: commands.Context):
        profile = self.economy.get_entry(ctx.author.id)

        currentall = profile[2] * 100 + profile[1]

        if currentall > 500:
            await ctx.send('구걸하기에는 당신의 돈이 너무 많다.')
        else:
            amount = DEFAULT_BET*LB_MULT
            self.economy.add_money(ctx.author.id, amount)
            await ctx.send(f"당신의 자산에 ${amount}를 추가했습니다!\n{1}분 후에 다시 획득 가능합니다.")

    @commands.command(
        brief="자신의 자산 확인!",
        usage="money *[@member]",
        aliases=['credits']
    )
    async def money(self, ctx: commands.Context, user: discord.Member=None):
        user = user.id if user else ctx.author.id
        user = self.client.get_user(user)
        profile = self.economy.get_entry(user.id)
        embed = make_embed(
            title=user.name,
            description=(
                '**${:,}**'.format(profile[1]) +
                '\n티켓 **{:,}**개'.format(profile[2]) +
                '\n. . .' +
                '\n낡은🕹️유압프레스 **{:,}**개'.format(profile[3])
            ),
            footer=discord.Embed.Empty
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        brief="Shows the user with the most money",
        usage="leaderboard",
        aliases=["top"]
    )
    async def leaderboard(self, ctx):
        entries = self.economy.top_entries(5)
        embed = make_embed(title='Leaderboard:', color=discord.Color.gold())
        for i, entry in enumerate(entries):
            embed.add_field(
                name=f"{i+1}. {self.client.get_user(entry[0]).name}",
                value='${:,}'.format(entry[1]),
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(
        brief="친구에게 자신의 돈을 송금!\n수수료는 20%를 떼가요~",
        usage="give *[@member]",
        aliases=['g']
    )
    async def give(self, ctx: commands.Context, user: discord.Member=None, giveamount: int = 0):
        receiveuser = self.client.get_user(user.id)
        senduser = self.client.get_user(ctx.author.id)

        seconomy = self.economy.get_entry(ctx.author.id)
        reconomy = self.economy.get_entry(user.id)

        if seconomy[1] < giveamount:
            await ctx.reply('가지고 있는 돈이 부족합니다.')
        elif seconomy[1] < 0:
            await ctx.reply('ERROR')
        else:
            ramount = math.floor(giveamount * 4 / 5)

            print(giveamount)
            print(ramount)

            self.economy.add_money(ctx.author.id, -giveamount)
            self.economy.add_money(user.id, ramount)

            embed = make_embed(
                title=f'[송금 로그]\n{senduser.name} -> {receiveuser.name} ${giveamount}',
                description=(
                    f'{senduser.name}님의 잔고 : {self.economy.get_entry(ctx.author.id)[1]}' +
                    f'\n{receiveuser.name}님의 잔고 : {self.economy.get_entry(user.id)[1]}'
                ),
                image=receiveuser.avatar_url
            )
            
            embed.set_thumbnail(url=senduser.avatar_url)
            await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(GamblingHelpers(client))