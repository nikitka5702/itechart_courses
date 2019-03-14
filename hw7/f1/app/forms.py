from django import forms

from app.models import Shop


class ShopChooserForm(forms.Form):
    shop = forms.ModelChoiceField(Shop.objects.all())
