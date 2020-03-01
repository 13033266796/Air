from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^demo', views.index),
    # url(r"^get_city_history_data/", views.get_city_history_data),
    url(r"^predict",views.predict),
]