from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('create_menu/',views.create_menu,name='create_menu'),
        path('register_form/',views.register_form,name='register_form'),
        path('register/',views.register,name='register'),
        path('register/register_success/',views.register_success,name='register_success'),
        path('register_override/',views.register_override,name='register_override'),
        path('register_override/register_success/',views.register_success,name='register_override_success'),
        path('query_form/',views.query_form,name='query_form'),
        path('query/',views.query,name='query'),
]
