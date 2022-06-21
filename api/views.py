from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from khata.models import AppUser, ExpenseCategory, ExpenseItem, Group, Transaction
from api.serializers import AppUserSerializer, CategorySerializer, ExpenseItemSerializer, GroupSerializer, \
    TransactionSerializer, ExpenseItemSerializer1

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
import logging

# Create your views here.

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def exp_category_list(request):
    if request.method == 'GET':
        categories = ExpenseCategory.objects.filter(
            created_by__id=request.user.id)
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        request.data.update({"created_by": request.user.id})
        serializer = CategorySerializer(data=request.data)
        logging.debug(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expenses_list(request):
    if request.method == 'GET':
        logging.debug(request.user.id)
        expenses = ExpenseItem.objects.filter(
            appuser__id=request.user.id)
        logger.debug(expenses)
        serializer = ExpenseItemSerializer1(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = ExpenseItemSerializer(data=request.data)
        logging.debug(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expenses_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    logger.debug(request.data)
    try:
        exp_item = ExpenseItem.objects.get(
            appuser__id=request.user.id, id=pk)
    except ExpenseItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        exp_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = ExpenseItemSerializer(exp_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ExpenseItemSerializer(expenses_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def groups_list(request):
    if request.method == 'GET':
        categories = Group.objects.all()
        serializer = GroupSerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['POST', ])
def register_user(request):
    if request.method == 'POST':
        serializer = AppUserSerializer(data=request.data)
        logger.debug(request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            data = get_user_response_dict(user, token)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("***** User Creattion Failed *****")
            return Response({"error": "Request Failed !!!!"}, status=status.HTTP_400_BAD_REQUEST)


def get_user_response_dict(user, token):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "token": token.key
    }
