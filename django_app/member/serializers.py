from rest_framework import serializers
from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'name', 'password'

    def create(self, validated_data):
        print(self.initial_data)
        print(self.validated_data)
        print(self.data)
        instance = CustomUser.objects.create_user(**validated_data)
        return instance
