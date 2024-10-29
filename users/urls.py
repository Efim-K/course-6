from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView

from users.views import UserCreateView, email_verification, UserResetPasswordView, ProfileView, UsersListView, \
    UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('user_list/', UsersListView.as_view(), name="user_list"),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]
