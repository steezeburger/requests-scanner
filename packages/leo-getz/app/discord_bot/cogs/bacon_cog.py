import networkx as nx
import pandas as pd
from asgiref.sync import sync_to_async
from discord.ext import commands
from discord.ext.commands import Context

from movie_requests.models import PlexMovie


class BaconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Shows the number of hops connecting two actors. Names are case sensitive.',
                      usage='John Goodman to Chevy Chase',
                      help='Send !bacon John Goodman to Chevy Chase to see how many hops there are between actors. Names are case sensitive.')
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
            hops = 0

            for idx, entry in enumerate(path):
                if idx == 0:
                    # from actor
                    words_list.append(entry)
                    words_list.append('was in')
                elif idx % 2 != 0:
                    # a movie
                    hops += 1
                    words_list.append(entry)
                    words_list.append('with')
                elif idx % 2 == 0 and idx != len(path) - 1:
                    # an actor
                    words_list.append(entry)
                    words_list.append('who was in')
                elif idx == len(path) - 1:
                    # last actor
                    words_list.append(f'{entry}.')

            message = f'{from_actor} and {to_actor} are connected by {hops} hops.\n' + \
                      ' '.join(words_list)
            await ctx.message.channel.send(message)
        except nx.NetworkXNoPath as exception:
            await ctx.message.channel.send(exception)
        except nx.NodeNotFound as exception:
            await ctx.message.channel.send(exception)
