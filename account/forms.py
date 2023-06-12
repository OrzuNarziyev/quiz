import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Organizations, Staff_user
from account.utils.auth_token import get_info

import re


# email = 'railtest-coll@railway.ajk'
# password = 'RailWayTest12345%^&'
# login_endpoint = 'https://api-exodim.railway.uz/api/auth/collaborator/login'
# endpoint = "https://api-exodim.railway.uz/api/collaborator/cadry/check"
#
# def get_info(pinfl):
#
#     data = {
#         'pinfl': pinfl
#     }
#     cache.set('key', 'qiymat')
#     if cache.get('access_token') is None:
#         api = api_login()
#         print(api)
#         token = cache.get('access_token')
#         type_api = cache.get('token_type')
#         headers = {
#             'Authorization': f"{token} {type_api}"
#         }
#     else:
#         token = cache.get('access_token')
#         type_api = cache.get('token_type')
#         headers = {
#             'Authorization': f"{token} {type_api}"
#         }
#     get_response = requests.get(endpoint, headers=headers, params=data)
#     if get_response.status_code == 200:
#         print(get_response.json(), )
#         return get_response.json()
#     else:
#         return None
#
#
# def api_login():
#     get_acces_token = requests.post(login_endpoint, data={
#         'email': email,
#         'password': password
#     })
#     if get_acces_token.status_code == 200:
#         # print('status code 200 ')
#
#         access_token = get_acces_token.json()['access_token']
#         token_type = get_acces_token.json()['token_type']
#         cache.set('access_token', access_token, 21600)
#         cache.set('token_type', token_type, 21600)
#         context = {
#             'access_token': access_token,
#             'token_type': token_type
#         }
#         return context
#     else:
#         return None


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label=_('login'),
                                                  widget=forms.TextInput(attrs={'class': 'input100 has-val'}))
        self.fields['password'] = forms.CharField(label=_('password'),
                                                  widget=forms.PasswordInput(attrs={'class': 'input100 has-val'}))


class LoginForm(forms.Form):
    username = forms.CharField(label=_('login yoki parol'),
                               widget=forms.TextInput(attrs={'class': 'input100 has-val'}))
    password = forms.CharField(label=_('Parol'),
                               widget=forms.PasswordInput(attrs={'class': 'input100 has-val'}))


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['pinfl', 'username',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):

        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(
            label=_('Login'), widget=forms.TextInput(attrs={'type': 'text', 'class': 'input100 has-val'})
        )
        self.fields['pinfl'] = forms.CharField(label=_('JSHSHR'),
                                               widget=forms.TextInput(
                                                   attrs={'type': 'text', 'class': 'input100 has-val'}))
        self.fields['password1'] = forms.CharField(label=_('Parol'),
                                                   widget=forms.TextInput(
                                                       attrs={'type': 'password', 'class': 'input100 has-val'}))
        self.fields['password2'] = forms.CharField(
            label=_('Parolni qaytadan kiriting'),
            widget=forms.TextInput(
                attrs={'type': 'password', 'class': 'input100 has-val'})
        )

    def clean_pinfl(self):
        pinfl = self.cleaned_data['pinfl']
        info = get_info(pinfl=pinfl)
        print(info)
        if info == 200:
            user = cache.get(pinfl)
            print(user)
            return pinfl
        else:
            raise forms.ValidationError(_('Bu foydalanuvchi e-xodim dasturida topilmadi'))

    # 32512985330016

    # phone = re.findall('[0-9]+', data)
    # if CustomUser.objects.filter(phone_number=''.join(phone)).exists():
    #     raise forms.ValidationError(_('Bu raqam allaqachon mavjud'))
    # return ''.join(phone)

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if CustomUser.objects.filter(email=data).exists():
    #         raise forms.ValidationError(
    #             _('Bu electron pochta ro\'xatdan o\'tgan'))
    #     return data
    #
    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     if CustomUser.objects.filter(username=data).exists():
    #         raise forms.ValidationError(
    #             _('Bu foydalanuvchi ro\'yxatdan o\'tgan'))
    #     return data.lower()

    # def clean_full_name(self):
    #     data = self.cleaned_data['full_name']
    #     list_data = data.split(' ')
    #     print(list_data)
    #     print(list_data[0])
    #     print(list_data[1])
    #     print(list_data[2:])
    #     if len(list_data) == 3:
    #         data = list(map(lambda s: str(s).capitalize(), list_data))
    #     elif len(list_data) == 4:
    #         data = list(map(lambda s: str(s).capitalize(), list_data[:3]))
    #         data[2] = data[2] + ' ' + list_data[3].lower()
    #     elif len(list_data) < 3 or len(list_data) > 4:
    #         raise forms.ValidationError(
    #             _("Ism Familya Sharif ni to'liq kiriting"))
    #
    #     return ' '.join(data)

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     cd = self.cleaned_data
    #     full_name = tuple(str(cd['full_name']).split(' '))
    #     last_name = full_name[0]
    #     first_name = full_name[1]
    #     fathers_name = ' '.join(full_name[2:])
    #     # (last_name, first_name, fathers_name) = full_name
    #     instance.last_name = last_name
    #     instance.first_name = first_name
    #     instance.father_name = fathers_name
    #     if commit:
    #         instance.save()
    #     return instance

    # self.fields['full_name'] = forms.CharField(
    #     label=_('Familya Ism Sharif'), widget=forms.TextInput(attrs={'type': 'text', 'class': 'input100'})
    #
    # )
    # self.fields['position'] = forms.ModelChoiceField(queryset=Grade.objects.all(), label=_('Lavozim'),
    #                                                  widget=forms.Select(attrs={'type': 'text', 'class': 'input100', 'style':'border:none;outline:none;'}))
    #
    # self.fields['work_place'] = forms.ModelChoiceField(queryset=Work_place.objects.all(), label=_('Ish joyi'),
    #                                                    widget=forms.Select(attrs={'type': 'text', 'class': 'input100','style':'border:none;outline:none;'}))
    #
    # self.fields['phone_number'] = forms.CharField(label=_('Telefon Raqam'), widget=forms.NumberInput(
    #     attrs={'data-format': "+(*****) ***-**-**", "data-mask": "+(998__) __-__-__", 'type': 'tel',
    #            'class': 'input100'}))
