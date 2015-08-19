from django.forms.models import ModelForm
from django.contrib.auth.models import User


class AccountSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
