from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home),
    path('cat/<val>',views.cat,name="cat"),
    path('productdetails/<pk>',views.productdetails,name="productdetails"),
    path('categorytitle/<val>',views.categorytitle,name="categorytitle"),
    path('about',views.about,name="about"),
    path('contect',views.contect,name="contect"),
    path('profile',views.profile.as_view(),name="profile"),
    path('address',views.address,name="address"),
    path('updateAddress/<pk>',views.updateAddress.as_view(),name="updateAddress"),
    
    path('add-to-cart',views.add_to_cart,name="add-to-cart"),
    path('cart',views.show_cart,name="showcart"),
    path('checkout',views.checkout,name="checkout"),
    path('paymentdone',views.payment_done,name="paymentdone"),
    path('orders',views.orders,name="orders"),
    
    path('pluscart',views.plus_cart ),
    path('minuscart',views.minus_cart ),
    path('removecart',views.remove_cart ),
    path('search',views.search_products),

    # login athentication
    path('ragistration',views.ragistration,name="ragistration"),
    path('user_login',views.user_login,name="user_login"),
    path('logout',views.user_logout),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)