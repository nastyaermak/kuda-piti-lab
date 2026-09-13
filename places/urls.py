from django.urls import path

from . import views

app_name = 'places'

urlpatterns = [
    path('', views.home, name='home'),
    path('places/', views.place_list, name='place_list'),
    path('places/add/', views.place_add, name='place_add'),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
]
