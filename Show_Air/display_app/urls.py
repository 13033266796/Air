from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r"^index/", views.index),
    url(r"^$", views.index),
    url(r"^get_city_history_data/", views.get_city_history_data),
    url(r"^api/data/", views.get_data)
]
