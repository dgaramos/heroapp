import graphene
import hero.schema


class Query(hero.schema.Query, graphene.ObjectType):
    pass


class Mutation(hero.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
