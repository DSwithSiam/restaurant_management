from rest_framework import viewsets
from .models import Restaurant, Menu, MenuItem
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer
from .permissions import IsOwner, IsEmployee
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order




class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.queryset.filter(restaurant__owner=self.request.user)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsOwner, IsEmployee]

    def get_queryset(self):
        return self.queryset.filter(menu__restaurant__owner=self.request.user)
    
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    @action(detail=True, methods=['post'])
    def create_payment(self, request, pk=None):
        order = self.get_object()
        order.create_payment_intent()
        return Response({'client_secret': order.stripe_payment_intent_id})