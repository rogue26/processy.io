from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from bootstrap_modal_forms.generic import BSModalCreateView

from ..forms import AddDeliverableTypeForm


class AddDeliverableType(BSModalCreateView):
    template_name = 'deliverables/add_deliverable_type.html'
    form_class = AddDeliverableTypeForm
    success_url = reverse_lazy('organization')

    def form_valid(self, form):
        if not self.request.is_ajax():
            form.instance.organization = self.request.user.organization
            form.save()
        else:
            pass
        return HttpResponseRedirect(reverse_lazy('organization'))
