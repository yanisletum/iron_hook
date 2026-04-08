from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Поля, которые должен заполнить покупатель на сайте
        fields = ['first_name', 'last_name', 'email', 'city', 'address']