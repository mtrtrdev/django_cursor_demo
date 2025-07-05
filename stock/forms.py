from django import forms
from .models import Item
from django.core.exceptions import ValidationError

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '商品名を入力してください'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        labels = {
            'name': '商品名',
            'quantity': '数量',
        }
        # エラーメッセージを日本語化
        error_messages = {
            'name': {
                'unique': "この商品名は既に登録されています。",
                'required': "商品名は必須です。", # ここを確認
                'max_length': "商品名は200文字以内で入力してください。"
            },
            'quantity': {
                'required': "数量は必須です。",
                'invalid': "数量は有効な数値を入力してください。"
            }
        }

    def clean_quantity(self):
        """
        数量が0以上であることを確認するカスタムバリデーション。
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError('数量は0以上でなければなりません。')
        return quantity

    def clean_name(self):
        """
        商品名の重複チェック（大文字・小文字を区別しない）。
        """
        name = self.cleaned_data.get('name')
        if name:
            # 自身を除いて重複をチェック (更新時の対応)
            if self.instance and Item.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError('この商品名は既に登録されています。')
            elif not self.instance and Item.objects.filter(name__iexact=name).exists():
                raise ValidationError('この商品名は既に登録されています。')
        return name