import discord
from discord.ext import commands
import asyncio
import time


class EmbedPaginator():
    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self.start_time = time.time()
        self.current_page = 0
        self.emojis = ('⏮', '◀️', '⏹', '▶️', '⏭')

    async def run(self, embeds):
        self.embeds = embeds

        if self.embeds[0].footer.text == discord.Embed.Empty:
            self.embeds[0].set_footer(text=f'({self.current_page+1}/{len(self.embeds)})')

        else:
            # Adds the text set by user plus the current_page / len(embeds)
            self.embeds[0].set_footer(text=f"{self.embeds[0].footer.text} - ({self.current_page+1}/{len(self.embeds)})")

        self.message = await self.ctx.send(embed=self.embeds[0])

        for emoji in self.emojis:
            await self.message.add_reaction(emoji)

        async def embed_footer(page):
            if self.embeds[page].footer.text == discord.Embed.Empty:
                self.embeds[page].set_footer(text=f"({page+1}/{len(self.embeds)})")

            else:
                # Prevents adding the text if already exist
                if not f"({page+1}/{len(self.embeds)})" in self.embeds[page].footer.text:
                    self.embeds[page].set_footer(text=f"{self.embeds[page].footer.text} - ({page+1}/{len(self.embeds)})")

        def check(reaction, user):
            return user == self.ctx.author and reaction.message.id == self.message.id and str(reaction.emoji) in self.emojis

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=100)

            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                return
                break

            if str(reaction.emoji) == self.emojis[0]:
                self.current_page = 0

            if str(reaction.emoji) == self.emojis[1]:
                self.current_page -= 1

                if self.current_page < 0:
                    self.current_page = 0

            if str(reaction.emoji) == self.emojis[2]:
                await self.message.clear_reactions()
                return
                break

            if str(reaction.emoji) == self.emojis[3]:
                self.current_page += 1
                if self.current_page >= len(self.embeds):
                    self.current_page -= 1  # Sets the current page back to the last page

            if str(reaction.emoji) == self.emojis[4]:
                self.current_page = len(self.embeds) - 1

            await self.message.remove_reaction(str(reaction.emoji), user)
            await embed_footer(self.current_page)
            await self.message.edit(embed=self.embeds[self.current_page])
