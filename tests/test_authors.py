from flask import Flask

from pytest import fixture
from app import create_app
from json import loads


@fixture
def app_client():
    application = create_app()
    with application.test_client() as client:
        with application.app_context() as app_context:
            yield client


@fixture
def client(app: Flask):
    return app.test_client()


def test_post_author(client):
    given = {
        "author": {
            "name": "Liev Tolstói",
            "birthplace": "09-09-1828"
        }
    }

    response = client.post('/authors/', json=given)

    expected = {
        "author": {
            "id": 13,
            "name": "Liev Tolstói",
            "birthplace": "09-09-1828"
        }
    }

    assert expected == loads(response.get_data(as_text=True))


def test_get_author(client):
    response = client.get('/authors')

    expected = [
        {
            "id": 13,
            "name": "Liev Tolstói",
            "birthplace": "09-09-1828"
        }
    ]

    assert expected == loads(response.get_data(as_text=True))
