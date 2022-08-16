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


def test_search_by_tag(api_client):
    response = api_client.get("/recipe/search?recipe_tag=indian")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    if len(response.json()) == 2:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False


def test_search_by_name(api_client):
    response = api_client.get("/recipe/search?recipe_name=vinladoo")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    if len(response.json()) == 1:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False


def test_search_by_item_name(api_client):
    response = api_client.get("/recipe/search?recipe_item_name=curry")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    if len(response.json()) == 1:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False


def test_search_by_recipe_name_item_name(api_client):
    response = api_client.get("/recipe/search?recipe_item_name=curry&recipe_name=curry")

    if response.status_code == 200:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False

    if len(response.json()) == 1:
        pass
    else:
        LOGGER.info(f"JSON Output of response: {response.json()}")
        assert False
