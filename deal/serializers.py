from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    """
    Сериалйзер для обработки и внесение в БД информации из полученного файла
    """
    customer = serializers.CharField()

    def validate_customer(self, value: str) -> User:
        user, _ = User.objects.get_or_create(username=value)
        return user

    class Meta:
        model = Deal
        fields = ('customer', 'item', 'total', 'quantity', 'date')
