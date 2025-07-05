"""
URL configuration for inventory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy # reverse_lazy をインポート
from django.views.generic.base import RedirectView # RedirectView をインポート
from stock.views import TopPageView # TopPageView は既にインポート済み

urlpatterns = [
    path('admin/', admin.site.urls),
    # /stock/ にアクセスしたらトップページにリダイレクト
    path('stock/', RedirectView.as_view(url=reverse_lazy('top_page'), permanent=False)), # ここを修正
    path('', TopPageView.as_view(), name='top_page'),
    # 在庫管理機能のURLは別のパスにする
    path('inventory/', include('stock.urls')), # 'stock/' を 'inventory/' に変更
]
