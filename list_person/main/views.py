from django.shortcuts import render
from users.models import Profile
from django.views.generic import ListView
from .forms import ProfileSearchForm


class MainList(ListView):
    model = Profile
    template_name = 'main/list.html'
    context_object_name = 'profile'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(name__icontains=query)
        order_by = self.request.GET.get('order_by')
        if order_by:
            queryset = queryset.order_by(order_by)
        filial = self.request.GET.get('filial')
        if filial:
            queryset = queryset.filter(filial=filial) if filial else queryset.filter(filial__isnull=True)
        account_type = self.request.GET.get('account_type')
        if account_type:
            queryset = queryset.filter(account_type=account_type) if account_type else queryset.filter(account_type__isnull=True)
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department=department) if department else queryset.filter(department__isnull=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(MainList, self).get_context_data(**kwargs)
        ctx['form'] = ProfileSearchForm(self.request.GET or None)
        ctx['title'] = 'Список сотрудников'
        return ctx


