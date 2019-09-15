import graphene
from graphene_django import DjangoObjectType
from hero.models import Hero


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class Query(graphene.ObjectType):
    hero = graphene.Field(HeroType, id=graphene.Int())
    heroes = graphene.List(HeroType)

    def resolve_hero(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Hero.objects.get(pk=id)

        return None

    def resolve_heroes(self, info, **kwargs):
        return Hero.objects.all()


class HeroInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    gender = graphene.String()
    movie = graphene.String()


class CreateHero(graphene.Mutation):
    class Arguments:
        input = HeroInput(required=True)

    ok = graphene.Boolean()
    hero = graphene.Field(HeroType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        hero_instance = Hero(name=input.name, gender=input.gender, movie=input.movie)
        hero_instance.save()
        return CreateHero(ok=ok, hero=hero_instance)


class UpdateHero(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = HeroInput(required=True)

    ok = graphene.Boolean()
    hero = graphene.Field(HeroType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        hero_instance = Hero.objects.get(pk=id)
        if hero_instance:
            ok = True
            hero_instance.name = input.name
            hero_instance.gender = input.gender
            hero_instance.movie = input.movie
            hero_instance.save()
            return UpdateHero(ok=ok, hero=hero_instance)
        return UpdateHero(ok=ok, hero=None)


class DeleteHero(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        obj = Hero.objects.get(pk=id)
        if obj:
            ok = True
            obj.delete()

        return DeleteHero(ok=ok)


class Mutation(graphene.ObjectType):
    create_hero = CreateHero.Field()
    update_hero = UpdateHero.Field()
    delete_hero = DeleteHero.Field()
