from django import forms
from ..models import Product
from django.core.files.storage import default_storage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    images = MultipleFileField(label='Select files', required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle image upload
        images = self.files.getlist('images')
        image_urls = []
        for image in images:
            path = default_storage.save(f'product_images/{image.name}', image)
            url = default_storage.url(path)
            image_urls.append(url)

        if image_urls:
            instance.images = image_urls

        if commit:
            instance.save()
        return instance
