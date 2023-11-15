from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import render
from .models import Transaction
from .serializers import TransactionSerializer
import requests
import json

class ChargeCardAPIView(APIView):
    template_name = "payment/charge_card.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Perform charge using Authorize.Net API
            response = self.charge_card(serializer.validated_data)
            if response['status'] == 'success':
                serializer.save()
                return Response({'message': 'Transaction successful.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Transaction failed.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def charge_card(self, data):
        payload = {
            "createTransactionRequest": {
                "merchantAuthentication": {
                    "name": settings.AUTHORIZE_NET_API_LOGIN_ID,
                    "transactionKey": settings.AUTHORIZE_NET_TRANSACTION_KEY
                },
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": str(data['amount']),
                    "payment": {
                        "creditCard": {
                            "cardNumber": data['card_number'],
                            "expirationDate": data['expiration_date'],
                            "cardCode": data['cvv']
                        }
                    }
                }
            }
        }

        response = requests.post(settings.AUTHORIZE_NET_API_URL, json=payload)
        
        if response.text.startswith('\ufeff'):
            response_text = response.text[1:]
        else:
            response_text = response.text

        result = json.loads(response_text)

        if 'transactionResponse' in result and result['transactionResponse']['responseCode'] == '1':
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': result['messages']["message"][0]['text']}
