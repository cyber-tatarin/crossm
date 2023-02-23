import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.views.generic import TemplateView
from funcy import omit
from last_seen.models import LastSeen
from .forms import UserCreateForm, UserLoginForm, ProfileInfoForm, ProfileUpdateForm
from .models import Profile, Cities, User
from .services import AiGeneratorChooser
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


def get_profile_ph(request):
	try:
		obj = Profile.objects.filter(user=request.user).first()
		if obj:
			if obj.photo:
				return obj.photo.url
			else:
				return None
		else:
			return None
	except TypeError:
		return None


def is_allowed(request):
	if not request.user.allowed:
		raise PermissionError


class RegisterView(View):
	template_name = 'registration/register.html'

	def get(self, request):
		context = {
			'form': UserCreateForm(),
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserCreateForm(request.POST)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=password)
			login(request, user)
			return redirect('set-profile-info')

		context = {
			'form': form,
		}

		return render(request, self.template_name, context)


class SetProfileInfo(LoginRequiredMixin, View):
	template_name = 'registration/setprofileinfo.html'

	def get(self, request):
		if request.user.allowed:
			raise Http404

		context = {
			'form': ProfileInfoForm(),
			'profile_ph': get_profile_ph(request),
		}
		return render(request, self.template_name, context)

	def post(self, request):
		if request.user.allowed:
			raise Http404

		form = ProfileInfoForm(request.POST)

		if form.is_valid():
			data = form.cleaned_data
			r_data = omit(data, 'city')
			obj = Profile(**r_data)
			obj.user = request.user
			obj.city = Cities.objects.get(city=data['city'])
			obj.save()
			request.user.allowed = 1
			request.user.save()
			return redirect('companies:create-company')

		context = {
			'form': form,
		}
		return render(request, self.template_name, context)


class LoginView(View):
	template_name = 'registration/login.html'

	def get(self, request):
		context = {
			'form': UserLoginForm(),
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserLoginForm(request, request.POST)

		if form.is_valid():
			user = form.get_user()
			login(request, user)

			nexty = request.POST.get('next')
			if nexty:
				try:
					return HttpResponseRedirect(nexty)
				except:
					raise Http404
			else:
				return redirect('offers:catalog')

		context = {
			'form': form
		}

		return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
	template_name = 'registration/profile.html'

	def get(self, request, **kwargs):

		try:
			is_allowed(request)
		except PermissionError:
			return redirect('set-profile-info')

		owner = 0
		s_user = kwargs['pk']
		if request.user.id == s_user:
			owner = 1

		user = User.objects.filter(id=s_user).prefetch_related('companies_set', 'profile_set').all()
		# print(user[0].companies_set.all())

		if not user:
			return redirect('404')

		try:
			seen = LastSeen.objects.when(user=user[0])
		except ObjectDoesNotExist:
			seen = "Давно"

		context = {
			'user': user[0],
			'owner': owner,
			'seen': seen,
			'profile_ph': get_profile_ph(request),
		}

		return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
	template_name = 'registration/update_profile.html'

	def get(self, request):

		try:
			is_allowed(request)
		except PermissionError:
			return redirect('set-profile-info')

		profile = get_object_or_404(Profile, user=request.user)

		context = {
			'form': ProfileUpdateForm(request.user.id, initial={
				'phone_num': profile.phone_num,
				'phone_num_show': profile.phone_num_show,
				'bio': profile.bio,
				'city': profile.city.city,
				'first_name': profile.user.first_name,
				'last_name': profile.user.last_name
			}),
			'profile_ph': get_profile_ph(request),
		}

		return render(request, self.template_name, context)

	def post(self, request):

		try:
			is_allowed(request)
		except PermissionError:
			return redirect('set-profile-info')

		form = ProfileUpdateForm(request.user.id, request.POST)

		if form.is_valid():
			data = form.cleaned_data
			obj = get_object_or_404(Profile, user=request.user)
			obj.user.first_name = data['first_name']
			obj.user.last_name = data['last_name']
			obj.city = Cities.objects.get(city=data['city'])
			obj.phone_num = data['phone_num']
			obj.phone_num_show = data['phone_num_show']
			obj.bio = data['bio']
			obj.save()
			return redirect(reverse('view-profile', kwargs={'pk': request.user.id}))

		context = {
			'form': form,
			'profile_ph': get_profile_ph(request),
		}
		return render(request, self.template_name, context)


class ProfilePhotoUpload(LoginRequiredMixin, View):

	def post(self, request, **kwargs):
		obj = get_object_or_404(Profile, user=request.user)
		obj.photo = request.FILES.get('image')
		obj.save()
		return JsonResponse({'success': True, 'image': obj.photo.url})


class DeletePhotoView(LoginRequiredMixin, View):

	def post(self, request, **kwargs):
		obj = get_object_or_404(Profile, user=request.POST.get('id'))
		obj.photo = None
		obj.save()
		return JsonResponse({'success': True})


@receiver(pre_save, sender=Profile)
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


class WhatisCMView(TemplateView):
	template_name = 'registration/what_is_cm.html'

	def get_context_data(self, **kwargs):
		return {'profile_ph': get_profile_ph(self.request)}


class CheckProfilePhoto(LoginRequiredMixin, View):
	def get(self, request, **kwargs):
		obj = get_object_or_404(Profile, user=request.user)
		if obj.photo:
			return JsonResponse({'success': True, 'image': obj.photo.url})
		else:
			return JsonResponse({'success': True, 'image': False})


class GetAiHelp(View):
	@method_decorator(ratelimit(key='ip', rate='5/d', method='GET'))
	def get(self, request, *args, **kwargs):
		company = request.GET.get('company')
		g_type = request.GET.get('g_type')
		lang = request.GET.get('lang')
		aig = AiGeneratorChooser(g_type=g_type, company=company, lang=lang)
		return JsonResponse({'text': aig.execute()})
		# return JsonResponse({'text': {'translated': 'gogo', 'original': 'lokaloka'}})
		# return JsonResponse({'text': {'error': True}})


