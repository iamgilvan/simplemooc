from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template

from .models import PasswordReset

User = get_user_model()

#Será um form normal. Não será um ModelForm, pois inicialmente não estará assoociado a nenhum outro model
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    #Validando email (Pode conter email existente na base)
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário encontrado com este email.')

    def save(self):
        #se existe usuário
        user = User.objects.get(email=self.cleaned_data['email'])
        #gerar a chave
        key   = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_email.html'
        subject = 'Criar nova senha no Simple MOOC'
        context = {
            'reset': reset,
        }
        send_mail_template(subject, template_name, context, [user.email])
    
# Esta classe foi cirada para adicionar o campo email
# Ela extende a classe UserCreationForm e adiciona o email
class RegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])# set_password para criptografar a senha
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name']