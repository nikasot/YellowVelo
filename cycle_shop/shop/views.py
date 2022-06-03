import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, TemplateView

from cart.cart import Cart
from cart.context_processors import cart
from .utils import ContextMixin, UserData, StaffRequiredMixin

from .form import RegisterUserForm, LoginUserForm, PostForm, EmailChangeForm
from .models import Cycle, Category
from cart.forms import CartAddProductForm
from cloudipsp import Api, Checkout

logger = logging.getLogger('shop')
logger_create_cycle = logging.getLogger('shop_create_cycle')
logger_auth = logging.getLogger('shop_auth')


class CycleIndex(UserData, ContextMixin, ListView):
    model = Cycle
    template_name = 'shop/index.html'
    context_object_name = 'cycles'
    paginate_by = 12

    def get_queryset(self):
        logger.info('Getting cycles from db', extra=self.get_user_data())
        return CycleIndex.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class CreateCycle(UserData, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    login_url = reverse_lazy('shop:login')
    permission_required = 'is_staff'
    template_name = 'shop/create_cycle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        logger_create_cycle.info(f'\nCreating cycle... '
                                 f'title: {self.request.POST["title"]}, '
                                 f'category: {self.request.POST["category"]}, '
                                 f'description: {self.request.POST["description"]}, '
                                 f'price: {self.request.POST["price"]} ',
                                 extra=self.get_user_data())
        return super().post(request, *args, **kwargs)


class ShowCycle(DetailView):
    model = Cycle
    template_name = 'shop/show_cycle.html'
    slug_url_kwarg = 'cycle_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class ShowCategory(ContextMixin, ListView):
    model = Cycle
    template_name = 'shop/index.html'
    context_object_name = 'cycles'

    def get_queryset(self):
        return ShowCategory.model.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        user_context = self.get_user_context(title=f'Категория: {category.name}')
        context |= user_context
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('shop:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Регистрация'
        return context


class LoginUser(UserData, LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        logger_auth.info('[Success login]', extra=self.get_user_data())
        if self.request.GET.get('next') is None:
            return reverse('shop:index')
        else:
            return self.request.GET.get('next')
            # return reverse('shop:' + self.request.GET.get('next')[1:])


class LogoutUser(UserData, LogoutView):
    next_page = 'shop:index'

    def get_next_page(self):
        next_page = super(LogoutUser, self).get_next_page()
        logger_auth.info('[Logout]', extra=self.get_user_data())
        return next_page


class PersonalAccount(TemplateView):
    template_name = 'shop/personal_acc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'shop/change_password.html'
    success_url = reverse_lazy("shop:password_change_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PasswordChangeDone(ChangePassword, TemplateView):
    template_name = 'shop/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_changed'] = 'Пароль успешно изменен'
        return context


class ChangeEmail(PasswordChangeView):
    form_class = EmailChangeForm
    template_name = 'shop/change_email.html'
    success_url = reverse_lazy("shop:change_email_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChangeEmailDone(ChangeEmail, TemplateView):
    template_name = 'shop/change_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_changed'] = 'Почтовый адрес успешно изменен'
        return context


def product_detail(request, slug):
    product = get_object_or_404(slug=slug,
                                available=True)
    # product = Cycle.objects.get(slug=slug,
    #                             available=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/show_cycle.html',
        {'product': product, 'cart_product_form': cart_product_form}
    )


class SearchResultsView(ListView):
    model = Cycle
    template_name = 'shop/search_results.html'
    context_object_name = 'cycles'

    def get_queryset(self):  # новый
        # return Cycle.objects.filter(title__icontains='forward')

        query = self.request.GET.get('q')
        object_list = Cycle.objects.filter(title__icontains=query)
        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cycles = Cycle.objects.all()
    #     context['cycles'] = cycles
    #     return context


class Buy(View):
    model = Cycle
    template_name = 'shop/show_cycle.html'

    # def get(self, request, slug):
    #     product = Cycle.objects.get(slug=slug)
    #     api = Api(merchant_id=1396424, secret_key='test')
    #     checkout = Checkout(api=api)
    #     data = {
    #         "currency": "RUB",
    #         "amount": str(product.price) + '00'
    #     }
    #     url = checkout.url(data).get('checkout_url')
    #     print(url)
    #     return redirect(url)
    def get(self, request, total_price):
        print(type(total_price))
        api = Api(merchant_id=1396424, secret_key='test')
        checkout = Checkout(api=api)
        data = {
            "currency": "RUB",
            "amount": str(total_price) + '00'
        }
        url = checkout.url(data).get('checkout_url')
        print(url)
        return redirect(url)


class DeliveryPayment(TemplateView):
    template_name = 'shop/oplata_i_dostavka.html'


class About(TemplateView):
    template_name = 'shop/about.html'


