from rest_framework import serializers
from khata.models import AppUser, Transaction, ExpenseItem, ExpenseCategory, Group


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        # fields = ('email', 'first_name', 'last_name', 'phone_number','profile_pic','appgroups')
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('title', 'date_posted', 'amount', 'paid_by')


class ExpenseItemSerializer1(serializers.ModelSerializer):
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


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    # members = AppUserSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'
