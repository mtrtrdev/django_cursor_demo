from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView # TemplateView をインポート
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item
from .forms import ItemForm


class TopPageView(TemplateView):
    """
    トップページを表示するビュー。
    """
    template_name = 'stock/top_page.html' # ここを追加
    
class ItemListView(ListView):
    """
    在庫アイテムの一覧を表示するビュー。
    """
    model = Item
    template_name = 'stock/item_list.html'
    context_object_name = 'items'
    ordering = ['-created_at'] # 新しいものが上に表示されるように並び替え

class ItemDetailView(DetailView):
    """
    特定の在庫アイテムの詳細を表示するビュー。
    """
    model = Item
    template_name = 'stock/item_detail.html'
    context_object_name = 'item'

class ItemCreateView(CreateView):
    """
    新しい在庫アイテムを追加するビュー。
    """
    model = Item
    form_class = ItemForm
    template_name = 'stock/item_form.html'
    success_url = reverse_lazy('stock:item_list') # 成功時に一覧ページへリダイレクト

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新規アイテム追加'
        return context

class ItemUpdateView(UpdateView):
    """
    既存の在庫アイテムを編集するビュー。
    """
    model = Item
    form_class = ItemForm
    template_name = 'stock/item_form.html'
    success_url = reverse_lazy('stock:item_list') # 成功時に一覧ページへリダイレクト

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'アイテム編集'
        return context

class ItemDeleteView(DeleteView):
    """
    特定の在庫アイテムを削除するビュー。
    """
    model = Item
    template_name = 'stock/item_confirm_delete.html'
    context_object_name = 'item'
    success_url = reverse_lazy('stock:item_list') # 成功時に一覧ページへリダイレクト
