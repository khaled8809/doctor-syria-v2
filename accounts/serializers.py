from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """مسلسل بيانات المستخدم"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
            "date_joined",
            "barcode",
        ]
        read_only_fields = ["id", "date_joined", "barcode"]
