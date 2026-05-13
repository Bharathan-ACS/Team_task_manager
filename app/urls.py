from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('signup/', views.signup_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('project/create/', views.create_project),
    path('task/create/', views.create_task),
    path('task/update/<int:id>/', views.update_task),
]