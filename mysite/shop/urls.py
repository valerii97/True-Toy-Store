from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='product_details'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('clear-all-fm-cart/', views.clear_cart, name='clear_all_fm_cart'),
    path('open-cart/', views.open_cart, name='open_cart'),
    path('delete-item/', views.delete_item_fm_cart, name='delete_item'),
    path('create-order/', views.create_order, name='create_order'),
    path('thanks/<int:order_num>/', views.thanks, name='thanks'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('product-search/', views.product_search, name='product_search'),
    path('product-search-autocomplete/', views.product_search_autocomplete,
         name='product_search_autocomplete'),
    path('substruct-fm-item/', views.substruct_fm_cart, name='substruct_fm_item'),
    path('choose-delivery/', views.choose_delivery, name='choose_delivery'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
