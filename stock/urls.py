from django.urls import path
from . import views

app_name = 'stock' # アプリケーションの名前空間を定義

urlpatterns = [
    path('list/', views.ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('new/', views.ItemCreateView.as_view(), name='item_new'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
]