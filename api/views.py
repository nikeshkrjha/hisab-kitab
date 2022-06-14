from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from khata.models import AppUser, ExpenseCategory, ExpenseItem, Transaction
from api.serializers import AppUserSerializer, CategorySerializer, ExpenseItemSerializer, TransactionSerializer, ExpenseItemSerializer1
import logging

# Create your views here.

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('message')

@csrf_exempt
@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        snippets = AppUser.objects.all()
        serializer = AppUserSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET', 'POST'])
def transactions_list(request):
    """
    List all transactions, or create a new transaction.
    """
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        logging.debug(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def exp_category_list(request):
    if request.method == 'GET':
        categories = ExpenseCategory.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        logging.debug(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def expenses_list(request):
    if request.method == 'GET':
        logging.debug(request.data)
        if 'appuser' in request.data:
            expenses = ExpenseItem.objects.filter(appuser__id=request.data['appuser'])
        else:
            expenses = ExpenseItem.objects.all()
        serializer = ExpenseItemSerializer1(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = ExpenseItemSerializer(data=request.data)
        logging.debug(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
