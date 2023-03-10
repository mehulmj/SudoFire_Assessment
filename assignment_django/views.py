from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Customer
from .serializers import CustomerSerializer

@api_view(['POST'])
def create_customer(request):
    try:
        user = User.objects.get(email=request.data['email'])
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.get(mobile_no=request.data['mobile_no'])
        return Response({'error': 'Mobile no already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass

    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        customer_data = {
            'user': user.id,
            'profile_number': request.data['profile_number'],
        }
        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            return Response({'id': customer.id}, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
