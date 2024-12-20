from django.contrib.auth.views import PasswordChangeView

from .forms import PasswordChangeForm

# Create your views here.


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
