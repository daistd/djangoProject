from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

    phone = forms.CharField(label='Номер телефона', max_length=12)
    name = forms.CharField(label='Название компании или Ваше имя', max_length=100)
    ceo = forms.CharField(label='Ваше имя как в Каспи переводах', max_length=100)


