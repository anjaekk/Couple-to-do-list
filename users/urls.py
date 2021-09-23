from django.urls import path, include

from .views import SignUpView, UserListView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("", include("rest_auth.urls")),
    path("", UserListView.as_view())
]