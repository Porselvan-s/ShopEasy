from django.shortcuts import render,redirect
from shop. form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
    
def favview_page(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
  
def remove_cart(request,cid):
    cartitem = Cart.objects.get(id=cid)
    product_status = Product.objects.get(id=cartitem.product.id)
    product_status.save()
    cartitem.delete()
    print("here : ",product_status.quantity)
    return redirect("/cart")

def remove_fav(request,cid):
    item = Favourite.objects.get(id=cid)
    item.delete()
    return redirect("/favviewpage")

def fav_page(request):
    if request.headers.get("x-requested-with") == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user = request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status = 200)
                else:
                    Favourite.objects.create(user = request.user,product_id=product_id)
            # print(request.user.id)
                    return JsonResponse({'status':'Product added to Favourite'}, status = 200)            
        else:
            return JsonResponse({'status':'Login To Add Favourite'}, status = 200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status = 200)


def add_to_cart(request):
    if request.headers.get("x-requested-with") == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            product_status.quantity-=product_qty
            product_status.save()
            if product_status:
                if Cart.objects.filter(user = request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status = 200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user = request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart '}, status = 200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status = 200)
        else:
            return JsonResponse({'status':'Login To Add Cart'}, status = 200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status = 200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request,"shop/login.html")
    
def login_page_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=name,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"Ivalid Username or Password")
                return redirect("/login_user")
        return render(request,"shop/login_user.html")


def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login_user')
  return render(request,"shop/register.html",{'form':form})
 

def collection(request):
    category = Category.objects.filter(status=0)
    return render(request,"shop/collection.html",{"category":category})

def collectionview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such Category Found")
        return redirect('collection')


def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No Such Produtct Found")
            return redirect('collection')
    else:
        messages.error(request,"No Such Catagory Found")
        return redirect('collections')
