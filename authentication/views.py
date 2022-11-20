from django.contrib.auth.models import Group
from authentication.models import User
from rest_framework import permissions, viewsets, generics
from authentication.serializers import (
    UserSerializer,
    GroupSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


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


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer


#CreateAPIView used for create-only endpoints only POST
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer
