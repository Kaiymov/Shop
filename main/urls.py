from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from registration.backends.default.views import RegistrationView, ResendActivationView, ActivationView

from . import views
from .views import CustomResendActivationView

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('categories', views.CategoryList.as_view(), name='categories'),
    path('category/<slug:slug>/', views.ProductList.as_view(), name='product_list'),
    path('about', views.about_us, name='about_us'),
    # path('auth/login', views.auth_template),

    # DJANGO AUTH
    path('accounts/login', auth_views.LoginView.as_view(template_name='auth_user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth_user/logout.html'), name='auth_logout'),
    path('password/change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('auth_password_change_done')), name='auth_password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='auth_password_change_done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='auth_user/password_reset.html', success_url=reverse_lazy('auth_password_reset_done'), email_template_name='email_msg/password_reset.html'), name='auth_password_reset'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='auth_password_reset_complete'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_user/password_reset_done.html'), name='auth_password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('auth_password_reset_complete')),name='auth_password_reset_confirm'),

    # DJANGO-REGISTRATION-REDUX
    path('accounts/register',
         RegistrationView.as_view(template_name='auth_user/registration_form.html', success_url=reverse_lazy('home')),
         name='register'),
    path('activate/complete/',
         TemplateView.as_view(template_name='auth_user/activation_complete.html'),
         name='registration_activation_complete'),
    path('activate/resend/',
         CustomResendActivationView.as_view(template_name='auth_user/resend_activation_form.html'),
         name='registration_resend_activation'),
    path('activate/<activation_key>/',
         ActivationView.as_view(),
         name='registration_activate'),
    path('register/complete/',
         TemplateView.as_view(template_name='auth_user/registration_complete.html'),
         name='registration_complete'),
    path('register/closed/',
         TemplateView.as_view(template_name='auth_user/registration_closed.html'),
         name='registration_disallowed'),
]

