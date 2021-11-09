from django import forms
from django.forms import ModelForm
from youTube_app.models import DownloadUser


class YouTubeLinkInput(forms.Form):
    yt_link = forms.CharField(
        max_length=200,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Paste YouTube Link Here',
            'id': 'linkHere'
        })
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Username'
        })
    )

    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Email'
        })
    )

    path = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Full path to download dir'
        })
    )

    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*Password'
        })
    )

    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*Confirm Password'
        })
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Username'
        })
    )

    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*Password'
        })
    )


class YouTubeStream(forms.Form):
    yt_stream = forms.CharField(
        max_length=4,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*itag choice'
        }))


class UpdateUserForm(ModelForm):
    username = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Username'
        })
    )

    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Email'
        })
    )

    download_path = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Full path to download dir'
        })
    )

    user_pic = forms.FileField(
        label='Profile Picture',
        required=False)

    class Meta:
        model = DownloadUser
        fields = [
            'username',
            'email',
            'download_path',
            'user_pic'
        ]


class ResetRequest(forms.Form):
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Email'
        })
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*New Password'
        })
    )

    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*Re-Type Password'
        })
    )
