from django.db import models
from django.db.models.deletion import DO_NOTHING
from accounts.models import CustomUser
from django.db.models.fields import related
from blog.utils import generate_unique_slug
from django.utils.text import slugify
# from ckeditor.fields import RichTextField
# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=264, verbose_name="Put a Title")
    slug = models.SlugField(max_length=264, unique=True)
    blog_content = models.TextField(verbose_name="What is on your mind?")
    # blog_content = RichTextField(verbose_name="What is on your mind?")
    blog_image = models.ImageField(upload_to='blog_images', verbose_name="Image")
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date',]

    # generate unique slug
    def save(self, *args, **kwargs): 
        if self.slug:  # edit
            if slugify(self.blog_title) != self.slug:
                self.slug = generate_unique_slug(Blog, self.blog_title)
        else:  # create
            self.slug = generate_unique_slug(Blog, self.blog_title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)
        
    def __str__(self):
        return self.comment