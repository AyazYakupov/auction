from django.conf.urls import url, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from django.conf import settings
from rest_framework import permissions

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Auction API",
        default_version='v1',
        description='Auction API Documentation',
        contact=openapi.Contact(email='a.yak.prog@gmail.com'),
    ),
    url=settings.API_URL if hasattr(settings, 'API_URL') else None,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', views.UserViewSet, basename='users')
router.register(r'animals', views.AnimalViewSet, basename='animals')
router.register(r'lots', views.LotViewSet, basename='lots')
router.register(r'bids', views.BidViewSet, basename='bids')

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url("^api-token-auth/", views.CustomAuthToken.as_view()),
    url(r"^", include(router.urls)),
]
