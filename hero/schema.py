import graphene
from graphene_django import DjangoObjectType
from hero.models import Hero, HeroTeam


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class HeroTeamType(DjangoObjectType):
    class Meta:
        model = HeroTeam


class Query(graphene.ObjectType):
    hero = graphene.Field(HeroType, id=graphene.Int())
    HeroTeam = graphene.Field(HeroTeamType, id=graphene.Int())
    heroes = graphene.List(HeroType)
    HeroTeams = graphene.List(HeroTeamType)

    def resolve_hero(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Hero.objects.get(pk=id)

        return None

    def resolve_heroTeam(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return HeroTeam.objects.get(pk=id)

        return None

    def resolve_heroes(self, info, **kwargs):
        return Hero.objects.all()

    def resolve_heroTeams(self, info, **kwargs):
        return HeroTeam.objects.all()


class HeroInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    gender = graphene.String()
    mainTeam = graphene.String()


class HeroTeamInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    heroes = graphene.List(HeroInput)
    editor = graphene.String()


class CreateHero(graphene.Mutation):
    class Arguments:
        input = HeroInput(required=True)

    ok = graphene.Boolean()
    hero = graphene.Field(HeroType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        hero_instance =\
            Hero(name=input.name, gender=input.gender, mainTeam=input.mainTeam)
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
            hero_instance.mainTeam = input.mainTeam
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


class CreateHeroTeam(graphene.Mutation):
    class Arguments:
        input = HeroTeamInput(required=True)

    ok = graphene.Boolean()
    HeroTeam = graphene.Field(HeroTeamType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        heroes = []
        for hero_input in input.heroes:
            hero = Hero.objects.get(pk=hero_input.id)
            if hero is None:
                return CreateHeroTeam(ok=False, HeroTeam=None)
            heroes.append(hero)
        hero_team_instance = HeroTeam(
          name=input.name,
          editor=input.editor
          )
        hero_team_instance.save()
        hero_team_instance.heroes.set(heroes)
        return\
            CreateHeroTeam(ok=ok, HeroTeam=hero_team_instance)


class UpdateHeroTeam(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = HeroTeamInput(required=True)

    ok = graphene.Boolean()
    HeroTeam = graphene.Field(HeroTeamType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        hero_team_instance = HeroTeam.objects.get(pk=id)
        if hero_team_instance:
            ok = True
            heroes = []
            for hero_input in input.heroes:
                hero = Hero.objects.get(pk=hero_input.id)
                if hero is None:
                    return UpdateHeroTeam(ok=False, movie=None)
                heroes.append(hero)
            hero_team_instance.name = input.name
            hero_team_instance.editor = input.edit
            hero_team_instance.heroes.set(heroes)
            return UpdateHeroTeam(ok=ok, HeroTeam=hero_team_instance)
        return UpdateHeroTeam(ok=ok, HeroTeam=None)


class DeleteHeroTeam(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        obj = HeroTeam.objects.get(pk=id)
        if obj:
            ok = True
            obj.delete()

        return DeleteHeroTeam(ok=ok)


class Mutation(graphene.ObjectType):
    create_hero = CreateHero.Field()
    update_hero = UpdateHero.Field()
    delete_hero = DeleteHero.Field()
    create_hero_team = CreateHeroTeam.Field()
    update_hero_team = UpdateHeroTeam.Field()
    delete_hero_team = DeleteHeroTeam.Field()
