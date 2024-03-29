from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import RegisterView, LoginView, SetProfileInfo, ProfileView, \
    ProfileUpdateView, ProfilePhotoUpload, DeletePhotoView, WhatisCMView, CheckProfilePhoto, GetAiHelp, \
    CrossMHelp, TechnicalHelp, UserEnrollment, CheckRefCodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/<str:ref_code>', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('setprofileinfo/', SetProfileInfo.as_view(), name='set-profile-info'),
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>', ProfileView.as_view(), name='view-profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update-profile'),
    path('profile/photoupload/', ProfilePhotoUpload.as_view(), name='upload-photo'),
    path('profile/photodelete/', DeletePhotoView.as_view(), name='delete-photo'),
    path('whatis', WhatisCMView.as_view(), name='what-is-cm'),
    path('checkphoto', CheckProfilePhoto.as_view(), name='check-photo'),
    path('getaihelp', GetAiHelp.as_view(), name='get-ai-help'),
    path('techhelp', TechnicalHelp.as_view(), name='tech-help'),
    path('crossmhelp', CrossMHelp.as_view(), name='crossm-help'),
    path('enrollment', UserEnrollment.as_view(), name='user-enrollment'),
    path('checkrefcode', CheckRefCodeView.as_view(), name='check-ref-code'),
]
