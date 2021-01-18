from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class RACI(LoginRequiredMixin, TemplateView):
    template_name = "RACI/RACI.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
