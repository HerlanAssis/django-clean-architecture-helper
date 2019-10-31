import graphene
from apps.posts.schema.query import Query as PostQuery
from apps.posts.schema.mutation import Mutation as PostMutation


class Query(
        PostQuery,
        graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(
        PostMutation,
        graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass
