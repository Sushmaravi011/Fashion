from django.http import  JsonResponse
from django.shortcuts import redirect, render
from DrapeDream.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"DrapeDream/home.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"DrapeDream/wishlist.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
  
def cart_view(request):
  if request.user.is_authenticated:
    cart_item=cart.objects.filter(user=request.user)
    return render(request,"DrapeDream/cart.html",{"cart":cart_item})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
def wishlist(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                product_id = data['pid']
                product_status = Product.objects.get(id=product_id)

                if product_status:
                    if Favourite.objects.filter(user=request.user.id, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                    else:
                        Favourite.objects.create(user=request.user, product_id=product_id)
                        return JsonResponse({'status': 'Product Added to Favourite'}, status=200)
                else:
                    return JsonResponse({'status': 'Product not found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON'}, status=400)
        else:
            fav = Favourite.objects.filter(user=request.user)
            return render(request, "DrapeDream/wishlist.html", {"fav": fav})
    else:
        return redirect("/login")

 
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = data.get('product_qty')
                product_id = data.get('pid')

                if not product_qty or not product_id:
                    return JsonResponse({'status': 'Missing required parameters'}, status=400)

                product = Product.objects.filter(id=product_id).first()

                if product:
                    if cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product already in cart'}, status=200)

                    if product.quantity >= product_qty:
                        cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Not enough stock available'}, status=200)

                else:
                    return JsonResponse({'status': 'Product not found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON'}, status=400)
        else:
            return JsonResponse({'status': 'Please login to add items to the cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=403)

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"DrapeDream/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"DrapeDream/register.html",{'form':form})
 
 
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"DrapeDream/collection.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"DrapeDream/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collection')
 
 
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"DrapeDream/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
