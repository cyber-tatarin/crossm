import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import DeleteView
from .forms import CompanyCreateForm
from .models import Companies, Countries
from funcy import omit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponseRedirect
from users.views import get_profile_ph, is_allowed


class CreateCompanyView(LoginRequiredMixin, View):
    template_name = 'companies/create_company.html'

    def get(self, request):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        context = {
            'form': CompanyCreateForm(),
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)

    def post(self, request):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        form = CompanyCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            r_data = omit(data, 'country_of_res')
            obj = Companies(**r_data)
            obj.owner = request.user
            obj.country_of_res = Countries.objects.filter(country=data['country_of_res']).first()
            obj.save()

            nexty = request.POST.get('next')
            if nexty:
                try:
                    return HttpResponseRedirect(nexty)
                except:
                    raise Http404
            else:
                return redirect(reverse('companies:company-page', kwargs={'pk': obj.pk}))

        context = {
            'form': form,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class CompanyPageView(LoginRequiredMixin, View):
    template_name = 'companies/company_page.html'

    def get(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        company = Companies.objects.filter(id=kwargs['pk']).select_related('owner').all(). \
            prefetch_related('offers_set', 'owner__profile_set').all()

        if not company:
            raise Http404

        owner = 0
        if company[0].owner == request.user:
            owner = 1

        context = {
            'company': company[0],
            'owner': owner,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class DeleteCompanyView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        obj = get_object_or_404(Companies, id=request.POST.get('id'), owner=request.user)
        obj.delete()
        return JsonResponse({'success': True})


class UpdateCompanyView(LoginRequiredMixin, View):
    template_name = 'companies/update_company.html'

    def get(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        obj = get_object_or_404(Companies, id=kwargs['pk'], owner=request.user)
        form = CompanyCreateForm(initial={
            'title': obj.title,
            'niche': obj.niche,
            'country_of_res': obj.country_of_res.country,
            'link': obj.link,
            'role': obj.role,
        })
        context = {
            'form': form,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

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
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class CompanyImageDeleteView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        company = get_object_or_404(Companies, id=request.POST.get('id'), owner=request.user)
        if company.owner == request.user:
            company.photo = None
            company.save()
            return JsonResponse({'success': True})
        else:
            return Http404


class CompanyPhotoUpload(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        obj = get_object_or_404(Companies, owner=request.user, id=request.POST.get('id'))
        obj.photo = request.FILES.get('image')
        obj.save()
        return JsonResponse({'success': True, 'image': obj.photo.url})


@receiver(pre_save, sender=Companies)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.photo.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


@receiver(post_delete, sender=Companies)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.photo.delete(save=False)
    except:
        pass


class CheckCompanyPhoto(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        obj = get_object_or_404(Companies, owner=request.user, id=request.GET.get('id'))
        if obj.photo:
            return JsonResponse({'success': True, 'image': obj.photo.url})
        else:
            return JsonResponse({'success': True, 'image': False})
