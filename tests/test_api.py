import json


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

    assert len(response.json()["data"]["tags"]["edges"]) == 1, response.content


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

    try:
        assert len(response.json()["data"]["recipes"]["edges"]) == 2, response.content
    except TypeError:
        raise AssertionError(response.json()["errors"])
