
from registration.forms import RegistrationFormUniqueEmail, \
    RegistrationFormUsernameLowercase

from main.models import CustomUser


class CustomForm(RegistrationFormUniqueEmail, RegistrationFormUsernameLowercase):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'phone', 'email', 'username', 'password1', 'password2')
