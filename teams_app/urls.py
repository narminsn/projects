from django.urls import path
from teams_app import views

urlpatterns = [
    path('create/', views.create_team, name='createteam'),
    path('myteam/', views.my_teams, name='myteams'),
    path('test/', views.test, name='test'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:id>/', views.detail_team, name='detail'),
    path('verify_team/<str:token>/<int:id>/', views.verify_view, name='verify_view'),
    path('dashboard/edit/<int:id>', views.dashboard_edit, name='dash-edit'),
    path('dashboard/my/project/', views.active_my, name='my-active'),
    path('dashboard/finished/', views.finished_project, name='finish'),
    path('dashboard/required/', views.required_project, name='required'),

]
