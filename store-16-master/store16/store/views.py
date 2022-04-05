from django.http import HttpResponse,Http404, HttpResponseRedirect
from .models import Product, ShoppingCart, Available_product, Review, History, Wishlist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q


def index(response):
	return render(response, "store/index.html")

# function to add available products to shopping cart
# can add a <add to shoppingcart> button to product view page.
# can be called by redirecting to url store/purchase/<book_id>/add
def add2ShoppingCart(request, id):
	if len(Available_product.objects.filter(id=id)) < 1:
		return HttpResponseRedirect("/store/purchase")

	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		Cart = ShoppingCart()

		Cart.books_id = id
		Cart.user = user
		Cart.save()
	else:
		# guest users can also use shopping cart
		Cart = ShoppingCart()
		Cart.books_id = id
		Cart.user = None
		Cart.save()
	return HttpResponseRedirect("/store/purchase")

def buy(request, id):
	if len(Available_product.objects.filter(id=id)) < 1:
		return HttpResponseRedirect("/store/purchase")

	available_p = Available_product.objects.get(id=id)
	total = available_p.price
	books = [available_p.product]
	items = 1
	context = {
		'books': books,
		'items': items,
		'total': total,
	}
		
	if request.user.is_authenticated:
		time = timezone.now()
		user = User.objects.get(id=request.user.id)
		history = History()
		history.books_id = id
		history.user = user
		history.purchase_date = time
		history.save()

	return render(request, 'store/purchase/pay1.html', context)


def finish(request):
	render(request, 'store/purchase/finish.html')

def remove(request, id):
	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		Cart = ShoppingCart.objects.filter(user = user,books_id=id)
		if len(Cart) > 1:
			obj = Cart[0]
			obj.delete()
		elif len(Cart) == 1:
			Cart.delete()
	else:
		Cart = ShoppingCart.objects.filter(user = None,books_id=id)
		if len(Cart) > 1:
			obj = Cart[0]
			obj.delete()
		elif len(Cart) == 1:
			Cart.delete()
	return HttpResponseRedirect("/store/purchase")

def purchase_index(request):
	shpping_cart = ShoppingCart.objects.filter(user = request.user.id)
	available_p = [Available_product.objects.get(id=i.books_id) for i in shpping_cart]
	total = sum([i.price for i in available_p ])
	books = [[i.product, i.price] for i in available_p ]
	context = {
		'books': books,
		'total': total,
	}
	return render(request, 'store/purchase/index.html', context)

def pay(request):
	shpping_cart = ShoppingCart.objects.filter(user = request.user.id)
	available_p = [Available_product.objects.get(id=i.books_id) for i in shpping_cart]
	total = sum([i.price for i in available_p ])
	books = [i.product for i in available_p ]
	items = len(books)
	context = {
		'books': books,
		'items': items,
		'total': total,
	}
	return render(request, 'store/purchase/pay.html', context)

def detail(request, id):

	return HttpResponseRedirect("/store/available_product/" + str(id) )

def payment(request):
	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		shpping_cart = ShoppingCart.objects.filter(user = request.user.id)
		available_p = [Available_product.objects.get(id=i.books_id) for i in shpping_cart]
		total = sum([i.price for i in available_p ])
		books = [i.product for i in available_p ]
		items = len(books)
		time = timezone.now()
		if request.user.is_authenticated:
			user = User.objects.get(id=request.user.id)
			for book in books:
				history = History()
				history.books_id = book.id
				history.user = user
				history.purchase_date = time
				history.save()
		ShoppingCart.objects.filter(user = user).delete()
	else:
		ShoppingCart.objects.filter(user = None).delete()
	return render(request, 'store/purchase/finish.html')

@login_required(login_url='/login')
def history(request):
	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		history = History.objects.filter(user = user).order_by("purchase_date")
		availableProduct_date = [ [Available_product.objects.get(id=i.books_id),i.purchase_date] for i in history]
		total = sum([i[0].price for i in availableProduct_date ])
		books_date = [ [i[0].product,i[1], i[0].price]  for i in availableProduct_date]
		context = {
			'books_date': books_date,
			'total': total,
		}
		return render(request, 'store/purchase/history.html', context)

@login_required(login_url='/login')
def removeHistory(request,id):
	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		hist = History.objects.filter(user = user,books_id=id)
		if len(hist) > 1:
			obj = hist[0]
			obj.delete()
		elif len(hist) == 1:
			hist.delete()
		return HttpResponseRedirect("/store/purchase/purchase_history")


def available_product(request, available_productId):
    try:
        avproduct = Available_product.objects.get(pk=available_productId)
    except Available_product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, 'store/available_product/available_product.html', {'available_product': avproduct})

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
                form.save()
        return redirect('../store/product/productlist')
    else:
        form = RegisterForm()
    
    return render(response, "store/register.html", {"form":form})
    
def productList(request):
    productList = Product.objects.all()
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except Wishlist.DoesNotExist:
            wishlist = Product.objects.order_by('-id')[:10]
    else:
        wishlist = Product.objects.order_by('-id')[:10]
    paginator = Paginator(productList, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = loader.get_template('store/product/productlist.html')
    context = {
        'wishlist':wishlist,
        'productList': productList,
        'page_obj': page_obj,
    }
    return HttpResponse(template.render(context, request,))

def product(request, productId):
    try:
        product = Product.objects.get(pk=productId)
        avproduct = Available_product.objects.filter(product=product)
        context = {
            'product': product,
            'available_product': avproduct
        }
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, 'store/product/product.html', context)

@login_required(login_url='/login')
def wishlist(request):
    try:
        wishlist = Wishlist.objects.filter(user = request.user)
    except Wishlist.DoesNotExist:
        raise Http404("Wishlist does not exist")
    return render(request, 'store/wishlist/wishlist.html', {'wishlist': wishlist})

@login_required(login_url='/login')
def addWishlistItem(request, productId):
    if request.POST.get('addtowishlist'):
        if request.user.is_authenticated:
            try:
                Wishlist.objects.get(user = request.user, products = productId) 
            except Wishlist.DoesNotExist:
                wishlist = Wishlist()
                wishlist.products = Product.objects.get(pk = productId)
                wishlist.user = request.user
                wishlist.save()
    return HttpResponseRedirect("/store/product/productlist/")

@login_required(login_url='/login')
def removeWishlistItem (request,  productId):
    if request.POST.get('removefromwishlist'):
        if request.user.is_authenticated:
            product = Product.objects.get(pk = productId)
            wishlist = Wishlist.objects.get(user = request.user, products = product)
            wishlist.delete()
        else:
            pass
    return HttpResponseRedirect('/store/product/wishlist')

@permission_required('store.add_product', login_url='/login')
def createProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/store/product/createproduct/')
    else:
        form = ProductForm()
        return render(request, 'store/product/createproduct.html', {'form' : form})

@login_required(login_url='/login')
def createReview(request, productId):
    product = get_object_or_404(Product, pk=productId)
    if request.method == 'POST':
        numReviews = len(Review.objects.filter(product=product))
        review = Review()
        review.username = request.POST.get('username')
        review.rating = request.POST.get('rating')
        review.feedback = request.POST.get('feedback')
        review.product = product
        review.save()

        newRating = 0
        if product.rating is not None:
            newRating = product.rating * numReviews
        newRating += int(request.POST.get('rating'))
        newRating /= (numReviews + 1)
        product.rating = newRating
        product.save()

        return render(request, 'store/product/product.html', {'product': product})
    else:
        return render(request, 'store/review/review.html', {'product': product})

def reviewList(request, productId):
    product = get_object_or_404(Product, pk=productId)
    reviewlist = Review.objects.filter(product=product)
    return render(request, 'store/review/reviewlist.html', {'product': product, 'reviewlist': reviewlist})

def search_results(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(product__title__icontains=query) | Q(product__author__icontains=query)
            results= Available_product.objects.filter(lookups).distinct()
            context={'results': results,
                     'submitbutton': submitbutton}
            return render(request, 'search_results.html', context)
        else:
            return render(request, 'search_results.html')
    else:
        return render(request, 'search_results.html')
