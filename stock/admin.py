from django.contrib import admin
from .models import Item # Itemモデルをインポート

# Itemモデルを管理者サイトに登録
admin.site.register(Item)