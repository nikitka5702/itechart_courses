from django import forms

from app.models import Shop, Department


class ShopChooserForm(forms.Form):
    shop = forms.ModelChoiceField(Shop.objects.all())


class DepartmentPickerForm(forms.Form):
    first_department = forms.ModelChoiceField(Department.objects.all())
    second_department = forms.ModelChoiceField(Department.objects.all())

    dep_staff = forms.BooleanField(initial=False, required=False)
    sold_items_cost = forms.BooleanField(initial=False, required=False)
    selling_items_cost = forms.BooleanField(initial=False, required=False)
    total_items_cost = forms.BooleanField(initial=False, required=False)
    sold_items_count = forms.BooleanField(initial=False, required=False)
    selling_items_count = forms.BooleanField(initial=False, required=False)
    total_count = forms.BooleanField(initial=False, required=False)
