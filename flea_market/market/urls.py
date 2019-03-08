from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^favicon\.ico$', favicon_view),
    url(r'^$', views.homepage, name='homepage' ),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^forget_password/$', views.forget_password, name='forget_password'),
    #url(r'^about/', views.about,name='about'),
    url(r'^logout/$', views.user_logout,name='logout'),
    url(r'^add_comment/(?P<goods_id>[\w\-]+)', views.add_comment, name='add_comment'),
    url(r'^add_message/(?P<user_id>[\w\-]+)/(?P<goods_id>[\w\-]+)', views.add_message, name='add_message'),
    url(r'^search/(?P<typ_id>[\w\-]+)',views.search,name='search'),
    #url(r'^search_book/(?P<typ_id>[\w\-]+)', views.search_book, name='search_book'),
    url(r'^goods/(?P<typ_id>[\w\-]+)', views.goods, name='goods'),
    #url(r'^book/(?P<typ_id>[\w\-]+)', views.book, name='book'),
    #url(r'^add_book/(?P<book_id>[\w\-]+)', views.add_book, name = "add_book"),
    #url(r'^minus_book/(?P<book_id>[\w\-]+)', views.minus_book, name = "minus_book"),
    #url(r'^del_book/(?P<book_id>[\w\-]+)', views.del_book, name='del_book'),
    url(r'^del_goods/(?P<goods_id>[\w\-]+)', views.del_goods, name='del_goods'),
    url(r'^comment/(?P<goods_id>[\w\-]+)', views.comment, name='comment'),
    url(r'^my_goods/(?P<goods_id>[\w\-]+)', views.my_goods, name='my_goods'),
    url(r'^profile/(?P<seller_id>[\w\-]+)', views.profile, name='profile'),
    url(r'^check_user_name', views.check_user_name, name = "check_user_name"),
    url(r'^check_mail', views.check_mail, name = "check_mail"),
    url(r'^send_email', views.send_email_register, name = "send_email"),
    url(r'^send_forget', views.send_email_forget_pwd, name = "send_forget"),
    url(r'^user_center', views.user_center, name = "user_center"),
    url(r'^change_profile', views.change_profile, name = "change_profile"),
    url(r'^add_goods/', views.add_goods, name='add_goods'),
    #url(r'^new_book/', views.new_book, name='new_book'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), # make sure the media works well when debug is false
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('403/', views.permission_denied)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = views.permission_denied