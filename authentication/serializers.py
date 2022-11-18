import re
from django.contrib.auth.models import Group
from authentication.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url',
            'uid',
            'username',
            'alt_name',
            'i_alt_name',
            'email',
            'is_staff',
            'groups'
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message="This email address is already in use"
        )]
    )
    alt_name = serializers.CharField(
        min_length=3,
        max_length=25,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message="This alternative name is already in use"
        )]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'alt_name', 'password', 'password2')

        #We can add extra validations with extra_kwargs option
        extra_kwargs = {
            'alt_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})

        return attrs

    def validate_alt_name(self, value):
        if not re.match("^[A-Za-z0-9 _-]*$", value):
            raise serializers.ValidationError("Please, use only letters and numbers")
        if User.objects.filter(i_alt_name=value.lower()).exists():
            raise serializers.ValidationError("This alternative name is already in use")
        return value

    # called when POST
    def create(self, validated_data):
        '''user = User.objects.create(
            username=validated_data['username'],
            alt_name=validated_data['alt_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        '''

        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.alt_name = validated_data['alt_name']
        user.i_alt_name = validated_data['alt_name'].lower()
        user.save()

        return user
