from entities.models import Entity
from rest_framework import serializers


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ['name', 'author', 'views', 'link']


class PublicEntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ['name', 'author']
