from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta():
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password'
            ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name' # noqa
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name' # noqa
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address' # noqa
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number' # noqa
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name' # noqa
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name' # noqa
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone number' # noqa
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):

    profile_picture = forms.ImageField(
        required=False,
        error_messages={
            'invalid': ("Image files only")
        },
        widget=forms.FileInput
    )
    class Meta:
        model = UserProfile
        fields = [
            'address_line_1',
            'address_line_2',
            'profile_picture',
            'city',
            'state',
            'country',
        ]
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Address line 1' # noqa
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Address line 2' # noqa
        self.fields['city'].widget.attrs['placeholder'] = 'City' # noqa
        self.fields['state'].widget.attrs['placeholder'] = 'State' # noqa
        self.fields['country'].widget.attrs['placeholder'] = 'Country' # noqa
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'