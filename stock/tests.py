from django.test import TestCase
from django.urls import reverse
from .models import Item
from .forms import ItemForm

class ItemModelTest(TestCase):
    """
    Itemモデルのテストケース。
    """
    def test_item_creation(self):
        """
        アイテムが正しく作成されるかテスト。
        """
        item = Item.objects.create(name='テスト商品', quantity=10)
        self.assertEqual(item.name, 'テスト商品')
        self.assertEqual(item.quantity, 10)
        self.assertIsNotNone(item.created_at)
        self.assertIsNotNone(item.updated_at)

    def test_item_str_method(self):
        """
        __str__メソッドが正しく商品名を返すかテスト。
        """
        item = Item.objects.create(name='テスト商品2', quantity=5)
        self.assertEqual(str(item), 'テスト商品2')

class ItemFormTest(TestCase):
    """
    ItemFormのテストケース。
    """
    def test_form_valid_data(self):
        """
        フォームが有効なデータでバリデーションされるかテスト。
        """
        form = ItemForm(data={'name': 'フォーム商品', 'quantity': 100})
        self.assertTrue(form.is_valid())

    def test_form_no_name(self):
        """
        商品名が空の場合にバリデーションエラーが発生するかテスト。
        """
        form = ItemForm(data={'name': '', 'quantity': 50})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_negative_quantity(self):
        """
        数量が負の場合にバリデーションエラーが発生するかテスト。
        """
        form = ItemForm(data={'name': 'エラー商品', 'quantity': -5})
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_form_duplicate_name(self):
        """
        重複する商品名でバリデーションエラーが発生するかテスト。
        """
        Item.objects.create(name='既存商品', quantity=10)
        form = ItemForm(data={'name': '既存商品', 'quantity': 20})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ItemViewsTest(TestCase):
    """
    在庫アイテム関連ビューのテストケース。
    """
    def setUp(self):
        """
        各テストメソッド実行前にテストデータを準備。
        """
        self.item1 = Item.objects.create(name='リンゴ', quantity=10)
        self.item2 = Item.objects.create(name='オレンジ', quantity=20)

    def test_item_list_view(self):
        """
        アイテム一覧ページが正しく表示され、アイテムが含まれているかテスト。
        """
        response = self.client.get(reverse('stock:item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_list.html')
        self.assertContains(response, 'リンゴ')
        self.assertContains(response, 'オレンジ')
        self.assertContains(response, '新しいアイテムを追加') # 新規追加ボタンの確認

    def test_item_detail_view(self):
        """
        アイテム詳細ページが正しく表示され、詳細情報が含まれているかテスト。
        """
        response = self.client.get(reverse('stock:item_detail', args=[self.item1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_detail.html')
        self.assertContains(response, self.item1.name)
        self.assertContains(response, str(self.item1.quantity))
        self.assertContains(response, '編集') # 編集ボタンの確認

    def test_item_create_view_get(self):
        """
        新規アイテム作成ページのGETリクエストが正しく表示されるかテスト。
        """
        response = self.client.get(reverse('stock:item_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_form.html')
        self.assertContains(response, '新規アイテム追加')

    def test_item_create_view_post_valid_data(self):
        """
        有効なデータで新規アイテムが作成され、リダイレクトされるかテスト。
        """
        response = self.client.post(reverse('stock:item_new'), {
            'name': '新規作成アイテム',
            'quantity': 50
        }, follow=True) # follow=True でリダイレクト先を追跡
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_list.html') # 一覧ページにリダイレクトされたことを確認
        self.assertContains(response, '新規作成アイテム') # 作成したアイテムが一覧に含まれることを確認
        self.assertEqual(Item.objects.count(), 3) # アイテム数が1増えたことを確認

    def test_item_create_view_post_invalid_data(self):
        """
        無効なデータで新規アイテムが作成されないかテスト。
        """
        response = self.client.post(reverse('stock:item_new'), {
            'name': '', # 無効なデータ (空の名前)
            'quantity': 50
        })
        self.assertEqual(response.status_code, 200) # エラー表示のため200
        self.assertTemplateUsed(response, 'stock/item_form.html')
        self.assertContains(response, '商品名は必須です。') # エラーメッセージを修正
        self.assertEqual(Item.objects.count(), 2) # アイテム数が増加しないことを確認

    def test_item_update_view_get(self):
        """
        アイテム編集ページのGETリクエストが正しく表示されるかテスト。
        """
        response = self.client.get(reverse('stock:item_edit', args=[self.item1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_form.html')
        self.assertContains(response, 'アイテム編集')
        self.assertContains(response, self.item1.name)

    def test_item_update_view_post_valid_data(self):
        """
        有効なデータでアイテムが更新され、リダイレクトされるかテスト。
        """
        response = self.client.post(reverse('stock:item_edit', args=[self.item1.pk]), {
            'name': '更新済みリンゴ',
            'quantity': 15
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_list.html')
        self.item1.refresh_from_db() # データベースから最新の情報を取得
        self.assertEqual(self.item1.name, '更新済みリンゴ')
        self.assertEqual(self.item1.quantity, 15)

    def test_item_delete_view_get(self):
        """
        アイテム削除確認ページのGETリクエストが正しく表示されるかテスト。
        """
        response = self.client.get(reverse('stock:item_delete', args=[self.item1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_confirm_delete.html')
        self.assertContains(response, f'「{self.item1.name}」を削除しますか？')

    def test_item_delete_view_post(self):
        """
        アイテムが正しく削除され、リダイレクトされるかテスト。
        """
        response = self.client.post(reverse('stock:item_delete', args=[self.item1.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/item_list.html')
        self.assertNotContains(response, self.item1.name) # 削除されたアイテムが一覧にないことを確認
        self.assertEqual(Item.objects.count(), 1) # アイテム数が1減ったことを確認