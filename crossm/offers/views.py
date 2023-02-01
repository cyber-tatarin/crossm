from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateOfferForm
from companies.models import Companies
from .models import OffersImages, Offers
from django.views.generic import DeleteView
from users.models import User
from django.http import Http404, JsonResponse, HttpResponseForbidden
from funcy import omit
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete


class CreateOfferView(LoginRequiredMixin, View):
    template_name = 'offers/create_offer.html'

    def get(self, request, **kwargs):
        if not request.user.allowed:
            return redirect('login')
        context = {
            'form': CreateOfferForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = CreateOfferForm(request.POST, request.FILES)
        company_id = kwargs['pk']
        images = request.FILES.getlist('image')

        company = Companies.objects.filter(id=company_id, owner=request.user).first()
        if not company:
            raise Http404

        if form.is_valid():

            obj = form.save(commit=False)
            obj.company = company
            obj.save()
            for i in images:
                OffersImages(offer=obj, image=i).save()

            return redirect('companies:create-company')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class DeleteOfferView(LoginRequiredMixin, DeleteView):
    template_name = 'offers/delete_offer.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Offers, id=self.request.POST.get('id'))
        if obj.company.owner == self.request.user:
            return obj
        raise Http404

    def get_success_url(self):
        return reverse('view-profile', kwargs={'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        data = {'deleted': True}
        return JsonResponse(data)


class UpdateOfferView(LoginRequiredMixin, View):
    template_name = 'offers/update_offer.html'

    def get(self, request, **kwargs):
        obj = get_object_or_404(Offers, id=kwargs['pk'])
        if obj.company.owner != request.user:
            raise Http404
        context = {
            'form': CreateOfferForm(initial={
                'type': obj.type,
                'coupon_price': obj.coupon_price,
                'currency': obj.currency,
                'retail_price': obj.retail_price,
                'title': obj.title,
                'amount': obj.amount
            }),
            'images': OffersImages.objects.filter(offer=obj).all()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        instance = get_object_or_404(Offers, id=kwargs['pk'])
        form = CreateOfferForm(request.POST, request.FILES, instance=instance)
        images = request.FILES.getlist('image')

        if form.is_valid():
            obj = form.save()
            for i in images:
                OffersImages(offer=obj, image=i).save()

            return redirect('companies:create-company')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


def delete_image_fun(request, id):
    post = OffersImages.objects.get(id=id)
    post.delete()
    return JsonResponse({'success': True, 'message': 'Delete', 'id': id})


@receiver(post_delete, sender=OffersImages)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


class MyOffersPageView(LoginRequiredMixin, View):
    template_name = 'offers/my_offers.html'

    def get(self, request, **kwargs):
        objects = Companies.objects.filter(owner=request.user).prefetch_related('offers_set').all()
        context = {
            'objects': objects
        }
        return render(request, self.template_name, context)

"""
class CatalogPageView(View):
    template_name = 'offers/catalog.html'

    def get(self, request, **kwargs):


"""














