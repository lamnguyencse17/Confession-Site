from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=20)


class ConfessionForm(forms.Form):
    confess_content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':10, 'cols':100}))
