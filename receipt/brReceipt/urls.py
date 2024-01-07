from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('search_receipts/', views.search_receipts, name="search_receipts"),
    path('add_receipt/', views.add_receipt, name='add_receipt'),
    path('rate_receipt/<int:receipt_id>/', views.rate_receipt, name='rate_receipt'),


    path('categories', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category_recipes, name='category_recipes'),
    path('categories/<int:category_id>/<int:receipt_id>', views.single_receipt, name='single_receipt'),
    path('rate_category/<int:category_id>/', views.rate_category, name='rate_category'),


    path('login/', auth_views.LoginView.as_view(template_name='brReceipt/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('ranking/', views.show_ranking,name='ranking'),
    path('random_receipt',views.random_receipt,name='random_receipt')


]