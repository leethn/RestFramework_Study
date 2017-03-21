from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.UserCreate.as_view()),
]