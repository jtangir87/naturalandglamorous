from django import forms

from localflavor.us.forms import USStateField, USStateSelect
from products.models import Product


class AddToCartForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(active=True), widget=forms.HiddenInput
    )
    quantity = forms.IntegerField(widget=forms.HiddenInput)


class CheckoutForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    street_1 = forms.CharField(required=False, label="Street")
    city = forms.CharField(required=False)
    state = USStateField(widget=USStateSelect)
    zip = forms.IntegerField(required=False)

    def clean(self):
        data = self.cleaned_data
        if data["street_1"] == "":
            self.add_error("street_1", "Please complete for delivery")
        elif data["city"] == "":
            self.add_error("city", "Please complete for delivery")
        elif data["zip"] == "":
            self.add_error("zip", "Please complete for delivery")

        return data
