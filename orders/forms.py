from django import forms
from .models import Order, ShippingAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'state', 'postal_code', 
            'country', 'payment_method'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(choices=[('India', 'India'), ('United States', 'United States'), ('United Kingdom', 'United Kingdom')], attrs={'class': 'form-control'}),
            'payment_method': forms.Select(choices=Order.PAYMENT_CHOICES, attrs={'class': 'form-control'}),
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = (
            'first_name', 'last_name', 'phone', 
            'address', 'city', 'state', 'postal_code', 
            'country', 'is_default'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(choices=[('India', 'India'), ('United States', 'United States'), ('United Kingdom', 'United Kingdom')], attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
