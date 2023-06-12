from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'account'


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.register, name="signup"),
    # path('login/', LoginView.as_view(template_name='registration/login.html',
    #      form_class=CustomAuthenticationForm),  name='login')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
