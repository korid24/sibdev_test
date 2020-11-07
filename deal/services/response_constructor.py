from typing import List, NoReturn

from django.db.models import Sum, QuerySet, F

from ..models import Deal


INTERSECTIONS: set = set()


def get_top_customers_queryset() -> QuerySet:
    """
    Возвращает queryset из логинов 5ти клиентов с наибольшей суммой
    сделок за все время и суммой их сделок
    """
    return (Deal.objects.annotate(username=F('customer__username'))
            .values('username')
            .annotate(spent_money=Sum('total'))
            .order_by('-spent_money')[:5])


def get_top_customers_usernames() -> List[str]:
    """
    Возвращает логины 5ти клиентов с наибольшей суммой сделок за все время
    """
    queryset = get_top_customers_queryset()
    return queryset.values_list('username')


def get_gems_intersections() -> NoReturn:
    """
    Определяет множество позиций приобретенных хотя бы 2мя из 5ти
    топовых клиентов
    """
    gems_of_top = (Deal.objects.values('customer__username', 'item')
                   .filter(customer__username__in=get_top_customers_usernames())
                   .distinct()).order_by('customer__username')
    gems = [gem['item'] for gem in gems_of_top]
    not_unique_gems = [gem for gem in gems if gems.count(gem) > 1]
    global INTERSECTIONS
    INTERSECTIONS = set(not_unique_gems)


def get_user_intersections_gems(username: str) -> List[str]:
    """
    Возвращает список позиций приобретённых клиентом и входящих во
    множество позиций приобретенных хотя бы 2мя из 5ти
    топовых клиентов
    """
    queryset = (Deal.objects.filter(customer__username=username)
                .values_list('item').distinct())
    gems_set = set([gem[0] for gem in queryset])
    return list(gems_set.intersection(INTERSECTIONS))


def get_response() -> List[dict]:
    """Возвращает ответ на get запрос"""
    get_gems_intersections()
    top_customers = list(get_top_customers_queryset())
    for customer in top_customers:
        name = customer['username']
        customer.update({'gems': get_user_intersections_gems(name)})
    return top_customers
