from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Deal


class DealListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        feed_list = [Deal(**item) for item in validated_data]
        return Deal.objects.bulk_create(feed_list)


class DealSerializer(serializers.ModelSerializer):
    """
    Сериалйзер для обработки и внесение в БД информации из полученного файла
    """
    customer = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.users_dict: dict = {}
        super(DealSerializer, self).__init__(*args, **kwargs)

    def validate_customer(self, value: str) -> User:
        if not self.users_dict.get(value):
            user, _ = User.objects.get_or_create(username=value)
            self.users_dict[value] = user
        return self.users_dict[value]

    class Meta:
        model = Deal
        list_serializer_class = DealListSerializer
        fields = ('customer', 'item', 'total', 'quantity', 'date')
