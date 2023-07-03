from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
from .forms import CustomAuthenticationForm, LoginForm, RegisterUserForm
from .models import Organizations, Staff_user
from account.translate import to_cyrillic, to_latin

import redis, json

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


def register(request):
    if request.user.is_authenticated:
        return redirect('quiz:dashboard')
    form = RegisterUserForm()
    # request.session['date'] = str(datetime.now())
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                data = json.loads(r.get(user.pinfl))
                print(data)

                organization_railway = to_cyrillic(data['organization']['name']) if str(
                    data['organization']['name']).isascii() else \
                    data['organization']['name']

                organization = to_cyrillic(data['organization']['railway']['name']) if str(
                    data['organization']['railway']['name']).isascii() else \
                    data['organization']['railway']['name']

                department = to_cyrillic(data['staff'][0]['department']['name']) if str(
                    data['staff'][0]['department']['name']).isascii() else \
                    data['staff'][0]['department']['name']

                staff_full = to_cyrillic(data['staff'][0]['staff_full']) if str(
                    data['staff'][0]['staff_full']).isascii() else data['staff'][0]['staff_full']

                org, create = Organizations.objects.get_or_create(organization=organization)
                # staff, staff_create = Staff_user.objects.get_or_create(staff=staff_full,
                #                                                        organization__organization=department)

                if create:
                    org_railway = Organizations.objects.create(organization=organization_railway, parent=org)
                    obj = Organizations.objects.create(organization=department, parent=org_railway)
                    user.organizations = obj
                    staff, staff_create = Staff_user.objects.get_or_create(staff=staff_full,
                                                                           organization=obj)
                    user.staff_user = staff
                    user.save()
                else:
                    org_railway, create_railway = Organizations.objects.get_or_create(organization=organization_railway,
                                                                                      parent=org)
                    child, create_child = Organizations.objects.get_or_create(organization=department,
                                                                              parent=org_railway)
                    user.organizations = child

                    staff, staff_create = Staff_user.objects.get_or_create(staff=staff_full,
                                                                           organization=child)

                    user.staff_user = staff

                    user.save()

            messages.success(request, f'{user}user muvaffaqiyatli saqlandi')
            return redirect('account:login')

    context = {
        'forms': form
    }
    return render(request, 'registration/signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:dashboard')
    # messages.success(request, 'Login yoki parol xato kiritildi')

    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz:dashboard')
            else:
                messages.warning(request, 'Login yoki parol xato kiritildi')
                return render(request, 'registration/login.html', {'form': form})

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('account:login')

# info user data views

# bu yerda foydalanuvchining test statistika funcsiyalari
