from decimal import Decimal
from django.core.mail import send_mail
from django.db import transaction
import requests
from uuid import uuid4
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import FundSerializer, TransferSerializer
from .models import Transaction, Wallet


# Create your views here.

@api_view()
def welcome(request):
    return Response(f"welcome to django")

@api_view()
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
        amount=(amount/100),
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
        "email": email,
        "callback_url": "http://localhost:8000/wallet/fund/verify",
    }
    try:
        response_str = requests.post(url=url, json=data, headers=headers)
        response = response_str.json()
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        return None
    except requests.exceptions.RequestException as e:
        return Response({"message": f"Unable to complete transaction. {e}"}, status=status.HTTP_302_FOUND)

@api_view()
def verify_fund(request):
    reference = request.GET.get('reference')
    secret = settings.PAYSTACK_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response_str = requests.get(url=url, headers=headers)
    response = response_str.json()
    if response['status'] and response['data']['status'] == "success":
        amount = (response['data']['amount'] / 100)
        try:
            transaction = Transaction.objects.get(reference=reference, verified=False)
        except Transaction.DoesNotExist:
            return Response({"message": "Transaction does not exist"}, status=status.HTTP_404_NOT_FOUND)
        wallet = get_object_or_404(Wallet, user=transaction.sender)
        wallet.deposit(Decimal(amount))
        transaction.verified = True
        transaction.save()

        subject = "Eazi-Pay Transaction Alert"
        message = f"""Deposit transaction occurred on your wallet
        You received: {amount} 
        from {transaction.sender.first_name} {transaction.sender.last_name}
        *****thank you for using Eazi-Pay***"""
        from_email = settings.EMAIL_HOST_USER
        recipient_email = transaction.sender.email

        send_mail(
            subject=subject,
            recipient_list=[recipient_email],
            message=message,
            from_email=from_email
        )

        return Response({"message": "Deposit successful"}, status=status.HTTP_200_OK)
    return Response({"message": "Transaction not successful"}, status=status.HTTP_404_NOT_FOUND)


"""
curl https://api.paystack.co/transaction/initialize 
-H "Authorization: Bearer YOUR_SECRET_KEY"
-H "Content-Type: application/json"
-X POST
"""
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def transfer(request):
    data = TransferSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    amount = data.validated_data['amount']
    account_number = data.validated_data['account_number']
    sender = request.user
    sender_wallet = get_object_or_404(Wallet, user=sender)
    receiver_wallet = get_object_or_404(Wallet, account_number=account_number)
    receiver = receiver_wallet.user
    with transaction.atomic():
        reference = f"ref_{uuid4().hex}"
        try:
            sender_wallet.withdraw(amount)
        except ValueError:
            return Response({"message": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
        Transaction.objects.create(
        amount=amount,
        sender=sender,
        reference=reference,
        transaction_type="T",
        verified=True,
        )
        subject = "Eazi-Pay Transaction Alert"
        message = f"""Debit transaction occurred on your wallet
                You transferred: {amount} 
                from {sender.first_name} {sender.last_name}
                *****thank you for using Eazi-Pay***"""
        from_email = settings.EMAIL_HOST_USER
        recipient_email = sender.email

        send_mail(
            subject=subject,
            recipient_list=[recipient_email],
            message=message,
            from_email=from_email
        )
        receiver_wallet.deposit(amount)
        reference = f"ref_{uuid4().hex}"
        Transaction.objects.create(
        amount=amount,
        sender=receiver,
        reference=reference,
        transaction_type="D",
        verified=True,
        )
        subject = "Eazi-Pay Transaction Alert"
        message = f"""Credit transaction occurred on your wallet
                You received: {amount} 
                from {receiver.first_name} {receiver.last_name}
                *****thank you for using Eazi-Pay***"""
        from_email = settings.EMAIL_HOST_USER
        recipient_email = receiver.email

        send_mail(
            subject=subject,
            recipient_list=[recipient_email],
            message=message,
            from_email=from_email
        )
        return Response({"message": "Transfer successful"}, status=status.HTTP_200_OK)

