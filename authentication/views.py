import base64
from django.contrib.auth.models import Group
from authentication.models import User
from django.utils import http, encoding
from django.contrib.auth import tokens
from django.template import loader
from django.core import mail, serializers
from django.contrib.sites import shortcuts
from django.conf import settings
from rest_framework import (
    permissions,
    viewsets,
    generics,
    response,
    status
)
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import (
    UserSerializer,
    GroupSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # method to get an user
    '''def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj'''


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


#CreateAPIView used for create-only endpoints only POST
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.create(
                username=serializer.validated_data['username'],
                alt_name=serializer.validated_data['alt_name'],
                i_alt_name=serializer.validated_data['alt_name'].lower(),
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])
            user.is_active = False
            user.save()
        except Exception:
            return response.Response({
                "message":"An error happened creating the user: %s"
                % e
            }, status=status.HTTP_400_BAD_REQUEST)

        token = tokens.PasswordResetTokenGenerator().make_token(user)
        user_idb64 = http.urlsafe_base64_encode(encoding.smart_bytes(user.id))
        message = loader.render_to_string('emails/account_activation.html', {
            'user': user,
            'protocol': settings.PROTOCOL,
            'domain': shortcuts.get_current_site(request).domain,
            'app_title': settings.APP_TITLE,
            "url_reset": f"/auth/activate-account/{user_idb64}/{token}/"
        })

        mail.send_mail(
            'Activate your account',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return response.Response({
            "message":"The user %s was created. Activation email sent"
                % user.username,
            "data": serializer.data
        }, status=status.HTTP_202_ACCEPTED)


class ActivationView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            user_id = http.urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=user_id)
            if not tokens.PasswordResetTokenGenerator().check_token(user, token):
                return response.Response({
                    "message":"The activation link is invalid"
                }, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()

            # generate new token
            token = RefreshToken.for_user(user)
        except Exception as e:
            return response.Response({
                "message":"An error happened trying to activate the account: %s"
                % e
            }, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({
            "message":"The %s account was activated" % user.username,
            "refresh": str(token),
            "access": str(token.access_token)
        }, status=status.HTTP_202_ACCEPTED)



class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    # Replicate method to return a custom message
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response({
            "message":"The %s password was changed" % request.user.username
        }, status=status.HTTP_202_ACCEPTED)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer

    # Replicate method to return a custom message
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response({
            "message":"The %s profile was changed" % request.user.username,
            "data": serializer.data
        }, status=status.HTTP_202_ACCEPTED)


class ForgotPasswordRequest(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validated in serializer
        users = User.objects.filter(email=serializer.data.get("email", ""))
        user = users.first()

        token = tokens.PasswordResetTokenGenerator().make_token(user)
        user_idb64 = http.urlsafe_base64_encode(encoding.smart_bytes(user.id))

        message = loader.render_to_string('emails/password_reset.html', {
            'user': user,
            'protocol': settings.PROTOCOL,
            'domain': shortcuts.get_current_site(request).domain,
            'app_title': settings.APP_TITLE,
            "url_reset": f"/auth/reset-password/{user_idb64}/{token}/"
        })

        mail.send_mail(
            'Reset your password',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return response.Response({
            "message": "The email to reset the password was sent"
        }, status=status.HTTP_200_OK)


class ResetPasswordRequest(generics.GenericAPIView):
    permission_classes = []
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = http.urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=user_id)
            if not tokens.PasswordResetTokenGenerator().check_token(user, token):
                return response.Response({
                    "message":"The reset link is invalid"
                }, status=status.HTTP_400_BAD_REQUEST)

            pwd = serializer.data.get("password")
            user.set_password(pwd)
            user.is_active = True
            user.save()

            # generate new token
            token = RefreshToken.for_user(user)
        except Exception as e:
            return response.Response({
                "message":"An error happened trying to reset the password: %s"
                % e
            }, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({
            "message":"The password for the user %s was reset"
            % user.username,
            "refresh": str(token),
            "access": str(token.access_token)
        }, status=status.HTTP_202_ACCEPTED)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return response.Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return response.Response(
                {"message":
                 "An error happened invalidating the token: %s" % e},
                status=status.HTTP_400_BAD_REQUEST
            )
