from django.contrib import admin
from market.models import Category, Goods, UserProfile, Comment, InstationMessage, Book
# Register your models here.

admin.site.register(Category)
admin.site.register(Goods)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(InstationMessage)
admin.site.register(Book)