from django.urls import path
from . import views
from page_views.views import dashboard, products

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('dashboard/', dashboard),
    path('products/', products),
]
