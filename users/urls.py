from django.urls import path, include

from .views import SignUpView, UserListView, FollowView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("", include("rest_auth.urls")),
    path("", UserListView.as_view()),
    path("<int:user_id>/follow", FollowView.as_view()),
]