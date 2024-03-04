
from django.urls import path
from .views import (UserCreateView,LoginView,CategoryCreateView,CategoryUpdateView,CategoryListView,CategoryDeleteView,ProductCreateView,ProductUpdateView,ProductListView,ProductDetailView,
                    ProductDeleteView)


urlpatterns = [
path('register/',UserCreateView.as_view(),name='register'),
path('login/',LoginView.as_view(),name='login'),

path('category/create/',CategoryCreateView.as_view(),name='category-create'),
path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name='category-update'),
path('category/list/',CategoryListView.as_view(),name='category-list'),
path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name='category-delete'),

path('product/create/<int:category_id>/',ProductCreateView.as_view(),name='product-create'),
path('product/update/<int:pk>/',ProductUpdateView.as_view(),name='product-update'),
path('product/list/<int:category_id>/',ProductListView.as_view(),name='product-list'),
path('product/<int:pk>/',ProductDetailView.as_view(),name='product-detail'),
path('product/<int:pk>/delete/',ProductDeleteView.as_view(),name='product-delete'),

]
