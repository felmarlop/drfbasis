from django.urls import path
from authentication.views import (
  RegisterView,
  ChangePasswordView,
  UpdateProfileView,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  LogoutView
)
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('register/', RegisterView.as_view(),
         name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
    path('forgot-password/', ForgotPasswordRequest.as_view(),
         name='auth_forgot_password'),
    path("reset-password/<uidb64>/<token>/", ResetPasswordRequest.as_view(),
         name="reset_password"),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
