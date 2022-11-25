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
            raise serializers.ValidationError({"alt_name": "Please, use only letters and numbers"})
        if User.objects.filter(i_alt_name=value.lower()).exists():
            raise serializers.ValidationError({"alt_name": "This alternative name is already in use"})
        return value
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
        validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords didn't match."
            })

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({
                "old_password": "Old password is not correct"
            })
        return value

    # PUT request
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({
                "authorize": "You dont have permission to update this user."
            })

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'alt_name')
        extra_kwargs = {
            'username': {'required': True},
            'alt_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        if User.objects.exclude(pk=user.pk).filter(username=attrs['alt_name']).exists():
            raise serializers.ValidationError({"alt_name": "This alternative name is already in use."})
        return attrs

    # PUT request
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.alt_name = validated_data['alt_name']
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords didn't match."
            })

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"message": "This email does not exist."})
