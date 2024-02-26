from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, help_text='Informe um endereço de e-mail já caadstrado em nosso sistema')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                username = User.objects.get(email=email).username
            except User.DoesNotExist:
                raise forms.ValidationError("Desculpe, esse e-mail não está cadastrado ou a senha está errada. Por favor, tente novamente.")
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Desculpe, esse e-mail não está cadastrado ou a senha está errada. Por favor, tente novamente.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
