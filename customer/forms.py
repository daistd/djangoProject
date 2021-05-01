from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

    ceo = forms.CharField(label='Ваше Имя', max_length=100)
    phone = forms.CharField(label='Номер телефона', max_length=12)
    name = forms.CharField(label='Название Юр. лица', max_length=100)


