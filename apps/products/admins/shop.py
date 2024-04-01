from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_display')
    search_fields = ('id', 'title')

    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;"/>', settings.MEDIA_URL + str(obj.image))
        return "No Image"

    image_display.short_description = 'Image'


