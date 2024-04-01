from django.db import models
from apps.commons.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parents = models.ManyToManyField('self', symmetrical=False, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def get_all_paths(self):
        """
        Recursively gets all paths from root to current category.
        Each path is a list of category titles from root to the current category.
        """
        def get_paths(category, current_path):
            if category.parents.count() == 0:
                return [current_path]
            paths = []
            for parent in category.parents.all():
                paths.extend(get_paths(parent, [parent.title] + current_path))
            return paths

        all_paths = get_paths(self, [self.title])
        return [' > '.join(path) for path in all_paths]


