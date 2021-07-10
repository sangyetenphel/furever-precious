from store.models import Review
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store-home')
        else:
            messages.error(request, "Login Error! Username or password is incorrect.")
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'See you again!')
    return redirect('store-home')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Will save the user to database with hashed password and all that good stuff
            form.save()
            username = form.cleaned_data.get('username')
            # One-time message send to base.html (Also: info, error, warning etc)
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    reviews = Review.objects.filter(user=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'reviews': reviews,
    }
    return render(request, 'users/profile.html', context)


def user_review_delete(request, id):
    Review.objects.get(pk=id).delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('user-profile')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user-profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    def form_valid(self, form):
        messages.success(self.request, f"Password reset information has been sent to the email provided.")
        return super().form_valid(form)

    success_url = reverse_lazy('user-login')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, f"You can now login with your new password.")
        return super().form_valid(form)

    success_url = reverse_lazy('user-login')