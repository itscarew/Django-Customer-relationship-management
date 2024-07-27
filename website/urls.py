from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_user, name="logout"),
    path("record/<int:pk>", views.record, name="record"),
    path("delete/<int:pk>", views.delete_record, name="delete"),
    path("add_record/", views.add_record, name="add_record"),
    path('update/<int:pk>', views.update_record, name='update_record'),
]
