from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static


from . import views

app_name = 'store'

urlpatterns = [
    path('', views.productList, name='productList'),
    path('available_product/<int:available_productId>', views.available_product, name='available_product'),
    path('register', views.register, name='register'),
    path('product/productlist/', views.productList, name = 'productlist'),
    path('product/<int:productId>/',views.product, name = 'product'),
    path('product/createproduct/',views.createProduct, name = 'createproduct'),
    path('product/<int:productId>/review', views.createReview, name='createReview'),
    path('product/<int:productId>/reviewlist', views.reviewList, name='reviewlist'),
    path('search/', views.search_results, name='search_results'),
    path('product/wishlist', views.wishlist, name='wishlist'),
    path('product/<int:productId>/addtowishlist', views.addWishlistItem, name='addtowishlist'),
    path('product/<int:productId>/removefromwishlist', views.removeWishlistItem, name = 'removefromwishlist'),
    path('purchase/', views.purchase_index, name='purchase_index'),
    path('purchase/<int:id>/add', views.add2ShoppingCart, name='add2ShoppingCart'),
    path('purchase/<int:id>/buy', views.buy, name='buy'),
    path('purchase/<int:id>/', views.detail, name='detail'),
    path('purchase/pay/', views.pay, name='pay'),
    path('purchase/finish/', views.finish, name='finish'),
    path('purchase/<int:id>/remove/', views.remove, name='remove'),
    path('purchase/<int:id>/removeHistory/', views.removeHistory, name='removeHistory'),
    path('purchase/finish_payment/', views.payment, name='payment'),
    path('purchase/purchase_history/', views.history, name='history')
]
