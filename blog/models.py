from django.db import models
from embed_video.fields import EmbedVideoField
from autoslug import AutoSlugField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    filter_name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def post_count(self):
        count = VlogPost.objects.filter(
            categories=self, published=True).count()
        return count


def vlog_uploads(instance, filename):
    upload_path = "vlog"
    return os.path.join(upload_path, filename.lower())


class VlogPost(models.Model):
    video_url = EmbedVideoField(
        verbose_name="YouTube Link", blank=True, null=True)
    header_img = models.ImageField(
        upload_to="vlog_uploads", blank=True, null=True)
    title = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='title',
                         unique_with='created_at__month')
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at', ]
