from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family_name = models.CharField(max_length=20, default='无姓')
    given_name = models.CharField(max_length=20, default='无名')
    description = models.CharField(max_length=512, default='他好像不愿意向你介绍自己。')
    phone = models.CharField(null=True, default='12345678910', max_length=20)
    mail = models.CharField(max_length=50, blank=True)
    nums = models.IntegerField(default=0) # total nums
    recent_nums = models.IntegerField(default=0) # maximum 6
    height = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    width = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    avatar = models.ImageField(upload_to='', height_field='height', width_field='width', blank=True)

    is_tengfei = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Goods(models.Model):
    typ = models.IntegerField(default=0) # 0 sell, 1 buy, 2 give
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    trade_location = models.CharField(max_length=32)
    price = models.CharField(max_length=10, default='0')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='', blank=True, null=True)
    seller = models.ForeignKey(UserProfile, blank=True ,null=True, on_delete=models.CASCADE)
    publish_time = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    typ = models.IntegerField(default=0) # 0 borrow, 1 give
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    picture = models.ImageField(upload_to='goods', blank=True, null=True)
    nums = models.IntegerField(default=0)
    publish_time = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    goods = models.ForeignKey(Goods,blank=True,null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,blank=True,null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    comment_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content


class InstationMessage(models.Model):
    goods = models.ForeignKey(Goods,blank=True,null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='receiver_id', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name='sender_id', on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    send_time = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content
