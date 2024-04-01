from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html_join


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('id', 'title')
    readonly_fields = ('all_paths',)

    def all_paths(self, obj):
        paths = obj.get_all_paths()
        return format_html_join('\n', "<li>{}</li>", ((path,) for path in paths)) or 'No parents'
    all_paths.short_description = "All Paths to Category"

    def get_search_results(self, request, queryset, search_term):
        """
        Extend the search functionality to allow searching by ID, title,
        and parent category's title using Q objects for complex queries.
        """
        if search_term:
            query = Q(id__icontains=search_term) | Q(title__icontains=search_term) | Q(
                parents__title__icontains=search_term)
            queryset = queryset.filter(query).distinct()
            use_distinct = True
        else:
            queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

