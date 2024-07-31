from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'Input1'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'id': 'Input2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'Input3'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Input4'}),
            'state': forms.Select(attrs={'class': 'form-control', 'id': 'Input5'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'id': 'Input6'}),
        }
