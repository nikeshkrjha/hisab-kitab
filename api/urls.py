from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.users_list),
    path('transactions/', views.transactions_list),
    path('categories/', views.exp_category_list),
    path('expenses/', views.expenses_list)
]