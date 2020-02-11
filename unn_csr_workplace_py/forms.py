from django import forms


class CustomerSearchByPhone(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'data-mask': '0(000)000-00-00'}),
                                   label='Phone Number')
