from rest_framework.pagination import PageNumberPagination


class ADSPagination(PageNumberPagination):
    """
    Вывод списка до 4 объявлений
    """

    page_size = 4


class ListPagination(PageNumberPagination):
    """
    Вывод списка до 4 объявлений
    """

    page_size = 10
