import csv
from typing import NoReturn, List

from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

from ..serializers import DealSerializer


def get_file_data(file: InMemoryUploadedFile) -> List[dict]:
    """
    Сохраняет файл и получает из него данные, после чего удаляет файл
    """
    saved_file = default_storage.save(file.name, file)
    with open(saved_file) as csv_file:
        data = list(csv.DictReader(csv_file))
    default_storage.delete(saved_file)
    return data


def write_to_database(file: InMemoryUploadedFile) -> NoReturn:
    """
    Записывает полученные данные в базу, прогоняя их через сериализатор,
    очищает кэш, если запись состоялась
    """
    serializer = DealSerializer(data=get_file_data(file), many=True)
    serializer.is_valid(raise_exception=True)
    if not serializer.validated_data:
        raise ValidationError({'deals': 'file is empty'})
    serializer.save()
    cache.clear()
