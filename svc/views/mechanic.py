from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from svc.forms.mechanic import MechanicForm
from svc.models import Mechanic


class MechanicListView(ListView):
    model = Mechanic
    template_name = "mechanic/mechanics_list.html"
    context_object_name = "mechanics"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context['mechanics'])  # Print the mechanics to the console
    #     # return context


class MechanicCreateView(CreateView):
    model = Mechanic
    form_class = MechanicForm
    template_name = "mechanic/mechanic_form.html"
    success_url = reverse_lazy("mechanics")


class MechanicUpdateView(UpdateView):
    model = Mechanic
    form_class = MechanicForm
    template_name = "mechanic/mechanic_form.html"
    success_url = reverse_lazy("mechanics")


class MechanicDeleteView(DeleteView):
    model = Mechanic
    template_name = "mechanic/mechanic_confirm_delete.html"
    success_url = reverse_lazy("mechanics")
