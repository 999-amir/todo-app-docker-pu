from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import SignupForm, LoginForm, ProfileForm, ProfileDescriptionForm
from .models import CostumeUser, ProfileModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class SignupView(View):
    form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'you are still logged in', 'red-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'forms': self.form_class(),
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            CostumeUser.objects.create_user(email=cd['email'], password=cd['password_1'])
            messages.success(request, 'registered complete', 'green-600')
            return redirect('todo:main_page')
        context = {
            'forms': form,
        }
        return render(request, 'accounts/signup.html', context)


class LoginView(View):
    class_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'you are still logged in', 'red-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'forms': self.class_form()
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if not user.is_verify:
                    messages.warning(request, 'account still not verified', 'red-600')
                    return redirect('accounts:login')
                login(request, user)
                messages.success(request, 'login complete', 'green-600')
                return redirect('todo:main_page')
            messages.warning(request, 'incorrect information', 'orange-600')
            return redirect('accounts:login')
        context = {
            'forms': form
        }
        return render(request, 'accounts/login.html', context)


class LogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'red-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        messages.success(request, 'logout completed', 'blue-600')
        return redirect('todo:main_page')


class ProfileView(View):
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'red-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            'forms': form
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = get_object_or_404(ProfileModel, user=request.user)
            profile.f_name = cd['f_name']
            profile.l_name = cd['l_name']
            profile.description = cd['description']
            profile.save()
            messages.success(request, 'profile updated', 'green-600')
            return redirect('todo:main_page')
        context = {
            'forms': form
        }
        return render(request, 'accounts/profile.html', context)


class ProfileDescription(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'need registration', 'red-600')
            return redirect('todo:main_page')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = ProfileDescriptionForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(ProfileModel, user=request.user)
            profile.description = form.cleaned_data['description']
            profile.save()
        return redirect('accounts:profile')