from django.urls import path
from . import views


urlpatterns = [path("", views.GetUserDetail.as_view())]
