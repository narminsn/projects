from django.urls import path
from teams_app import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:id>/', views.detail_team, name='detail'),
    path('verify_team/<str:token>/<int:id>/', views.verify_view, name='verify_view'),
    path('dashboard/edit/<int:id>', views.dashboard_edit, name='dash-edit'),
    path('dashboard/my/project/', views.active_my, name='my-active'),
    path('dashboard/finished/', views.finished_project, name='finish'),
    path('dashboard/required/', views.required_project, name='required'),
    path('dashboard/delete/<int:id>', views.delete_project, name='dash-delete'),

]
