from django.contrib.auth.mixins import AccessMixin
from django.core.cache import cache
from .models import Category
from cart.cart import Cart


class ContextMixin:

    def get_user_context(self, **kwargs) -> dict:
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('categories', categories, 60)
        context['categories'] = categories
        return context


class StaffRequiredMixin(AccessMixin):
    """Verify that the current user is staff."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserData:
    def get_user_data(self):
        user_data = {
            'username': self.request.user,
            'user_ip': self.request.META['REMOTE_ADDR'],
            'path': self.request.path,
        }
        # if self.request.method == 'POST':
        #     user_data['POST'] = self.request.POST
        return user_data

