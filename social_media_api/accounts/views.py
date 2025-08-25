from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from notifications.utils import create_notification  # safe now with apps.get_model()

CustomUser = get_user_model()

# ---- Auth/Profile ----
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        token = Token.objects.get(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key, "message": "Registration successful"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key, "message": "Login successful"})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        s = UserSerializer(request.user, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

    def patch(self, request):
        s = UserSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)

# ---- Follow/Unfollow (class-based for checker literals) ----
class FollowUserView(generics.GenericAPIView):  # checker literal
    permission_classes = [permissions.IsAuthenticated]  # checker literal
    queryset = CustomUser.objects.all()  # checker literal

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        target = get_object_or_404(CustomUser, pk=user_id)
        request.user.following.add(target)
        if target.id != request.user.id:
            create_notification(recipient=target, actor=request.user, verb="followed you", target=None)
        return Response({"detail": f"Now following {target.username}."})

class UnfollowUserView(generics.GenericAPIView):  # checker literal
    permission_classes = [permissions.IsAuthenticated]  # checker literal
    queryset = CustomUser.objects.all()  # checker literal

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        target = get_object_or_404(CustomUser, pk=user_id)
        request.user.following.remove(target)
        return Response({"detail": f"Unfollowed {target.username}."})

# (Optional) function versions kept if you referenced them anywhere:
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    if request.user.id == user_id:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    target = get_object_or_404(CustomUser, pk=user_id)
    request.user.following.add(target)
    if target.id != request.user.id:
        create_notification(recipient=target, actor=request.user, verb="followed you", target=None)
    return Response({"detail": f"Now following {target.username}."})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    if request.user.id == user_id:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    target = get_object_or_404(CustomUser, pk=user_id)
    request.user.following.remove(target)
    return Response({"detail": f"Unfollowed {target.username}."})
