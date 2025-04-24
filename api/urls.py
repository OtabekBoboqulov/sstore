from django.urls import path
from . import views
from page_views.views import dashboard

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('dashboard/', dashboard),
]
