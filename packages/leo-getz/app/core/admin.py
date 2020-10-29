from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False,
    )

    class Meta:
        model = User
        fields = ("nickname",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['activation_code'].required = False

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserEditForm
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'nickname',
                'discord_id',
                'discord_username',
                'password1',
                'password2',
                'is_superuser',
                'is_staff',
                'is_active',
            )
        }),)

    fieldsets = (
        (None, {'fields': ('nickname',
                           'discord_id',
                           'discord_username',
                           'password')}),

        ('Important', {'fields': ('is_active',
                                  'created_at',
                                  'modified_at',
                                  'deleted_at')}),
    )

    list_display = [
        'id',
        'nickname',
        'is_active',
        'is_staff',
        'is_superuser',
    ]

    list_display_links = ['id', 'nickname']

    ordering = ['id']

    readonly_fields = ['created_at', 'deleted_at', 'modified_at']
