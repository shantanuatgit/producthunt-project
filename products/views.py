from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ImageForm

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings


@login_required(login_url="/accounts/signup")
def home(request):
    products_list=Product.objects.order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,'products/home.html',{'products':products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method== 'POST':
        if request.POST['title'] and request.POST['body'] and request.FILES['image']:
            product=Product()
            product.title=request.POST['title']
            product.body=request.POST['body']
            product.image=request.FILES['image']
            product.pub_date=timezone.datetime.now()
            product.hunter=request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request,'products/create.html',{'error': 'All fields are required'})
    else:
        return render(request,'products/create.html')


def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'product':product})

def delete(request, product_id):
    article=Product.objects.filter(id=product_id)

    article.delete()
    return myarticles(request)

def edit(request, product_id, article_id):
    if request.method == "POST":
        article=Product.objects.filter(id=product_id).update(
            title=request.POST['title'],
            body=request.POST['body'],
            pub_date=timezone.datetime.now())
        old_image = Product.objects.get(id=product_id)
        form = ImageForm(request.POST, request.FILES, instance=old_image)
        if form.is_valid():
            image_path = old_image.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
            form.save()
        return detail(request, product_id)
    else:
        articles=Product.objects.filter(id=product_id)
        return render(request, 'products/edit.html', {'articles':articles})


def myarticles(request):
    articles_list=Product.objects.filter(hunter=request.user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(articles_list, 10)
    try:
        articles=paginator.page(page)
    except PageNotAnInteger:
        articles=paginator.page(1)

    except EmptyPage:
        articles=paginator.page(paginator.num_pages)
    return render(request, 'products/myarticles.html', {'articles':articles})


@login_required(login_url="/accounts/signup")
def upvote(request,product_id):
    if request.method=="POST":
        product=get_object_or_404(Product,pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
