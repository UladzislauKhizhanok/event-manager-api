from rest_framework.pagination import PageNumberPagination


class EventPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "size"
    max_page_size = 1000
