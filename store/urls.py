from django.urls import path
from . import views
from .views import MapView
from .views import order_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('update_password', views.update_password, name='update_password'),
    path('update_user', views.update_user, name='update_user'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('map/', MapView.as_view(), name='map'),
    path('orders/', order_list, name='order_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)