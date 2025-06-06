from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from wallet.models import Transaction, Wallet
from .models import Profile, User
from .serializers import ProfileSerializer, WalletSerializer, TransactionSerializer


# Create your views here.

class ProfileViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer


    def get_queryset(self):
        try:
            return Profile.objects.filter(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.none()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]


class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]
    #serializer_class = DashBoardSerializer

    def get(self, request):
        try:
            transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-transaction_date')[:5]
            serializer = TransactionSerializer(transactions, many=True)
            return Response({"transactions": serializer.data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

