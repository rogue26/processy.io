from django.urls import reverse_lazy
from django.contrib.auth import login

from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('manage_projects')

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        if not self.request.is_ajax():
            login(self.request, self.object)
        else:
            pass
        return valid


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('manage_projects')
