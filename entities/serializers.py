from entities.models import Entity
from rest_framework import serializers


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ['name', 'author', 'views', 'link']
        # fields = '__all__' to return all fields
        # read_only_fields = ['name'] same as editable=False in the model field

    # Validations are entirely done in serializers
    def validate_name(self, value):
        if ' ' not in value.lower():
            raise serializers.ValidationError("error message")
        return value
    
    def validate(self, data):
        if int(data['views']) < 0:
            raise serializers.ValidationError("finish must occur after start")
        return data
    
    # Methods to create and update entities can be overrided
    '''def create(self, validated_data):
        return Entity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.views = validated_data.get('views', instance.views)
        instance.save()
        return instance'''


class PublicEntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ['name', 'author']
