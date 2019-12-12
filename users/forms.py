"""Users forms"""

from django import forms

# Models

from django.contrib.auth.models import User
from users.models import Profile


# class ProfileForm(forms.Form):
#     """Profile form"""

#     website = forms.URLField(max_length=200, required=True)
#     biography = forms.CharField(max_length=500, required=False)
#     phone_number = forms.CharField(max_length=20, required=False)
#     picture = forms.ImageField(required=False)


class LoginForm(forms.ModelForm):
    """Login form"""

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        """User must exist"""

        data = super().clean()

        username = self.cleaned_data['username']
        username_exist = User.objects.filter(username=username).exists()
        if not username_exist:
            raise forms.ValidationError('El usuario ingresado no existe')
        return username

        return data


class SignupForm(forms.Form):
    """Sign up form"""

    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'required': True
        })
    )

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': True
        })
    )

    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'required': True

        })
    )

    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'required': True
        })
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'required': True
        })
    )

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'required': True
        })
    )

    def clean_username(self):
        """Username must be unique"""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('El nombre de usuario ya está en uso')
        return username

    def clean_email(self):
        """Username must be unique"""
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('El email ingresado ya está en uso')
        return email

    def clean(self):
        """Verify password confirmation match"""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden')

        return data

    def save(self):
        """Create user and profile"""

        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

        return user
