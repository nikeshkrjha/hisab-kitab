from curses import meta
from django.contrib import admin
from khata.models import AppUser, Transaction, Group, ExpenseCategory, ExpenseItem

# Register your models here.


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'date_joined', 'phone_number', 'is_staff')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'item_date', 'amount', 'paid_by')
    list_display_links = ('title', 'paid_by')


class GroupAdmin(admin.ModelAdmin):
    pass


class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'item_date',
                    'amount', 'appuser', 'expense_category')
    list_display_links = ('title', 'appuser')


class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ExpenseItem, ExpenseItemAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
