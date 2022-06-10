from sqlalchemy import Table, Column, ForeignKey

from models.db.base import Base

recipe_tags_table = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipe.id")),
    Column("tags_id", ForeignKey("tags.id")),
)
