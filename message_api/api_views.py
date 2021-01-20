from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from message_api import models, serializers


class MessageViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.counter += 1
        instance.save(update_fields=['counter'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
