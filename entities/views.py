from entities.models import Entity
from rest_framework import viewsets
from entities.serializers import EntitySerializer, PublicEntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows entities to be viewed or edited.
    """
    queryset = Entity.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
          return self.queryset

        """
        Less entities returned if it's not authenticated
        """
        return Entity.objects.all()[:1]
    
    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
          return EntitySerializer
        return PublicEntitySerializer