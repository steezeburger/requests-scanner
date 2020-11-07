import networkx as nx
import pandas as pd
from asgiref.sync import sync_to_async
from discord.ext import commands
from discord.ext.commands import Context

from movie_requests.models import PlexMovie


class BaconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bacon(self, ctx: 'Context', *args):
        # munge input
        user_input = ' '.join(args)
        from_actor, to_actor = user_input.split('to ')
        from_actor = from_actor.strip()
        to_actor = to_actor.strip()

        movies = await sync_to_async(list)(PlexMovie.objects.all().values())
        df = pd.DataFrame(movies)

        graph = nx.Graph()
        added_actor = []

        def add_movie_and_actors_to_graph(movie):
            graph.add_node(movie.title,
                       type='movie',
                       color='blue')
            for actor in movie.actors:
                if actor not in added_actor:
                    graph.add_node(actor,
                               type='actor',
                               color='red' if actor == from_actor else 'green')
                    added_actor.append(actor)
                graph.add_edge(movie.title, actor)

        _ = df.apply(lambda m: add_movie_and_actors_to_graph(m), axis=1)

        try:
            path = nx.shortest_path(graph,
                                    source=from_actor,
                                    target=to_actor)

            # build message
            words_list = []

            for idx, entry in enumerate(path):
                if idx == 0:
                    # from actor
                    words_list.append(entry)
                    words_list.append('was in')
                elif idx % 2 != 0:
                    # a movie
                    words_list.append(entry)
                    words_list.append('with')
                elif idx % 2 == 0 and idx != len(path) - 1:
                    # an actor
                    words_list.append(entry)
                    words_list.append('who was in')
                elif idx == len(path) - 1:
                    # last actor
                    words_list.append(f'{entry}.')

            await ctx.message.channel.send(' '.join(words_list))
        except nx.NodeNotFound as exception:
            await ctx.message.channel.send(exception)
