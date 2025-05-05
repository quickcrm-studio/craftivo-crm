from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .utils import FormWidgets, validate_password_strength

User = get_user_model()

class UserSignupForm(UserCreationForm):
    """
    Form for creating a new user account for staff members.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[
            ('Staff', 'Staff'),
            ('Manager', 'Manager'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def save(self, commit=True):
        """Save the user and set their role."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Add user to the appropriate group based on role
            role = self.cleaned_data['role']
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        
        return user

class UserLoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=FormWidgets.get_text_input(placeholder="Username", required=True)
    )
    
    password = forms.CharField(
        required=True,
        widget=FormWidgets.get_password_input(placeholder="Password", required=True)
    )
    
    remember_me = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=FormWidgets.get_checkbox()
    )


class UserEditForm(forms.ModelForm):
    """
    Form for editing user information by administrators.
    """
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FormWidgets.get_checkbox_select_multiple(),
        help_text="Select groups/roles for this user"
    )
    
    is_active = forms.BooleanField(
        required=False,
        widget=FormWidgets.get_checkbox(),
        help_text="Designates whether this user should be treated as active."
    )
    
    is_staff = forms.BooleanField(
        required=False,
        widget=FormWidgets.get_checkbox(),
        help_text="Designates whether the user can log into the admin site."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'groups')
        widgets = {
            'username': FormWidgets.get_text_input(placeholder="Username"),
            'email': FormWidgets.get_email_input(placeholder="Email address"),
            'first_name': FormWidgets.get_text_input(placeholder="First name"),
            'last_name': FormWidgets.get_text_input(placeholder="Last name"),
        }


class UserCreateForm(UserCreationForm):
    """
    Form for creating new users by administrators.
    """
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FormWidgets.get_checkbox_select_multiple(),
        help_text="Select groups/roles for this user"
    )
    
    is_active = forms.BooleanField(
        required=False, 
        initial=True,
        widget=FormWidgets.get_checkbox(),
        help_text="Designates whether this user should be treated as active."
    )
    
    is_staff = forms.BooleanField(
        required=False,
        widget=FormWidgets.get_checkbox(),
        help_text="Designates whether the user can log into the admin site."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                 'is_active', 'is_staff', 'groups')
        widgets = {
            'username': FormWidgets.get_text_input(placeholder="Username"),
            'email': FormWidgets.get_email_input(placeholder="Email address"),
            'first_name': FormWidgets.get_text_input(placeholder="First name"),
            'last_name': FormWidgets.get_text_input(placeholder="Last name"),
        }
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        return validate_password_strength(password)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to password fields
        self.fields['password1'].widget = FormWidgets.get_password_input(placeholder="Password")
        self.fields['password2'].widget = FormWidgets.get_password_input(placeholder="Confirm password")

class UserProfileForm(forms.ModelForm):
    """
    Form for users to edit their own profile.
    """
    current_password = forms.CharField(
        required=False,
        widget=FormWidgets.get_password_input(placeholder="Current password"),
        help_text="Enter your current password to confirm changes or to set a new password."
    )
    
    new_password1 = forms.CharField(
        required=False,
        widget=FormWidgets.get_password_input(placeholder="New password"),
        help_text="Leave blank if you don't want to change your password."
    )
    
    new_password2 = forms.CharField(
        required=False,
        widget=FormWidgets.get_password_input(placeholder="Confirm new password"),
        help_text="Enter the same password as above, for verification."
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': FormWidgets.get_text_input(placeholder="First name"),
            'last_name': FormWidgets.get_text_input(placeholder="Last name"),
            'email': FormWidgets.get_email_input(placeholder="Email address"),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        # Only validate the current password if they're trying to set a new password
        current_password = self.cleaned_data.get('current_password')
        new_password1 = self.cleaned_data.get('new_password1')
        
        if new_password1 and not current_password:
            raise ValidationError("You must enter your current password to set a new password.")
        
        if current_password and not self.user.check_password(current_password):
            raise ValidationError("Your current password is incorrect.")
            
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        # If they've entered a new password, make sure both fields match
        if new_password1:
            if not new_password2:
                self.add_error('new_password2', "You must confirm your new password.")
            elif new_password1 != new_password2:
                self.add_error('new_password2', "The two password fields didn't match.")
            else:
                # Validate password strength
                try:
                    validate_password_strength(new_password1)
                except ValidationError as e:
                    self.add_error('new_password1', e)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # If a new password was provided, set it
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
        
        return user 