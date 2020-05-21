from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('create_menu/', views.create_menu, name='create_menu'),
        path('register_form/', views.get_openid, name='get_openid'),
        path('register_form_after_oath/', views.register_form, name='register_form'),
        path('register/', views.register, name='register'),
        path('query_form/', views.query_form, name='query_form'),
        path('login_form/', views.login_form, name='login_form'),
        path('login_with_oath/', views.login_with_oath, name="login_with_oath"),
        path('back_to_admin_query/', views.back_to_admin_query, name='back_to_admin_query'),
        path('admin_query_override/', views.admin_query_override, name='admin_query_override'),
        path('check_patient_id/', views.check_patient_ID_exist, name='check_patient_id'),
]
