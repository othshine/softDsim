from rest_framework import serializers

from custom_user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  # serialize all the fields
        # fields = ["id", "username", "is_superuser", "is_staff"]
