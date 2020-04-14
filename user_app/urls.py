from django.urls import path
from user_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('verify/<str:token>/<int:id>/', views.verify_view, name='verify_view'),
    path('change_password/', views.change_password, name='change_password'),
    path('settings/<int:id>/', views.settings_user, name='settings'),

]
