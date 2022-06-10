

def test_get_tags(api_client):

    response = api_client.get("/")
    assert response.status_code == 200


