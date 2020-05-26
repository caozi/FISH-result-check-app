from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('create_menu/', views.create_menu, name='create_menu'),
        path('register_form/', views.get_openid, name='get_openid'),
        path('register_form_after_oath/', views.register_form, name='register_form'),
        path('register/', views.register, name='register'),
        path('after_register/', views.after_register, name='after_register'),
        path('FISH/', views.get_openid_FISH, name='get_openid_FISH'),
        path('FISH_register_form_afer_oath/', views.register_form_FISH, name='register_form_FISH'),
        path('register_FISH/', views.register_FISH, name='register_FISH'),
        path('query_form/', views.query_form, name='query_form'),
        path('login_form/', views.login_form, name='login_form'),
        path('login_with_oath/', views.login_with_oath, name="login_with_oath"),
        path('admin_query/', views.admin_query, name='admin_query'),
        path('back_to_admin_query/', views.back_to_admin_query, name='back_to_admin_query'),
        path('back_to_admin_query_after_phone/', views.back_to_admin_query_after_phone, name='back_to_admin_query_after_phone'),
        path('admin_query_override/', views.admin_query_override, name='admin_query_override'),
        path('check_patient_id/', views.check_patient_ID_exist, name='check_patient_id'),
]
