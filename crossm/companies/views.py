from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import DeleteView
from .forms import CompanyCreateForm
from .models import Companies, Countries
from funcy import omit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class CreateCompanyView(LoginRequiredMixin, View):
    template_name = 'companies/create_company.html'

    def get(self, request):
        if not request.user.allowed:
            return redirect('set-profile-info')
        context = {
            'form': CompanyCreateForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CompanyCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            r_data = omit(data, 'country_of_res')
            obj = Companies(**r_data)
            obj.owner = request.user
            obj.country_of_res = Countries.objects.filter(country=data['country_of_res']).first()
            obj.save()
            return redirect(reverse('companies:company-page', kwargs={'pk': obj.pk}))

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class CompanyPageView(LoginRequiredMixin, View):
    template_name = 'companies/company_page.html'

    def get(self, request, **kwargs):
        if not request.user.allowed:
            return redirect('set-profile-info')

        company = Companies.objects.filter(id=kwargs['pk']).select_related('owner').all().\
            prefetch_related('offers_set', 'owner__profile_set').all()

        if not company:
            raise Http404

        owner = 0
        if company[0].owner == request.user:
            owner = 1

        context = {
            'company': company[0],
            'owner': owner
        }
        return render(request, self.template_name, context)


class DeleteCompanyView(LoginRequiredMixin, DeleteView):
    template_name = 'companies/delete_company.html'

    def get_queryset(self):
        queryset = Companies.objects.filter(id=self.kwargs.get('pk'), owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('view-profile', kwargs={'pk': self.request.user.id})


class UpdateCompanyView(LoginRequiredMixin, View):
    template_name = 'companies/update_company.html'

    def get(self, request, **kwargs):
        obj = get_object_or_404(Companies, id=kwargs['pk'], owner=request.user)
        form = CompanyCreateForm(initial={
            'title': obj.title,
            'niche': obj.niche,
            'country_of_res': obj.country_of_res.country,
            'link': obj.link,
            'role': obj.role,
        })
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = CompanyCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            obj = get_object_or_404(Companies, id=kwargs['pk'], owner=request.user)
            obj.title = data['title']
            obj.niche = data['niche']
            obj.link = data['link']
            obj.role = data['role']

            if obj.country_of_res != data['country_of_res']:
                obj.country_of_res = Countries.objects.filter(country=data['country_of_res']).first()
            obj.save()
            return redirect(reverse('view-profile', kwargs={'pk': self.request.user.id}))

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
