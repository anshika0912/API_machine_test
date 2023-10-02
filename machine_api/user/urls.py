from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('getclient', views.get_client),
    path('createclient', views.create_client),
    path('updateclient/<rid>', views.update_client),
    path('deleteclient/<rid>', views.delete_client),
    path('clients/<int:client_id>/projects/', views.create_project_for_client, name='create_project_for_client'),
] 