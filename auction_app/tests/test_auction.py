from auction_app.models import Animal, Bid
from django.contrib.auth.models import User


def test_create_lot(regular_user_client, pet):
    data = {'price': 100, 'animal': pet.id}
    response = regular_user_client.post('/api/lots', data=data, )
    assert response.status_code == 200
    assert Animal.objects.get(pk=pet.id)


def test_create_bid(another_user_client, lot):
    data = {'price': 55, 'lot': lot.id}
    response = another_user_client.post('/api/bids', data=data)
    assert response.status_code == 200
    assert Bid.objects.filter(lot=lot).first()


def test_accept_bid(regular_user_client, regular_user, another_user, bid):
    response = regular_user_client.post(f'/api/bids/{bid.id}/accept')
    assert response.status_code == 200
    regular_user.refresh_from_db()
    another_user.refresh_from_db()
    assert regular_user.profile.balance == 155
    assert another_user.profile.balance == 45
    assert regular_user.lot_set.count() == 0
    assert another_user.bids.count() == 0
