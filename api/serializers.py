from re import A
from rest_framework import serializers
from khata.models import AppUser, Transaction, ExpenseItem, ExpenseCategory


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
    paid_by = serializers.SerializerMethodField('get_paid_by')

    def get_paid_by(self, obj):
        return {
            'email': obj.paid_by.email,
            'id': obj.paid_by.id
        }


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = '__all__'
        # depth = 1
    appuser = serializers.SerializerMethodField('get_appuser')

    def get_appuser(self, obj):
        return {
            'email': obj.appuser.email,
            'id': obj.appuser.id
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
