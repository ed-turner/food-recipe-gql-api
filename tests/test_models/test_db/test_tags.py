from models.db.tags import Tags


def test_get_tag(db_session, db_data):
    tag: Tags = db_session.get(Tags, 1)

    assert not tag is None
    assert tag.name == "indian"


def test_get_tag_1_recipes(db_session, db_data):
    tag: Tags = db_session.get(Tags, 1)

    assert not tag is None
    assert len(tag.tagged_recipes) == 2
