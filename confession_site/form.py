from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=20)


class ConfessionForm(forms.Form):
    confess_content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':10, 'cols':100}))
    picture = forms.ImageField(required = False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    contact_text = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 10, 'cols': 'auto', 'placeholder': 'Contact Details'}))
