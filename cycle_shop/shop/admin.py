from django.contrib import admin
from .models import Cycle, Category, User
from django.utils.translation import gettext_lazy as _

# Register your models here.

class CostFilter(admin.SimpleListFilter):
    title = _('Цена Товара')
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('under20', _('до 20 т.р')),
            ('20-50', _('от 20 до 50 т.р')),
            ('50-100', _('от 50 до 100 т.р')),
            ('over100', _('Свыше 100 т.р'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'under20':
            return queryset.filter(
                price__lte=20000
            )
        if self.value() == '20-50':
            return queryset.filter(
                price__gte=20000,
                price__lte=50000
            )
        if self.value() == '50-100':
            return queryset.filter(
                price__gte=50000,
                price__lte=100000
            )
        if self.value() == 'over100':
            return queryset.filter(
                price__gte=100000
            )


class CycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price')
    list_display_links = ('id', 'title')
    list_editable = ('price','category')
    search_fields = ('title',)
    list_filter = (CostFilter,)
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'date_joined')
    list_display_links = ('id', 'email')
    prepopulated_fields = {'email': ('email',)}


admin.site.register(User, UserAdmin)
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Category, CategoryAdmin)
