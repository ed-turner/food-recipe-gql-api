from graphene_sqlalchemy_filter import FilterSet
from models.db.recipe import Recipe
from models.db.tags import Tags
from models.db.recipe_items import RecipeItem


class RecipeFilter(FilterSet):

    class Meta:
        model = Recipe
        fields = {
            'name': ['ilike'],
            'direction': ['in'],
            'description': ['in']
        }


class TagsFilter(FilterSet):
    class Meta:
        model = Tags
        fields = {
            'name': ['ilike'],
        }


class RecipeItemFilter(FilterSet):
    class Meta:
        model = RecipeItem
        fields = {
            'name': ['ilike'],
            'measureUnit': ['eq', 'ilike'],
            'measureQuantity': ['gte', 'lte']
        }
