from django.urls import reverse_lazy
# from django.views.generic import TemplateView

from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView

from forms import CustomUserCreationForm, CustomAuthenticationForm


# class Index(TemplateView):
#     template_name = "index.html"


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')
