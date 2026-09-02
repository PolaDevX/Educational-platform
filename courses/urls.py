from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    path('about.html', views.about_view, name='about'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
    
    path('category/', views.category, name='category_all'),
    path('category/<cid>/', views.category, name='category_courses'),
    
    path('course/<int:pid>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/learn/', views.course_learn_view, name='course_learn'),
    path('buy-now/<int:pid>/', views.buy_now, name='buy_now'),
    path('lesson/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),
    
    path('cart/add/<int:pid>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pid>/', views.cart_remove, name='cart_remove'),
]