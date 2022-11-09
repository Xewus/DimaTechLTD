"""Эндпоинты для счетов.
"""
from sanic import Blueprint

from src.core.views import ApiGetMixin, ApiPosMixin
from src.db.models import Bill

blue = Blueprint('bills', url_prefix='/bills')


class BillView(ApiGetMixin, ApiPosMixin):
    model = Bill
    one = True
    many = True


blue.add_route(
    handler=BillView.as_view(),
    uri='/',
    methods=['GET', 'POST']
)
