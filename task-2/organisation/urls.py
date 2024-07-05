from django.urls import path
from . import views


urlpatterns = [
    path("", views.ListCreateOrganisations.as_view()),
    path("<uuid:orgId>", views.GetOrganisation.as_view()),
    path("<uuid:orgId>/users", views.AddUserToOrganisation.as_view()),
]
