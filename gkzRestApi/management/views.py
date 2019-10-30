from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from management.models import Customer
from management.serializers import CustomerSerializer


@api_view(['GET'])
def get_customers(request):
    customers = Customer.objects.all()
    customers_serializer = CustomerSerializer(customers, many=True)
    return JsonResponse(customers_serializer.data, safe=False)


@api_view(['POST'])
def create_employee(request):
    customer_data = JSONParser().parse(request)
    customer_serializer = CustomerSerializer(data=customer_data)
    if customer_serializer.is_valid():
         customer_serializer.save()
         return JsonResponse(customer_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt 
def customer_detail(request, pk):
    try: 
        customer = Customer.objects.get(pk=pk) 
    except Customer.DoesNotExist: 
        return HttpResponse(status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        customer_serializer = CustomerSerializer(customer) 
        return JsonResponse(customer_serializer.data) 
 
    elif request.method == 'PUT': 
        customer_data = JSONParser().parse(request) 
        customer_serializer = CustomerSerializer(customer, data=customer_data) 
        if customer_serializer.is_valid(): 
            customer_serializer.save() 
            return JsonResponse(customer_serializer.data) 
        return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        customer.delete() 
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)