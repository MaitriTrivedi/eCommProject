from django import forms
from products.models import Products

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Products
        fields=['product_id','product_name','price','description','category','quantity','product_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows':3,'cols':30})
        }
        exclude=['seller']