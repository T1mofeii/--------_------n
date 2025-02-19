from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_application/', views.create_application, name='create_application'),
    path('lk/', views.lk, name='lk'),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
    path('our_application/', views.our_application, name='our_application'),
    path('logout/', views.logout_view, name='logout'),
    path('api/solved-count/', views.get_solved_count, name='get_solved_count'),
    path('delete-application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('delete-application/<int:application_id>/', views.delete_application, name='delete_application'),
]