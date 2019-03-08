from django.shortcuts import render
from market.models import Category, Goods, UserProfile, Comment, InstationMessage, User, Book
from . import urls
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings
from django.db.models import Q
from functools import reduce
import operator
from PIL import Image
import json
import base64, os
import random
import smtplib
from email.mime.text import MIMEText
from collections import OrderedDict

# Create your views here.

def information(request):
    is_login = True
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        message_unread = InstationMessage.objects.filter(receiver=user_profile, active=True).order_by('-id')
        count = len(message_unread)
        if len(message_unread) > 10:
            message_unread = message_unread[0:9]
    except UserProfile.DoesNotExist:
        user_profile = []
        message_unread = []
        count = 0
    return user_profile, is_login, message_unread, count

def homepage(request):
    is_login = False
    if request.user.is_authenticated:
        is_login = True
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
            message_unread = InstationMessage.objects.filter(receiver=user_profile, active=True).order_by('-id')
            count = len(message_unread)
            if len(message_unread) > 10:
                message_unread = message_unread[0:9]
        except UserProfile.DoesNotExist:
            user_profile = []
            message_unread = []
            count = 0
    else:
        user_profile = []
        message_unread = []
        count = 0
    return render(request, 'homepage.html', {
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count})

@login_required
def goods(request, typ_id):
    user_profile, is_login, message_unread, count = information(request)
    page = 1
    if not (typ_id == '0' or typ_id == '1' or typ_id == '2'):
        return HttpResponse(status=404)
    category_list = Category.objects.all()
    try:
        goods_list = Goods.objects.filter(typ=typ_id).order_by('-id')
        paginator = Paginator(goods_list, 6)
        if request.GET.get('page'):
            page = request.GET.get('page')
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages

    goods_list_page = paginator.page(page)

    return render(request, 'goods.html', {
            'goods_list_page': goods_list_page, 
            'typ_id': int(typ_id),
            'category_list': category_list,
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required
def book(request, typ_id):
    user_profile, is_login, message_unread, count = information(request)
    page = 1
    if not (typ_id == '0' or typ_id == '1'):
        return HttpResponse(status=404)
    is_tengfei = UserProfile.objects.get(user=request.user).is_tengfei
    try:
        book_list = Book.objects.filter(typ=typ_id).order_by('id')
        paginator = Paginator(book_list, 6)
        if request.GET.get('page'):
            page = request.GET.get('page')
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages

    book_list_page = paginator.page(page)
    
    num_list = []
    id_list = []
    length = len(book_list_page)
    for i in range(length):
        num_list.append(book_list_page[i].nums)
        id_list.append(str(book_list_page[i].id))

    return render(request, 'book.html', {
            'book_list_page': book_list_page, 
            'typ_id': int(typ_id),
            'num_list': json.dumps(num_list),
            'id_list': json.dumps(id_list),
            'typ_js': json.dumps(int(typ_id)),
            'is_tengfei': is_tengfei,
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required
def search(request, typ_id):
    user_profile, is_login, message_unread, count = information(request)
    page = 1
    if not (typ_id == '0' or typ_id == '1' or typ_id == '2'):
        return HttpResponse(status=404)
    category_list = Category.objects.all()
    if request.method == 'POST':
        keywords_name = request.POST.get('keywords')
        category_id = request.POST.get('category')
        rank = request.POST.get('rank')
        request.session['keywords_name'] = keywords_name
        request.session['category_id'] = category_id
        request.session['rank'] = rank
    if request.method == 'GET':
        keywords_name = request.session['keywords_name']
        category_id = request.session['category_id']
        rank = request.session['rank']
        try:
            if request.GET.get('page'):
                page = request.GET.get('page')
        except PageNotAnInteger:
            page = 1
        except EmptyPage:
            page = 1
    keywords = keywords_name.split()
    query_list = [Q(name__icontains=words) for words in keywords]
    category = Category.objects.get(id=category_id)  
    r = '-' if rank == '0' else ''

    if len(query_list):
        goods_list = Goods.objects.filter(reduce(operator.or_, query_list), typ=typ_id, category=category).order_by(r+'id')
    else:
        goods_list = Goods.objects.filter(typ=typ_id, category=category).order_by(r+'id')

    paginator = Paginator(goods_list, 6)
    goods_list_page = paginator.page(page)

    return render(request, 'goods.html', {
            'goods_list_page': goods_list_page, 
            'typ_id': int(typ_id),
            'category_list': category_list,
            'keywords_name': keywords_name,
            'category_id': int(category_id),
            'rank_id': int(rank),
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required
def search_book(request, typ_id):
    user_profile, is_login, message_unread, count = information(request)
    page = 1
    if not (typ_id == '0' or typ_id == '1'):
        return HttpResponse(status=404)
    is_tengfei = UserProfile.objects.get(user=request.user).is_tengfei
    if request.method == 'POST':
        keywords_name = request.POST.get('keywords')
        rank = request.POST.get('rank')
        request.session['keywords_name'] = keywords_name
        request.session['rank'] = rank
    if request.method == 'GET':
        keywords_name = request.session['keywords_name']
        rank = request.session['rank']
        try:
            if request.GET.get('page'):
                page = request.GET.get('page')
        except PageNotAnInteger:
            page = 1
        except EmptyPage:
            page = 1
    keywords = keywords_name.split()
    query_list = [Q(name__icontains=words) for words in keywords]
    r = '-' if rank == '1' else ''

    if len(query_list):
        book_list = Book.objects.filter(reduce(operator.or_, query_list), typ=typ_id).order_by(r+'id')
    else:
        book_list = Book.objects.filter(typ=typ_id).order_by(r+'id')

    paginator = Paginator(book_list, 6)
    book_list_page = paginator.page(page)

    num_list = []
    id_list = []
    length = len(book_list_page)
    for i in range(length):
        num_list.append(book_list_page[i].nums)
        id_list.append(str(book_list_page[i].id))
    
    return render(request, 'book.html', {
            'book_list_page': book_list_page, 
            'typ_id': int(typ_id),
            'keywords_name': keywords_name,
            'rank_id': int(rank),
            'num_list': json.dumps(num_list),
            'id_list': json.dumps(id_list),
            'typ_js': json.dumps(int(typ_id)),
            'is_tengfei': is_tengfei,
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required # my
def comment(request, goods_id):
    user_profile, is_login, message_unread, count = information(request)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    try:
        goods = Goods.objects.get(id=goods_id)
    except:
        return HttpResponse(status=404)
    message_delete = InstationMessage.objects.filter(receiver=user_profile, goods=goods)
    if message_delete:
        for mess in message_delete:
            mess.active = False
            mess.save()
    comment_list = Comment.objects.filter(goods=goods).order_by('id')
    comment_dic = OrderedDict()
    for i in range(len(comment_list)):
        comment_dic[comment_list[i]] = i % 2
    return render(request, 'comment-1.html', {'comment_dic': comment_dic, 'goods': goods,
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required # my
def my_goods(request, goods_id):
    user_profile, is_login, message_unread, count = information(request)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    try:
        goods = Goods.objects.get(id=goods_id, seller=user_profile)
    except:
        return HttpResponse(status=404)
    message_delete = InstationMessage.objects.filter(receiver=user_profile, goods=goods)
    if message_delete:
        for mess in message_delete:
            mess.active = False
            mess.save()
    comment_list = Comment.objects.filter(goods=goods).order_by('id')
    comment_dic = OrderedDict()
    for i in range(len(comment_list)):
        comment_dic[comment_list[i]] = i % 2
    return render(request, 'my_goods.html', {'comment_dic': comment_dic, 'goods': goods,
            'user_profile': user_profile, 
            'is_login': is_login,
            'message_unread': message_unread,
            'count': count
            })

@login_required # my
def profile(request, seller_id):
    try:
        seller = UserProfile.objects.get(pk=seller_id)
    except:
        return HttpResponse(status=404)
    goods_list = Goods.objects.filter(seller=seller).order_by('-id')
    is_self = False
    if request.user == seller.user:
        is_self = True
    return render(request, 'profile.html', {'seller': seller, 'goods_list': goods_list, 'is_self': is_self})

@login_required # my
def user_center(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        goods_list = Goods.objects.filter(seller=user_profile).order_by('-id')
    return render(request, 'user_center.html', {'user': user_profile, 'goods_list': goods_list})

@login_required
def add_comment(request, goods_id):
    if request.method == 'POST':
        comment_add = request.POST.get('comment')
        if comment_add:
            comment_new = Comment(content=comment_add)
            try:
                goods = Goods.objects.get(pk=goods_id)
            except:
                return HttpResponse(status=404)
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            comment_new.user = user_profile
            comment_new.goods = goods
            comment_new.save()
            message = InstationMessage()
            message.goods = goods
            message.sender = user_profile
            message.receiver = goods.seller
            message.content = str(user_profile.family_name) + str(user_profile.given_name) + '给你留言了'
            message.save()
            return HttpResponseRedirect('/comment/'+str(goods_id))
    return comment(request, goods_id)

@login_required
def add_message(request, user_id, goods_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            message_new = InstationMessage(content=message)
            comment_new = Comment()
            try:
                goods = Goods.objects.get(pk=goods_id)
            except:
                return HttpResponse(status=404)
            user = request.user
            user_sender = UserProfile.objects.get(user=user)
            try:
                user_receiver = UserProfile.objects.get(id=user_id)
            except:
                return HttpResponse(status=404)

            comment_new.user = user_sender
            comment_new.goods = goods
            comment_new.content = '@'+str(user_receiver.family_name)+str(user_receiver.given_name)+':'+message
            comment_new.save()

            message_new.sender = user_sender
            message_new.receiver = user_receiver
            message_new.content = str(user_sender.family_name) + str(user_sender.given_name) + '回复了你'
            message_new.goods = goods
            message_new.save()
            return HttpResponseRedirect('/comment/'+str(goods_id))
    return comment(request, goods_id)
'''
@login_required
def add_goods(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    category_list = Category.objects.all()
    if request.method == 'POST':
        user_profile.recent_nums += 1
        user_profile.nums += 1
        if user_profile.recent_nums > 6:
            return render(request, 'add_fail.html', {'user': user_profile})
        name = request.POST.get('name')
        trade_location = request.POST.get('trade_location')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        typ_id = int(request.POST.get('typ_id'))
        if name and trade_location and price and description:
            new_goods = Goods(name=name, trade_location=trade_location, price=price, description=description, typ=typ_id)
            new_goods.category = Category.objects.get(name=category)
            new_goods.seller = user_profile
            if request.POST.get('base64'):
                path = str(user.username) + '-' +str(user_profile.nums) + '.jpg'
                image_data = base64.b64decode(request.POST['base64'])
                fname = os.path.join(settings.MEDIA_ROOT, path)
                with open(fname, 'wb') as f:
                    f.write(image_data)
                f.close()
                new_goods.picture = path
            new_goods.save()
            user_profile.save()
            return HttpResponseRedirect('/goods'+'/'+str(typ_id))

    return render(request, 'add_goods-1.html',{'user': user_profile, 'category_list': category_list})
'''
@login_required
def add_goods(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    category_list = Category.objects.all()
    if request.method == 'POST':
        user_profile.recent_nums += 1
        user_profile.nums += 1
        if user_profile.recent_nums > 6:
            return render(request, 'add_fail.html', {'user': user_profile})
        name = request.POST.get('name')
        trade_location = request.POST.get('trade_location')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        typ_id = int(request.POST.get('typ_id'))
        if name and trade_location and price and description:
            new_goods = Goods(name=name, trade_location=trade_location, price=price, description=description, typ=typ_id)
            new_goods.category = Category.objects.get(name=category)
            new_goods.seller = user_profile
            if 'picture' in request.FILES:
                name = str(request.FILES['picture'])
                ext = os.path.splitext(name)[1]
                print(ext)
                path = str(user.username) + '-' +str(user_profile.nums) + ext
                t_x = int(request.POST.get('dataX'))
                t_y = int(request.POST.get('dataY'))
                t_width = int(request.POST.get('dataWidth'))
                t_height = int(request.POST.get('dataHeight'))
                t_rotate = int(request.POST.get('dataRotate'))
                fname = os.path.join(settings.MEDIA_ROOT, path)
                img = Image.open(request.FILES['picture'])
                crop_im = img.rotate(-t_rotate, expand=True).crop((t_x, t_y, t_x + t_width, t_y + t_height)).resize((600, 600), Image.ANTIALIAS)
                crop_im.save(fname, quality=100, dpi=(600, 600))
                new_goods.picture = path
            new_goods.save()
            user_profile.save()
            return HttpResponseRedirect('/goods'+'/'+str(typ_id))

    return render(request, 'add_goods-1.html',{'user': user_profile, 'category_list': category_list})


@login_required
def new_book(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        if user_profile.is_tengfei:
            name = request.POST.get('name')
            nums = request.POST.get('nums')
            description = request.POST.get('description')
            typ_id = int(request.POST.get('typ_id'))
            if name and nums and description:
                new_book = Book(name=name, nums=nums, description=description, typ=typ_id)
                if request.POST.get('base64'):
                    path = 'book' + str(name) + '@' + str(new_book.id) + '.png'
                    image_data = base64.b64decode(request.POST['base64'])
                    fname = os.path.join(settings.MEDIA_ROOT, path)
                    with open(fname, 'wb') as f:
                        f.write(image_data)
                    f.close()
                    new_book.picture = fname
                new_book.save()
                return HttpResponseRedirect('/book'+'/'+str(typ_id))
        return book(request, typ_id)

    return render(request, 'new_book.html')
'''
@login_required
def change_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        given_name = request.POST.get('given_name')
        description = request.POST.get('description')
        phone = request.POST.get('phone')
        if family_name and given_name and description and phone:
            user_profile.family_name = family_name
            user_profile.given_name = given_name
            user_profile.description = description
            user_profile.phone = phone
            if request.POST.get('base64'):
                path = str(user.username) + '.jpg'
                image_data = base64.b64decode(request.POST['base64'])
                fname = os.path.join(settings.MEDIA_ROOT, path)
                with open(fname, 'wb') as f:
                    f.write(image_data)
                f.close()
                user_profile.avatar = path
            user_profile.save()
            return HttpResponseRedirect('/user_center')
    return render(request, 'change_profile.html', {'user_profile': user_profile})
'''
@login_required
def change_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        given_name = request.POST.get('given_name')
        description = request.POST.get('description')
        phone = request.POST.get('phone')
        if family_name and given_name and description and phone:
            user_profile.family_name = family_name
            user_profile.given_name = given_name
            user_profile.description = description
            user_profile.phone = phone
            if 'picture' in request.FILES:
                name = str(request.FILES['picture'])
                ext = os.path.splitext(name)[1]
                print(ext)
                path = str(user.username) + str(get_verify_code(4)) + ext
                t_x = int(request.POST.get('dataX'))
                t_y = int(request.POST.get('dataY'))
                t_width = int(request.POST.get('dataWidth'))
                t_height = int(request.POST.get('dataHeight'))
                t_rotate = int(request.POST.get('dataRotate'))
                fname = os.path.join(settings.MEDIA_ROOT, path)
                img = Image.open(request.FILES['picture'])
                print(t_x)
                print(t_y)
                print(t_width)
                print(t_height)
                print(t_rotate)
                crop_im = img.rotate(-t_rotate, expand=True).crop((t_x, t_y, t_x + t_width, t_y + t_height)).resize((300, 300), Image.ANTIALIAS)
                crop_im.save(fname, quality=100, dpi=(300, 300))
                if user_profile.avatar:
                    old_f = os.path.join(settings.MEDIA_ROOT, str(user_profile.avatar))
                    os.remove(old_f)
                user_profile.avatar = path
            user_profile.save()
            return HttpResponseRedirect('/user_center')
    return render(request, 'change_profile-1.html', {'user_profile': user_profile})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password and email:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = True
            user.save()
            user_profile = UserProfile(mail=email)
            user_profile.user = user
            user_profile.save()
            return render(request, 'register_success.html')
    return render(request, 'register.html')

@csrf_exempt
def check_user_name(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return HttpResponse(json.dumps({'msg': True}))
        else:
            return HttpResponse(json.dumps({'msg': False}))
    else:
        return HttpResponse(json.dumps({'msg': True}))

@csrf_exempt
def check_mail(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        if UserProfile.objects.filter(mail=mail).exists():
            return HttpResponse(json.dumps({'msg': True}))
        else:
            return HttpResponse(json.dumps({'msg': False}))
    else:
        return HttpResponse(json.dumps({'msg': True}))

@csrf_exempt
def add_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        adder = int(request.POST.get('adder'))
        if adder == 1:
            book.nums += 1
            book.save()
    return HttpResponse(json.dumps({'nums': book.nums}))

@csrf_exempt
def minus_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        minus = int(request.POST.get('minus'))
        if minus == 1:
            book.nums -= 1
            book.save()
    return HttpResponse(json.dumps({'nums': book.nums}))

@csrf_exempt
def del_book(request, book_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    ok = 0
    if user_profile.is_tengfei:
        if request.method == 'POST':
            deler = int(request.POST.get('deler'))
            if deler == 1:
                Book.objects.get(id=book_id).delete()
                ok = 1
    return HttpResponse(json.dumps({'ok': ok}))

@csrf_exempt
def del_goods(request, goods_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    goods = Goods.objects.get(id=goods_id)
    if user_profile == goods.seller:
        if request.method == 'POST':
            deler = int(request.POST.get('deler'))
            if deler == 1:
                goods.picture.delete(save=True)
                goods.delete()
                user_profile.recent_nums -= 1
                user_profile.save()
                return HttpResponseRedirect('/user_center')
    return my_goods(request, goods_id)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('inputUsername')
        password = request.POST.get('inputPassword')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login_fail.html')
        else:
            return render(request, 'login_fail.html')

    else:
        return render(request, 'login.html',{})

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        if password and email:
            try:
                user = User.objects.get(email=email)
            except:
                return HttpResponse(status=404)
            user.set_password(password)
            user.save()
            return render(request, 'forget_success.html')
    return render(request, 'forget_password.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def get_verify_code(num):
    base = 'QWER1TYU2IOP3ASD4FG5HJKL6ZXCV7BNMq8wert9yuiopa0sdfghjklzxcvbnm'
    length = len(base)
    verify = ''
    for i in range(num):
        verify += base[random.randint(0, length-1)]
    return verify


@csrf_exempt
def send_email_register(request):
    if request.method == 'POST':
        msg_from = 'TWTSGroup14@126.com' # TWTSGroup201820
        msg_to = request.POST.get('email')
        password = 'group201820' #授权码
        #verify = get_verify_code()
        verify = request.POST.get('varify_code')
        mail_host = 'smtp.126.com'
        subject = '感谢注册“贰拾”二手交易平台（请勿回复此邮件）'
        content = '您好，欢迎您注册“贰拾”二手交易平台，您的验证码是：' + verify + '\n' + '如果不是您本人操作，请忽略此邮件' 
    
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host,25)
            smtpObj.login(msg_from, password)
            smtpObj.sendmail(msg_from, msg_to, msg.as_string())
            print('send email success')
            print('register')
        except smtplib.SMTPException as e:
            print('send email fail',e)

        return HttpResponse(json.dumps({"verify": verify}))
    return HttpResponse(status=404)

@csrf_exempt
def send_email_forget_pwd(request):
    if request.method == 'POST':
        mail = request.POST.get('email')
        username=UserProfile.objects.get(mail=mail).user.username
        msg_from = 'TWTSGroup14@126.com' # TWTSGroup201820
        msg_to = mail
        password = 'group201820' #授权码
        #verify = get_verify_code()
        verify = request.POST.get('varify_code')
        mail_host = 'smtp.126.com'
        subject = '重置“贰拾”二手交易平台密码（请勿回复此邮件）'
        content = str(username) + '，您好，您重置密码的验证码是：' + verify + '\n' + '如果不是您本人操作，请忽略此邮件' 
    
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host,25)
            smtpObj.login(msg_from, password)
            smtpObj.sendmail(msg_from, msg_to, msg.as_string())
            print('send email success')
            print('forget')
        except smtplib.SMTPException as e:
            print('send email fail',e)

        return HttpResponse(json.dumps({"verify": verify}))
    return HttpResponse(status=404)

def permission_denied(request):
    return render(request, '403.html')