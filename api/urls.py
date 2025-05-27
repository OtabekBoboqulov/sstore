from django.urls import path
from . import views
from page_views.views import *

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('dashboard/', dashboard),
    path('products/', products),
    path('products/edit/<int:pk>/', product_edit),
    path('products/update/<int:pk>/', product_update),
]
