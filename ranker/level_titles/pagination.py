from rest_framework.pagination import (
    LimitOffsetPagination,
)
from drf_pagination_meta_wrap.mixins import WrapPaginationMetadataMixin


class LevelTitlePagination(WrapPaginationMetadataMixin, LimitOffsetPagination):
    pass
