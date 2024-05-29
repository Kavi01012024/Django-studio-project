"""
URL configuration for EM_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Studio_app import views

urlpatterns = [
    path('home/', views.home,name='home'),
    path('about/', views.About_us,name='about'),
    path('bookings/', views.bookings,name='bookings'),
    path('login/', views.signin,name='login'),
    path('logup/', views.logup,name='logup'),
    path('verify_mail/',views.send_maill,name= 'verify_mail'),
    path('logout/',views.logout_view,name= 'logout'),
    path('pr_list/',views.pr_list,name='pr_list'),
    path('pr_desc/<int:p_id>/',views.pr_desc,name='pr_desc'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'), 
    path('go_to_cart/',views.go_cart_page,name="go_to_cart"),
    path('rem_from_cart/',views.remove_cart_item,name='rem_cart_item'),
    path('address/',views.address,name='address'),
    path('get_total_quantity/',views.send_quantity_cart),
    path('place_order/',views.place_order,name= 'place_order'),
    path('payment_success_fail/',views.payment_success_fail,name='payment_success_fail'),
    path('profile/',views.profile_page,name = 'profile'),
    path('create_order/',views.create_order,name = 'create_order'),
    path('razor_order/',views.razor_order,name = 'razor_order')

]
