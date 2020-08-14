from rest_framework import viewsets
from django.contrib.auth.models import User
from . import models
from . import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .authentication import CustomTokenAuthentication
from rest_framework.decorators import action
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.db import transaction


class CustomAuthToken(ObtainAuthToken):

    @swagger_auto_schema(request_body=ObtainAuthToken.serializer_class)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects
    http_method_names = ['get', 'post']


class AnimalViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    serializer_class = serializers.AnimalSerializer
    queryset = models.Animal.objects
    http_method_names = ['get', 'post', 'put']

    @action(url_path='self', detail=False)
    def self_list(self, request):
        animals = self.queryset.filter(owner=request.user).all()
        serialized = self.serializer_class(animals, many=True)
        return Response(serialized.data)


class LotViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    serializer_class = serializers.LotSerializer
    queryset = models.Lot.objects
    http_method_names = ['get', 'post']

    @action(url_path='self', detail=False)
    def self_list(self, request):
        lots = self.queryset.filter(owner=request.user).all()
        serialized = self.serializer_class(lots, many=True)
        return Response(serialized.data)

    @swagger_auto_schema(
        responses={201: serializers.LotSerializer},
        request_body=serializers.LotSerializer,
    )
    def create(self, request, *args, **kwargs):
        lot = self.serializer_class(data=request.data)
        lot.is_valid(raise_exception=True)
        if request.user != lot.validated_data['animal'].owner:
            msg = _('This animal is not your')
            raise exceptions.ErrorDetail(msg)
        self.queryset.create(owner=request.user, **lot.validated_data)
        return Response(lot.data)


class BidViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    serializer_class = serializers.BidSerializer
    queryset = models.Bid.objects
    http_method_names = ['get', 'post']

    @action(url_path='self', detail=False)
    def self_list(self, request):
        bids = self.queryset.filter(user=request.user)
        serialized = self.serializer_class(bids, many=True)
        return Response(serialized.data)

    @swagger_auto_schema(
        responses={201: serializers.BidSerializer},
        request_body=serializers.BidSerializer,
    )
    def create(self, request, *args, **kwargs):
        bid = self.serializer_class(data=request.data)
        bid.is_valid(raise_exception=True)
        if request.user == bid.validated_data['lot'].animal:
            msg = _('Animal owner cannot buy his animal')
            raise exceptions.ErrorDetail(msg)
        if request.user.profile.balance < bid.validated_data['price']:
            msg = _("Don't have money enough for create this bid")
            raise exceptions.ErrorDetail(msg)

        self.queryset.create(user=request.user, **bid.validated_data)
        return Response(bid.data)

    @swagger_auto_schema(
        responses={200: 'The animal was sold'},
    )
    @action(url_path='accept', detail=True, methods=['post'])
    def accept_bid(self, request, pk):
        bid = self.queryset.get(pk=pk, lot__owner=request.user)
        with transaction.atomic():
            bid.lot.animal.owner = bid.user
            bid.lot.animal.owner.save()
            request.user.profile.balance = request.user.profile.balance + bid.price
            request.user.profile.save()
            bid.user.profile.balance = bid.user.profile.balance - bid.price
            bid.user.profile.save()
            bid.lot.delete()
            bid.delete()
        msg = _('The animal was sold')
        return Response(msg)
