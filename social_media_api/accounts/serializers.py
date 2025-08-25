# accounts/serializers.py
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token  # <- required literal import

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers_count",
            "following_count",
        ]
        read_only_fields = ["id", "followers_count", "following_count"]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # will expose token in the serializer output for convenience
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "token"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # <- required literal call using get_user_model
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email") or "",
            password=validated_data["password"],
        )
        # <- required literal call to create a token here in the serializer
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # include the token value in the response
        token = Token.objects.get(user=instance)
        data["token"] = token.key
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        attrs["user"] = user
        return attrs
