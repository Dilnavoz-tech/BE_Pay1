from datetime import timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ViewSet
from .models import HumoCard, OTP, UzCard
from rest_framework.response import Response
from rest_framework import status
from .serializers import HumoCardSerializer, CardSerializer, UzCardSerializer, CarduzSerializer
from .utils import send_otp_telegram
from django.utils import timezone


class OTPViewSet(ViewSet):
    def send(self, request, *args, **kwargs):
        humocard = HumoCard.objects.filter(pan=request.data['pan'], expire_month=request.data['expire_month'],
                                           expire_year=request.data['expire_year']).first()
        if humocard is None:
            return Response(data={'error': "card with this pan not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.create(phone_number=humocard.phone_number)
        otp.save()

        send_otp_telegram(otp)

        return Response(data={'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)


    def verify(self, request, *args, **kwargs):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        otp = OTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        if otp is None:
            return Response(data={'error': 'otp code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        if (timezone.now() - otp.created_at) > timedelta(minutes=3):
            return Response(data={'error': 'otp code is expired'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'otp code verified'}, status=status.HTTP_200_OK)

    def check_balance(self, request, *args, **kwargs):
        card_token = request.data.get('token')
        my_card = HumoCard.objects.filter(token=card_token).first()

        if my_card is None:
            return Response(data={'error': "card with this token not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'balance': my_card.balance}, status=status.HTTP_200_OK)

class AddCardAPIView(CreateAPIView):
    queryset = HumoCard.objects.all()
    serializer_class = HumoCardSerializer


class TransferViewSet(ViewSet):
    def up(self, request, *args, **kwargs):
        pan = request.data.get('pan')
        amount = int(request.data.get('amount'))
        assert amount > 0, ValueError('amount should be grater than 0')
        humocard = HumoCard.objects.filter(pan=pan).first()
        humocard.balance += amount
        humocard.save(update_fields=['balance'])
        return Response(data={'message': "Successfully transfer"}, status=status.HTTP_200_OK)

    def down(self, request, *args, **kwargs):
        card_token = request.data.get('cardToken')
        amount = int(request.data.get('amount'))
        assert amount > 0, ValueError('amount should be greater than 0')
        humocard = HumoCard.objects.filter(token=card_token).first()
        assert humocard.balance > amount, ValueError('balance should be grater than amount')
        humocard.balance -= amount
        humocard.save(update_fields=['balance'])
        return Response(data={'message': "Successfully transfer"}, status=status.HTTP_200_OK)


class HumoCardInfoViewSet(ViewSet):
    def info(self, request, *args, **kwargs):
        data = request.GET
        card_token = data.get('cardToken')
        if card_token is None:
          pan = data.get('pan')
          assert pan is not None, ValueError('pan or cardToken is required')
          humocard = HumoCard.objects.filter(pan=pan).first()
          return Response(data=HumoCardSerializer(humocard).data, status=status.HTTP_200_OK)

        card = HumoCard.objects.filter(token=card_token).first()
        return Response(data=CardSerializer(card).data, status=status.HTTP_200_OK)

class UzCardOTPViewSet(ViewSet):
    def send(self, request, *args, **kwargs):
        uzcard = UzCard.objects.filter(pan=request.data['pan'], expire_month=request.data['expire_month'],
                                           expire_year=request.data['expire_year']).first()
        if uzcard is None:
            return Response(data={'error': "card with this pan not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.create(phone_number=uzcard.phone_number)
        otp.save()

        send_otp_telegram(otp)

        return Response(data={'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)


    def verify(self, request, *args, **kwargs):
        otp_key = request.data['otp_key']
        otp_code = request.data['otp_code']
        otp = OTP.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
        if otp is None:
            return Response(data={'error': 'otp code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        if (timezone.now() - otp.created_at) > timedelta(minutes=3):
            return Response(data={'error': 'otp code is expired'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'otp code verified'}, status=status.HTTP_200_OK)

    def check_balance(self, request, *args, **kwargs):
        card_token = request.data.get('token')
        my_card = UzCard.objects.filter(token=card_token).first()

        if my_card is None:
            return Response(data={'error': "Card with this token not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'balance': my_card.balance}, status=status.HTTP_200_OK)


class UzCardAddAPIView(CreateAPIView):
        queryset = UzCard.objects.all()
        serializer_class = UzCardSerializer


class UzCardInfoViewSet(ViewSet):
    def info(self, request, *args, **kwargs):
        data = request.GET
        card_token = data.get('cardToken')
        if card_token is None:
          pan = data.get('pan')
          assert pan is not None, ValueError('pan or cardToken is required')
          uzcard = UzCard.objects.filter(pan=pan).first()
          return Response(data=CarduzSerializer(uzcard).data, status=status.HTTP_200_OK)

        card = UzCard.objects.filter(token=card_token).first()
        return Response(data=UzCardSerializer(card).data, status=status.HTTP_200_OK)

class UzCardTransferViewSet(ViewSet):
    def up(self, request, *args, **kwargs):
        pan = request.data.get('pan')
        amount = int(request.data.get('amount'))
        assert amount > 0, ValueError('amount should be grater than 0')
        uzcard = UzCard.objects.filter(pan=pan).first()
        uzcard.balance += amount
        uzcard.save(update_fields=['balance'])
        return Response(data={'message': "Successfully transfer"}, status=status.HTTP_200_OK)

    def down(self, request, *args, **kwargs):
        card_token = request.data.get('cardToken')
        amount = int(request.data.get('amount'))
        assert amount > 0, ValueError('amount should be greater than 0')
        uzcard = UzCard.objects.filter(token=card_token).first()
        assert uzcard.balance > amount, ValueError('balance should be grater than amount')
        uzcard.balance -= amount
        uzcard.save(update_fields=['balance'])
        return Response(data={'message': "Successfully transfer"}, status=status.HTTP_200_OK)








