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
    path('categories/products/', categories_with_products),
    path('categories/delete/<int:pk>/', category_delete),
    path('products/', products),
    path('products/<int:pk>/', product_detail),
    path('products/report/', products_report),
    path('products/edit/<int:pk>/', product_edit),
    path('products/update/<int:pk>/', product_update),
    path('products/delete/<int:pk>/', product_delete),
    path('products/delete/several/', product_delete_several),
    path('products/create/', product_create),
    path('sell/', save_product_updates),
    path('buy/', save_bought_products),
    path('debtors/', debtors),
    path('debtors/<int:pk>/', get_debtors_debts),
]
