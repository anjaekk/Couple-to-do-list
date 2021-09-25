from django.urls import path, include

from .views import SignUpView, UserLoginView, UserLogoutView, UserListView, FollowView, UserDetailView, FollowerLisetView, FollowingLisetView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("login", UserLoginView.as_view()),
    path("logout", UserLogoutView.as_view()),
    path("", UserListView.as_view()),
    path("<int:pk>", UserDetailView.as_view({'get': 'retrieve'})),
    path("<int:user_id>/follow", FollowView.as_view()),
    path("<int:user_id>/follower", FollowerLisetView.as_view()),
    path("<int:user_id>/following", FollowingLisetView.as_view()),
]