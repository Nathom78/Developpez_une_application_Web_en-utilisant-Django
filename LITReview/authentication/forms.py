# authentication/forms.py
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django import forms

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        help_text=password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'role')
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2
    
    def _post_clean(self):
        """
        Use Validators for password.
        from UserCreationForm auth\forms.py
        """
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        
        if commit:
            user.save()
            if user.role == user.ADMINISTRATOR:
                group = Group.objects.get(name='administrators')
                user.groups.add(group)
            elif user.role == user.SUBSCRIBER:
                group = Group.objects.get(name='subscribers')
                user.groups.add(group)
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = MyUser
        fields = ('username', 'role', 'email', 'password', 'is_active', 'is_admin')


# class SignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ('username', 'role', 'email', 'password1', 'password2')
