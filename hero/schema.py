import graphene
from graphene_django import DjangoObjectType
from hero.models import Hero, SuperHeroTeam


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero


class SuperHeroTeamType(DjangoObjectType):
    class Meta:
        model = SuperHeroTeam


class Query(graphene.ObjectType):
    hero = graphene.Field(HeroType, id=graphene.Int())
    superHeroTeam = graphene.Field(SuperHeroTeamType, id=graphene.Int())
    heroes = graphene.List(HeroType)
    superHeroTeams = graphene.List(SuperHeroTeamType)

    def resolve_hero(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Hero.objects.get(pk=id)

        return None

    def resolve_superHeroTeam(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SuperHeroTeam.objects.get(pk=id)

        return None

    def resolve_heroes(self, info, **kwargs):
        return Hero.objects.all()

    def resolve_superHeroTeams(self, info, **kwargs):
        return SuperHeroTeam.objects.all()


class HeroInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    gender = graphene.String()
    mainTeam = graphene.String()


class SuperHeroTeamInput(graphene.InputObjectType):
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
        hero_instance = Hero(name=input.name, gender=input.gender, mainTeam=input.mainTeam)
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


class CreateSuperHeroTeam(graphene.Mutation):
    class Arguments:
        input = SuperHeroTeamInput(required=True)

    ok = graphene.Boolean()
    superHeroTeam = graphene.Field(SuperHeroTeamType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        heroes = []
        for hero_input in input.heroes:
            hero = Hero.objects.get(pk=hero_input.id)
            if hero is None:
                return CreateSuperHeroTeam(ok=False, superHeroTeam=None)
            heroes.append(hero)
        super_hero_team_instance = SuperHeroTeam(
          name=input.name,
          editor=input.editor
          )
        super_hero_team_instance.save()
        super_hero_team_instance.heroes.set(heroes)
        return CreateSuperHeroTeam(ok=ok, superHeroTeam=super_hero_team_instance)


class UpdateSuperHeroTeam(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = SuperHeroTeamInput(required=True)

    ok = graphene.Boolean()
    superHeroTeam = graphene.Field(SuperHeroTeamType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        super_hero_team_instance = SuperHeroTeam.objects.get(pk=id)
        if super_hero_team_instance:
            ok = True
            heroes = []
            for hero_input in input.heroes:
                hero = Hero.objects.get(pk=hero_input.id)
                if hero is None:
                    return UpdateSuperHeroTeam(ok=False, movie=None)
                heroes.append(hero)
            super_hero_team_instance.name = input.name
            super_hero_team_instance.editor = input.edit
            super_hero_team_instance.heroes.set(heroes)
            return UpdateSuperHeroTeam(ok=ok, superHeroTeam=super_hero_team_instance)
        return UpdateSuperHeroTeam(ok=ok, superHeroTeam=None)


class DeleteSuperHeroTeam(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        obj = SuperHeroTeam.objects.get(pk=id)
        if obj:
            ok = True
            obj.delete()

        return DeleteSuperHeroTeam(ok=ok)


class Mutation(graphene.ObjectType):
    create_hero = CreateHero.Field()
    update_hero = UpdateHero.Field()
    delete_hero = DeleteHero.Field()
    create_super_hero_team = CreateSuperHeroTeam.Field()
    update_super_hero_team = UpdateSuperHeroTeam.Field()
    delete_super_hero_team = DeleteSuperHeroTeam.Field()
