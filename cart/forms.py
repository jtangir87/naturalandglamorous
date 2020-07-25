from django import forms
# from phone_field import PhoneFormField
# from localflavor.us.forms import USStateField, USStateSelect
from products.models import Product
# from customers.models import Location


class AddToCartForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(active=True), widget=forms.HiddenInput
    )
    quantity = forms.IntegerField(widget=forms.HiddenInput)


# class DeliveryCheckoutForm(forms.Form):
#     name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     phone = PhoneFormField(required=True)
#     street_1 = forms.CharField(required=False, label="Street")
#     city = forms.CharField(required=False)
#     state = USStateField(widget=USStateSelect)
#     zip = forms.IntegerField(required=False)
#     pd_date = forms.DateField(
#         label="Delivery Date", widget=DatePickerInput(), required=False
#     )
#     notes = forms.CharField(
#         widget=forms.Textarea(
#             attrs={"placeholder": "Please make any special requests here"}
#         ),
#         required=False,
#     )

#     def clean(self):
#         data = self.cleaned_data
#         if data["street_1"] == "":
#             self.add_error("street_1", "Please complete for delivery")
#         elif data["city"] == "":
#             self.add_error("city", "Please complete for delivery")
#         elif data["zip"] == "":
#             self.add_error("zip", "Please complete for delivery")

#         return data
