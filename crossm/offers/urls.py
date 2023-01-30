from django.urls import path, include
from .views import CreateOfferView, DeleteOfferView, UpdateOfferView, delete_image_fun, MyOffersPageView

app_name = 'offers'
urlpatterns = [
    path('create/<int:pk>', CreateOfferView.as_view(), name='create-offer'),
    path('delete/', DeleteOfferView.as_view(), name='delete-offer'),
    path('update/<int:pk>', UpdateOfferView.as_view(), name='update-offer'),
    path('delete/<int:id>', delete_image_fun, name='delete-image'),
    path('myoffers', MyOffersPageView.as_view(), name='my-offers'),

]