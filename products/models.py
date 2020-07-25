from django.db import models
from autoslug import AutoSlugField


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name

    def product_count(self):
        count = Product.objects.filter(
            categories=self, active=True).count()
        return count


def product_uploads(instance, filename):
    upload_path = "products"
    return os.path.join(upload_path, filename.lower())


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from="name")
    description = models.TextField()
    categories = models.ManyToManyField(ProductCategory)
    def_img = models.ImageField(
        upload_to="product_uploads", blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    product_order = models.PositiveIntegerField(
        help_text="Sets the display order for item on page",
        verbose_name="Display Ordering #",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["product_order", "name"]
