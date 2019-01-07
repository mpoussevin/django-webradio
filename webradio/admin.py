from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from webradio.models import Station, Category

admin.site.register(Category)


class StationCategoryFilter(admin.SimpleListFilter):
    title = _('Category')
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return Category.objects.all().values_list('id', 'name')

    def queryset(self, request, queryset):
        try:
            category_id = int(self.value())
        except:
            return queryset
        else:
            return queryset.filter(category_id=category_id)


class StationAdmin(admin.ModelAdmin):
    list_filter = (StationCategoryFilter,)


admin.site.register(Station, StationAdmin)
