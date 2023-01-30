from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from .forms import UserCreateForm, UserLoginForm, ProfileInfoForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from .models import Profile, Cities, User
from django.contrib.auth.mixins import LoginRequiredMixin
from funcy import omit
from last_seen.models import LastSeen


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreateForm()
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
            'form': form
        }

        return render(request, self.template_name, context)


class SetProfileInfo(LoginRequiredMixin, View):
    template_name = 'registration/setprofileinfo.html'

    def get(self, request):
        if request.user.allowed:
            return redirect('login')
        context = {
            'form': ProfileInfoForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
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
            'form': UserLoginForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('companies:create-company')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'registration/profile.html'

    def get(self, request, **kwargs):
        if not request.user.allowed:
            return redirect('set-profile-info')
        owner = 0
        s_user = kwargs['pk']
        if request.user.id == s_user:
            owner = 1

        user = User.objects.filter(id=s_user).prefetch_related('companies_set', 'profile_set').all()
       # print(user[0].companies_set.all())

        if not user:
            return redirect('404')

        seen = LastSeen.objects.when(user=user[0])

        context = {
            'user': user[0],
            'owner': owner,
            'seen': seen
        }

        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'registration/update_profile.html'

    def get(self, request):
        if not request.user.allowed:
            return redirect('login')

        profile = get_object_or_404(Profile, user=request.user)

        context = {
            'form': ProfileUpdateForm(initial={
                'phone_num': profile.phone_num,
                'phone_num_show': profile.phone_num_show,
                'bio': profile.bio,
                'city': profile.city.city,
                'first_name': profile.user.first_name,
                'last_name': profile.user.last_name
            })
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileUpdateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            obj = get_object_or_404(Profile, user=request.user)
            obj.user.first_name = data['first_name']
            obj.user.last_name = data['last_name']
            obj.city = Cities.objects.get(city=data['city'])
            obj.phone_num = data['phone_num']
            obj.phone_num_show = data['phone_num_show']
            obj.save()
            return redirect(reverse('view-profile', kwargs={'pk': request.user.id}))

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
