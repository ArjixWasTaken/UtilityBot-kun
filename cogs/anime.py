import discord
from discord.ext import commands
import getanime as ga
from pages import EmbedPaginator

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Anime cog was successfully loaded!')

    # Commands
    @commands.command()
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    async def search(self, ctx, *, query):
        results = ga.search_anilist(query)
        paginator = EmbedPaginator(ctx)
        embeds = []
        for result in results:
            url = result['link']
            embed = discord.Embed(color=0x00ff00)
            embed.title = result['title']
            embed.url = url
            embed.description = result['desc']
            embed.set_thumbnail(url=result['img'])
            embed.set_author(name='Anilist', url='http://anilist.co', icon_url='https://i.imgur.com/Ak72T73.png')
            embed.add_field(name='Total Eps:', value=result['totalEpisodes'])
            embed.add_field(name='Stats:', value=result['status'])
            genre = result['genres']
            genre_links = []
            for a in genre:
                url = f'[{a}]' + f'(https://anilist.co/search/anime/{a})'.replace(' ', '%20')
                genre_links.append(url)
            genre = ',  '.join(genre_links)
            embed.add_field(name='Genre:', value=genre)
            embed.add_field(name='AniList ID:', value=result['id'], inline=False)
            embeds.append(embed)
        if len(embeds) == 1:
            await ctx.send(embed=embed)
        else:
            await paginator.run(embeds)


def setup(client):
    client.add_cog(Anime(client))
