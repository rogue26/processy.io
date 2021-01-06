from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from ..forms import AddDivisionForm


class AddDivision(BSModalCreateView):
    template_name = 'organizations/add_division.html'
    form_class = AddDivisionForm

    def form_valid(self, form):
        if not self.request.is_ajax():
            form.instance.organization = self.request.user.organization
            form.save()
        else:
            pass
        return HttpResponseRedirect(reverse_lazy('organization'))
