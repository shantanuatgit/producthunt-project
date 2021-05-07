
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('accounts/',include('accounts.urls')),
    path('products/',include('products.urls')),
    path('myarticles/', views.myarticles, name='myarticles'),
    path('<int:product_id>',views.delete,name='delete'),
    path('<int:product_id> <int:article_id>',views.edit,name='edit'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
