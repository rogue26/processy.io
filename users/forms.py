from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
from organizations.models import Organization

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            user = super(CreateUpdateAjaxMixin, self).save(commit=commit)

            user.email = self.cleaned_data["email"]
            email_domain = user.email.split('@')[-1]

            if Organization.objects.filter(domain=email_domain).exists():
                organization = Organization.objects.get(domain=email_domain)
                user.organization = organization

            user.save()
        else:
            user = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
