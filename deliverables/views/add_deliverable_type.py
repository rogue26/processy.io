from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from ..forms import AddDeliverableTypeForm


class AddDeliverableType(BSModalCreateView):
    template_name = 'deliverables/add_deliverable_type.html'
    form_class = AddDeliverableTypeForm
    success_url = reverse_lazy('defaults')
