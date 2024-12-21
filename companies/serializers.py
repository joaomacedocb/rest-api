from rest_framework import serializers

from accounts.models import User

class User_Serializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email'
        )