from decimal import Decimal

import requests
from uuid import uuid4
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import FundSerializer
from .models import Transaction


# Create your views here.

@api_view()
def welcome(request):
    return Response(f"welcome to django")

def greeting(request, name):
    return render(request, 'hello.html', {'name':name})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def fund_wallet(request):
    data = FundSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    amount = data.validated_data['amount']
    amount *= 100
    email = request.user.email
    reference = f"ref_{uuid4().hex}"
    Transaction.objects.create(
        amount=amount,
        reference=reference,
        sender=request.user
    )
    url = 'https://api.paystack.co/transaction/initialize'
    secret = settings.PAYSTACK_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret}",
    }
    data = {
        "amount": amount,
        "reference": reference,
        "email": email
    }
    try:
        response_str = requests.post(url=url, json=data, headers=headers)
        response = response_str.json()
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        return None
    except requests.exceptions.RequestException as e:
        return Response({"message": f"Unable to complete transaction. {e}"}, status=status.HTTP_302_FOUND)

"""
curl https://api.paystack.co/transaction/initialize 
-H "Authorization: Bearer YOUR_SECRET_KEY"
-H "Content-Type: application/json"
-X POST
"""

