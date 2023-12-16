import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_listings_successful(client):
    response = client.get('/listings')
    assert response.status_code == 200
    
def test_get_all_listings_failure(client):
    response = client.get('/listings')
    assert response.status_code == 200 
    assert 'error' not in response.json

def test_get_listing_by_id_success(client):
    listing_id = 323733
    response = client.get(f'/listings/{listing_id}')
    assert response.status_code == 200
    assert response.json is not None
    assert response.json['id'] == listing_id
   
def test_get_listing_by_id_not_found(client):
    listing_id = 999999 
    response = client.get(f'/listings/{listing_id}')
    assert response.status_code == 404
    assert response.json['error'] == 'Listing not found'

def test_filter_listings_success(client):
    response = client.get('/listings/filter?neighbourhood=78704&host_id=1798084&room_type=Entire home')
    assert response.status_code == 200
    assert response.json is not None
    assert isinstance(response.json, list)

def test_filter_listings_invalid_parameters_bad_request(client):
    response = client.get('/listings/filter?invalid_param=value')
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid query parameters'


def test_create_listing_successful(client):
    new_listing = {
        "id": 9999,  
        "name": "New Listing",
        "host_id": 12345,
        "host_name": "John Doe",
        "neighbourhood": 78701,
        "latitude": "30.12345",
        "longitude": "-97.98765",
        "room_type": "Entire home/apt",
        "price": 150,
        "minimum_nights": 3,
        "number_of_reviews": 0,
        "last_review": None,
        "availability_365": 365
    }

    response = client.post('/listings', json=new_listing)
    assert response.status_code == 201
    assert response.json['message'] == 'Listing created successfully'
    assert response.json['listing'] == new_listing
    assert response.json['listing']['name'] == new_listing['name']
    assert 'id' in response.json['listing']
def test_create_listing_missing_data(client):
    incomplete_listing = {
        "host_id": 54321,
        "room_type": "Private room"
    }
    response = client.post('/listings', json=incomplete_listing)
    print(response.get_data(as_text=True))  # Add this line to inspect the response content
    assert response.status_code == 400
    assert response.json['error'] == 'Incomplete data provided'



def test_search_listings_successful(client):
    search_terms = {"search_terms": ["Guesthouse", "1 bedroom", "2 beds", "1 bath"]}

    response = client.post('/listing/search', json=search_terms)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_search_listings_no_search_terms(client):
    response = client.post('/listing/search', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'Search terms not provided'

#PATCH ENDPOINT

def test_update_listing_successful(client):
    listing_id = 325889
    update_data = {
        "price": 150,
        "minimum_nights": 5,
        "availability_365": 300
    }

    response = client.patch(f'/listing/{listing_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Listing updated successfully'
    assert response.json['listing']['id'] == listing_id
    assert response.json['listing']['price'] == 150


def test_update_listing_not_found(client):
    listing_id = 99999
    update_data = {"price": 150}
    
    response = client.patch(f'/listing/{listing_id}', json=update_data)

    assert response.status_code == 404
    assert 'Listing not found' in response.get_data(as_text=True)
#DELETE ENDPOINT
def test_delete_listing_successful(client):
    id = 40285
    response = client.delete(f'/listing/{id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Listing deleted successfully'
    assert response.json['listing']['id'] == id

def test_delete_listing_not_found(client):
    id = 785643 
    response = client.delete(f'/listing/{id}')
    assert response.status_code == 404
    assert response.json['error'] == 'Listing not found'