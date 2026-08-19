from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
class ProductForm(forms.ModelForm):
    images = forms.CharField(required=False, widget=MultipleFileInput())
    sale = forms.ChoiceField(choices=[
        (0,"new"),
        (1,"sale"),
    ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_sale'
        }
        )
    )
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'category',
            'brand',
            'sale',
            'sale_price',
            'company_profile',
            'detail',
            'images'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': ' Name',
                'class': 'form-control',
            }),

            'price': forms.NumberInput(attrs={
                'placeholder': 'Price',
                'class': 'form-control',
            }),

            'category': forms.Select(attrs={
                'placeholder': 'Please choose Category',
                'class': 'form-control',
            }),

            'brand': forms.Select(attrs={
                'placeholder': 'Please choose brand',
                'class': 'form-control',
            }),

            'sale': forms.NumberInput(attrs={
                'placeholder': 'Sale',
                'class': 'form-control',
            }),

            'company_profile': forms.TextInput(attrs={
                'placeholder': 'Company Profile',
                'class': 'form-control',
            }),

            'detail': forms.Textarea(attrs={
                'placeholder': 'Product Detail',
                'class': 'form-control',
                'rows': 5,
            }),
        }
    def clean_images(self):
        images = self.files.getlist("images")
        if len(images) > 3:
            raise ValidationError("Chỉ được upload tối đa 3 ảnh")
        # kiểm tra từng ảnh
        for image in images:
            if image.size > 1024 *1024:
                raise ValidationError(f"ảnh{image.name} vượt quá kích thước cho phép!")
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError( f"Ảnh {image.name} phải có định dạng png, jpg hoặc jpeg.")
        return images
        