from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField("Tag", related_name="posts", null=True, blank=True)
    is_active = models.BooleanField(default=True)


    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created_at = timezone.now()
    #         self.save()

    #     return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlockedUser(models.Model):
    id = models.AutoField(primary_key=True)
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_users")
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_by_users")
    is_blocked = models.BooleanField(default=True)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)