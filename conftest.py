from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from auction_app.models import Profile, Animal, Lot, Bid

import pytest


@pytest.fixture()
def regular_user_client(db, valid_auth_token, regular_user=None):
    from django.test.client import Client
    auth_header_name = "HTTP_AUTHORIZATION"
    auth_header_content = "Token {}".format(valid_auth_token.key)
    client = Client(**{auth_header_name: auth_header_content}, )
    return client


@pytest.fixture()
def another_user_client(db, valid_auth_token, another_user=None):
    from django.test.client import Client

    auth_header_name = "HTTP_AUTHORIZATION"
    auth_header_content = "Token {}".format(valid_auth_token.key)
    client = Client(**{auth_header_name: auth_header_content}, )
    return client


@pytest.fixture()
def valid_auth_token(regular_user):
    token = Token.objects.create(user=regular_user)
    return token


@pytest.fixture()
def another_valid_auth_token(another_user):
    token = Token.objects.create(user=regular_user)
    return token


@pytest.fixture()
def regular_user():
    user = User.objects.create(username='regular_user', password=hashers.make_password('test'))
    Profile.objects.create(user=user, balance=100)
    return user


@pytest.fixture()
def another_user():
    user = User.objects.create(username='another_user', password=hashers.make_password('test'))
    Profile.objects.create(user=user, balance=100)
    return user


@pytest.fixture()
def pet(regular_user):
    pet = Animal.objects.create(owner=regular_user, kind=Animal.KINDS[0][0], name='pet', breed='test')
    return pet


@pytest.fixture()
def lot(regular_user, pet):
    lot = Lot.objects.create(owner=regular_user, animal=pet, price=100)
    return lot


@pytest.fixture()
def bid(another_user, lot):
    bid = Bid.objects.create(user=another_user, lot=lot, price=55)
    return bid
