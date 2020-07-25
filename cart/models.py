from django.db import models
from django.utils.translation import ugettext_lazy as _
from products.models import Product


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_("creation date"))
    checked_out = models.BooleanField(
        default=False, verbose_name=_("checked out"))
    # sales_tax = models.DecimalField(
    #     max_digits=7, decimal_places=2, blank=True, null=True
    # )

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ("-creation_date",)

    def __unicode__(self):
        return unicode(self.creation_date)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_(
        "cart"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"))
    unit_price = models.DecimalField(
        max_digits=18, decimal_places=2, verbose_name=_("unit price")
    )
    # product as generic relation
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ("cart",)

    def __unicode__(self):
        return u"%d units of %s" % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price

    total_price = property(total_price)
