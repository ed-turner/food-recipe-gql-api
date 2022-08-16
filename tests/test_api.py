import logging

LOGGER = logging.getLogger(__name__)


def test_get_recipe1(api_client):

    response = api_client.get("/recipe/get/1")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    assert response.json()['id'] == 1


def test_ping(api_client):
    """

    :param api_client:
    :return:
    """
    response = api_client.get("/health")

    assert response.status_code == 200


def test_get_recipes(api_client):
    # this breaks for no reason
    response = api_client.get("/recipe/page")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    assert len(response.json()) < 10

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
