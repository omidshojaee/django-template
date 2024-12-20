from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

# Create your forms here.


class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'dir': 'ltr'})
        self.fields['password'].widget.attrs.update({'dir': 'ltr'})


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'dir': 'ltr'})
        self.fields['new_password1'].widget.attrs.update({'dir': 'ltr'})
        self.fields['new_password2'].widget.attrs.update({'dir': 'ltr'})
