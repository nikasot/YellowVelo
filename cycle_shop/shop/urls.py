from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.CycleIndex.as_view(), name='index'),
    path('create_cycle', views.CreateCycle.as_view(), name='create_cycle'),
    path('show_cycle/<slug:cycle_slug>', views.ShowCycle.as_view(), name='show_cycle'),
    path('show_category/<slug:category_slug>', views.ShowCategory.as_view(), name='show_category'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('personal', views.PersonalAccount.as_view(), name='personal'),
    path('change_password', views.ChangePassword.as_view(), name='change_password'),
    path('password_change_done', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('change_email', views.ChangeEmail.as_view(), name='change_email'),
    path('change_email_done', views.ChangeEmailDone.as_view(), name='change_email_done'),
    path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('buy/<slug:total_price>', views.Buy.as_view(), name='buy'),
    path('dostavka_i_oplata', views.DeliveryPayment.as_view(), name='dostavka_i_oplata'),
    path('about', views.About.as_view(), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
