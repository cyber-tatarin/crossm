from django.urls import path, include
from .views import CreateOfferView, DeleteOfferView, UpdateOfferView, OfferImageDeleteView, MyOffersPageView

app_name = 'offers'
urlpatterns = [
    path('create/<int:pk>', CreateOfferView.as_view(), name='create-offer'),
    path('delete/', DeleteOfferView.as_view(), name='delete-offer'),
    path('update/<int:pk>', UpdateOfferView.as_view(), name='update-offer'),
    path('delete/image/', OfferImageDeleteView.as_view(), name='delete-image'),
    path('myoffers', MyOffersPageView.as_view(), name='my-offers'),

]