from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSignupSerializer, UserListSerializer, UserDetailSerializer, FollowListSerializer, FollowUserSerializer
from .models import Follow

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"message":"SUCCESS"}, status = status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class FollowView(views.APIView):
    def post(self, request, user_id):
        user = generics.get_object_or_404(User, id=user_id)

        if user.follower.filter(follower_id = request.user.id).exists(): 
            user.follower.get(follower_id = request.user.id).delete()
            return Response({"message":"UNFOLLOWING"}, status = status.HTTP_200_OK)
        Follow.objects.create(
            follower = request.user,
            following_id = user_id
        )
        return Response({"message":"SUCCESS"}, status = status.HTTP_201_CREATED)


class UserDetailView(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class FollowerLisetView(generics.ListAPIView):   # 해당 사용자를 팔로우한 목록
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        queryset = User.objects.filter(following__following_id=user_id)
        return queryset


class FollowingLisetView(generics.ListAPIView):   # 해당 사용자가 팔로우한 목록
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        queryset = User.objects.filter(follower__follower_id=user_id)
        return queryset
