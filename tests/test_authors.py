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


def test_post_author(app_client):
    
    response = app_client.get('/products/')
    print(response.get_json())
    
    assert 1 == 2 
    #expected == loads(response.get_data(as_text=True))


#def test_get_author(client):
#    response = client.get('/authors')
#    
#    expected = [
#        {
#            "id": 1,
#            "name": "Liev Tolstói",
#            "birthplace": "09-09-1828"
#        }
#    ]
#
#    assert expected == loads(response.get_data(as_text=True))