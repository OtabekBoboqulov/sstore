from django.urls import path
from . import views
from page_views.views import *

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('dashboard/', dashboard),
    path('categories/', categories),
    path('categories/create/', category_create),
    path('products/', products),
    path('products/report/', products_report),
    path('products/edit/<int:pk>/', product_edit),
    path('products/update/<int:pk>/', product_update),
    path('products/delete/<int:pk>/', product_delete),
    path('products/delete/several/', product_delete_several),
    path('products/create/', product_create),
]
