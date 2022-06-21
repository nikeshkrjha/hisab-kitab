from django.urls import path
from api import views
from rest_framework.authtoken import views as av

urlpatterns = [
    path('users/', views.users_list),
    path('transactions/', views.transactions_list),
    path('categories/', views.exp_category_list),
    path('expenses/', views.expenses_list),
    path('expenses/<int:pk>', views.expenses_detail),
    path('groups/', views.groups_list),
    path('api-token-auth/', av.obtain_auth_token),
    path('register/',views.register_user)
]