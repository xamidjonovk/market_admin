from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .forms import ProductAdminForm
from rangefilter.filters import NumericRangeFilterBuilder


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'orders_count', 'first_image_display')
    readonly_fields = ('first_image_detail_display', 'orders_count')
    search_fields = ('id', 'title')
    list_filter = ['is_active', ("price", NumericRangeFilterBuilder()), ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(orders_count=Count('orders'))  # Correct annotation
        return queryset

    def first_image_display(self, obj):
        if obj.images:
            return self.image_display_helper(obj.images[0])

    first_image_display.short_description = 'First Image'

    def first_image_detail_display(self, obj):
        if obj.images:
            return self.image_display_helper(obj.images[0])

    first_image_detail_display.short_description = 'first image'

    def image_display_helper(self, image):
        if image:
            return format_html('<img src="{}" style="max-height: 80px;"/>', image)
        return "No Image"

    def orders_count(self, obj):
        # Use the annotated 'ordered_count' for display
        return obj.orders_count
    orders_count.admin_order_field = 'orders_count'  # Allows sorting by this annotated field
    orders_count.short_description = 'Ordered Count'

