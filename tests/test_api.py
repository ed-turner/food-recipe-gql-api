from graphene.relay.node import to_global_id


def test_get_recipe1(api_client):

    global_id = to_global_id("RecipeObjectType", 1)
    _q = """
        {
            node(id: "%s") {
                ... on RecipeObjectType {
                    id
                }
            }
        }
        """ % global_id

    response = api_client.post("/", json={"query": _q})

    assert response.status_code == 200

    assert response.json().get("errors", None) is None, response.json()["errors"][0]

    try:
        assert response.json()["data"]["node"]["id"] == global_id, response.content
    except TypeError:
        raise AssertionError(response.json()["errors"])


def test_get_recipes(api_client):

    _q = """
        {
            recipes
                {
                    edges {
                        node {
                            id
                        }
                    }
                }
        }
        """

    response = api_client.post("/", json={"query": _q})

    assert response.status_code == 200

    assert response.json().get("errors", None) is None, response.json()["errors"][0]

    try:
        assert len(response.json()["data"]["recipes"]["edges"]) == 2, response.content
    except TypeError:
        raise AssertionError(response.json()["errors"])


def test_get_tags(api_client):

    _q = """
    {
            tags
            {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """

    response = api_client.post("/", json={"query": _q})

    assert response.status_code == 200
    assert response.json().get("errors", None) is None, response.json()["errors"]

    assert len(response.json()["data"]["tags"]["edges"]) == 1, response.content
