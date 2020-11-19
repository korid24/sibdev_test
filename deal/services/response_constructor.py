from decimal import Decimal
from typing import List, TypedDict, Union, NoReturn

from django.db.models import Sum, F
from django.contrib.auth.models import User

from ..models import Deal


class CustomerInfo(TypedDict):
    """
    Информация о клиенте для ответа на get запрос
    """
    username: str
    spent_money: Decimal
    gems: Union[set, list]


def get_top_customers_usernames() -> List[str]:
    """
    Возвращает логины 5ти клиентов с наибольшей суммой сделок за все время
    """
    queryset = (Deal.objects.annotate(username=F('customer__username'))
                .values('username')
                .annotate(spent_money=Sum('total'))
                .order_by('-spent_money')[:5])
    return queryset.values_list('username')


def get_intersections(customers_list: List[CustomerInfo]) -> set:
    """
    Возвращает множество камней, которые купили как минимум двое из списка
    "5 клиентов, потративших наибольшую сумму за весь период"
    """
    gems_list = []
    for customer in customers_list:
        gems_list += list(customer['gems'])
    not_unique_gems = [gem for gem in gems_list if gems_list.count(gem) > 1]
    return set(not_unique_gems)


def get_final_customers_list(customers_list: List[CustomerInfo],
                             not_unique_gems: set) -> List[CustomerInfo]:
    """
    Возвращает изменённый список пользователей, в котором в поле gems
    отображается список из названий камней, которые купили как минимум двое из
    списка "5 клиентов, потративших наибольшую сумму за весь период", и данный
    клиент является одним из этих покупателей.
    """
    for customer in customers_list:
        customer['gems'] = sorted(
            customer['gems'].intersection(not_unique_gems))
    return sorted(
        customers_list, key=lambda el: el['spent_money'], reverse=True)


def get_response() -> List[CustomerInfo]:
    """
    Формирует ответ на get запрос
    """
    customers = User.objects.filter(
        username__in=get_top_customers_usernames()).prefetch_related('deals')
    customers_list = []
    for user in customers:
        customer_info = CustomerInfo(
            username=user.username,
            spent_money=sum([deal.total for deal in user.deals.all()]),
            gems=set([deal.item for deal in user.deals.all()]))
        customers_list.append(customer_info)
    not_unique_gems = get_intersections(customers_list)
    result = get_final_customers_list(customers_list, not_unique_gems)
    return result
