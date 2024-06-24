from django.urls import path
from .views import OTPViewSet, AddCardAPIView, TransferViewSet, HumoCardInfoViewSet, UzCardOTPViewSet, UzCardAddAPIView, \
    UzCardInfoViewSet

urlpatterns = [
    path('add/card/', AddCardAPIView.as_view()),
    path('humo/otp/send/', OTPViewSet. as_view({'post': 'send'})),
    path('humo/otp/verify/', OTPViewSet.as_view({'post': 'verify'})),
    path('humo/check/', OTPViewSet.as_view({'get': 'check_balance'})),

    path('humo/info/', HumoCardInfoViewSet.as_view({'get': 'info'})),
    path('humo/transfer/up/', TransferViewSet.as_view({'patch': 'up'})),
    path('humo/transfer/down/', TransferViewSet.as_view({'patch': 'down'})),
    #uzcard
    path('add/uzcard/', UzCardAddAPIView.as_view()),
    path('uzcard/otp/send/', UzCardOTPViewSet.as_view({'post': 'send'})),
    path('uzcard/otp/verify/', UzCardOTPViewSet.as_view({'post': 'verify'})),
    path('uzcard/check/', UzCardOTPViewSet.as_view({'get': 'check_balance'})),

    path('uzcard/info/', UzCardInfoViewSet.as_view({'get': 'info'})),
    path('uzcard/transfer/up/', UzCardInfoViewSet.as_view({'get': 'info'})),
    path('uzcard/info/down/', UzCardInfoViewSet.as_view({'get': 'info'})),
    
]