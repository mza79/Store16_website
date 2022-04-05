from django.contrib import admin
from .models import Product, Review, Wishlist, Available_product,ShoppingCart,History
# Register your models here.


admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(History)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Available_product)

