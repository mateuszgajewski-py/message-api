from django.urls import include, path
from rest_framework import routers

from . import api_views

router = routers.SimpleRouter()
router.register(r'message', api_views.MessageViewSet, basename="message")

urlpatterns = [
    path(r'', include(router.urls))
]
