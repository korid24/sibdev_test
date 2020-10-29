from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView
from .services.filehandler import write_to_database
from .services.response_constructor import get_response


class DealView(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        """
        Формирование ответа, кэширование ответа
        """
        return Response({'response': get_response()}, status=200)

    def post(self, request):
        """
        Проверка наличия и расширения файла deals,
        передача его в функцию для записи в бд.
        """
        deals = request.data.get('deals')
        if deals and deals.name.endswith('.csv'):
            write_to_database(deals)
        else:
            return Response({'deals': 'file deals.csv expected'}, status=400)

        return Response(status=200)
