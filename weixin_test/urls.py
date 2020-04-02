from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('create_menu/',views.create_menu,name='create_menu'),
        path('register_form/',views.get_openid,name='get_openid'),
        path('register_form_after_oath/',views.register_form,name='register_form'),
        path('register/',views.register,name='register'),
        path('register/register_success/',views.register_success,name='register_success'),
        path('register_override/',views.register_override,name='register_override'),
        path('register_override/register_success/',views.register_success,name='register_override_success'),
        path('query_form/',views.query_form,name='query_form'),
        path('query/',views.query,name='query'),
        path('login_form/',views.login_form,name='login_form'),
        path('login/',views.login,name='login'),
        path('admin_query/',views.admin_query,name='admin_query'),
        path('admin_query_override/',views.admin_query_override,name='admin_query_override'),
]
