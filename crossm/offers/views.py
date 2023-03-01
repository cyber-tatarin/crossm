from django.core.paginator import Paginator, EmptyPage
from django.core.serializers import serialize
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateOfferForm
from companies.models import Companies, Countries
from .models import OffersImages, Offers
from django.views.generic import DeleteView
from users.models import User
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from funcy import omit
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete, pre_save
from users.views import get_profile_ph
from users.models import Profile
import json
from users.views import is_allowed


class CreateOfferView(LoginRequiredMixin, View):
    template_name = 'offers/create_offer.html'

    def get(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        context = {
            'form': CreateOfferForm(),
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

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

            nexty = request.POST.get('next')
            if nexty:
                try:
                    return HttpResponseRedirect(nexty)
                except:
                    raise Http404
            else:
                return redirect('offers:my-offers')

        context = {
            'form': form,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class DeleteOfferView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        obj = get_object_or_404(Offers, id=request.POST.get('id'))

        if obj.company.owner != self.request.user:
            raise Http404

        obj.delete()
        data = {'deleted': True, 'success': True}
        return JsonResponse(data)


class UpdateOfferView(LoginRequiredMixin, View):
    template_name = 'offers/update_offer.html'

    def get(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

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
                'amount_min': obj.amount_min,
                'amount_max': obj.amount_max
            }),
            'images': OffersImages.objects.filter(offer=obj).all(),
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        instance = get_object_or_404(Offers, id=kwargs['pk'])

        if instance.company.owner != request.user:
            raise Http404

        form = CreateOfferForm(request.POST, request.FILES, instance=instance)
        images = request.FILES.getlist('image')

        if form.is_valid():
            obj = form.save()
            for i in images:
                OffersImages(offer=obj, image=i).save()

            nexty = request.POST.get('next')
            if nexty:
                try:
                    return HttpResponseRedirect(nexty)
                except:
                    raise Http404
            else:
                return redirect('offers:my-offers')

        context = {
            'form': form,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class OfferImageDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post = get_object_or_404(OffersImages, id=request.GET.get('id'))
        if post.offer.company.owner == request.user:
            post.delete()
            return JsonResponse({'success': True})
        else:
            return Http404


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

        try:
            is_allowed(request)
        except PermissionError:
            return redirect('set-profile-info')

        objects = Companies.objects.filter(owner=request.user).prefetch_related('offers_set',
                                                                                'owner__profile_set').all()
        context = {
            'objects': objects,
            'profile_ph': get_profile_ph(request),
        }
        return render(request, self.template_name, context)


class SendImagesView(View):
    def get(self, request, **kwargs):
        images = OffersImages.objects.filter(offer=request.GET.get('id')).all()
        res = []
        for image in images:
            res.append(image.image.url)
        return JsonResponse({'images': res})


class CatalogPageView(View):
    template_name = 'offers/catalog.html'

    def get(self, request, **kwargs):
        offers = Offers.objects.prefetch_related('offersimages_set', 'company__owner__profile_set').order_by(
            '-id').all()
        currencies = Offers.objects.values('currency').distinct()
        niches = Companies.objects.values('niche').distinct()

        # niche = request.GET.get('niche')
        # if niche:
        #     initial_offers = initial_offers.filter(company__niche=niche)
        #
        # amount_min = request.GET.get('amount_min')
        # amount_max = request.GET.get('amount_max')
        # if amount_min and amount_max:
        #     initial_offers = initial_offers.filter(amount_min__lte=amount_max, amount_max__gte=amount_min)
        # elif amount_min:
        #     initial_offers = initial_offers.filter(amount_max__gte=amount_min)
        # elif amount_max:
        #     initial_offers = initial_offers.filter(amount_min__lte=amount_max)
        #
        # currency = request.GET.get('currency')
        # if currency:
        #     initial_offers = initial_offers.filter(currency=currency)
        #
        # retail_price_min = request.GET.get('retail_price_min')
        # retail_price_max = request.GET.get('retail_price_max')
        # if retail_price_min and retail_price_max:
        #     initial_offers = initial_offers.filter(retail_price__gte=retail_price_min,
        #                                            retail_price__lte=retail_price_max)
        # elif retail_price_min:
        #     initial_offers = initial_offers.filter(retail_price__gte=retail_price_min)
        # elif retail_price_max:
        #     initial_offers = initial_offers.filter(retail_price__lte=retail_price_max)
        #
        # coupon_price_min = request.GET.get('coupon_price_min')
        # coupon_price_max = request.GET.get('retail_price_max')
        # if coupon_price_min and coupon_price_max:
        #     initial_offers = initial_offers.filter(retail_price__gte=coupon_price_min,
        #                                            retail_price__lte=coupon_price_max)
        # elif coupon_price_min:
        #     initial_offers = initial_offers.filter(retail_price__gte=coupon_price_min)
        # elif coupon_price_max:
        #     initial_offers = initial_offers.filter(retail_price__lte=coupon_price_max)
        #
        # country = request.GET.get('country')
        # if country:
        #     initial_offers = initial_offers.filter(company__country_of_res=country)
        #
        # phone_num_show = request.GET.get('phone_num_show')
        # #phone_num_show = 1
        # if phone_num_show:
        #     suitable_users = Profile.objects.filter(phone_num_show=True).values_list('user_id', flat=True)
        #     initial_offers = initial_offers.filter(company__owner__id__in=suitable_users)
        #
        # print(initial_offers)
        #
        # p = Paginator(initial_offers, 2)
        #
        # page = request.GET.get('page')
        #
        # try:
        #     res = p.page(page)
        # except EmptyPage:
        #     raise Http404
        #
        # serialized_data = serialize("json", res, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        # print(serialized_data)
        #
        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse(serialized_data, safe=False)
        try:
            profile_ph = get_profile_ph(request)
        except TypeError:
            profile_ph = None

        context = {
            'offers': offers,
            'profile_ph': profile_ph,
            'currencies': currencies,
            'niches': niches,
        }
        return render(request, self.template_name, context)


@receiver(post_delete, sender=OffersImages)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        img = OffersImages.objects.filter(offer=instance.offer).first()
        obj = Offers.objects.get(id=instance.offer.id)
        if not img:
            obj.has_photo = False
            obj.save()
    except:
        pass


@receiver(pre_save, sender=OffersImages)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        obj = Offers.objects.get(id=instance.offer.id)
        if not obj.has_photo:
            obj.has_photo = True
            obj.save()
    except:
        pass
