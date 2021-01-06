from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from ..forms import AddWorkstreamTypeForm


class AddWorkstreamType(BSModalCreateView):
    template_name = 'workstreams/add_workstream_type.html'
    form_class = AddWorkstreamTypeForm
    success_url = reverse_lazy('organization')
