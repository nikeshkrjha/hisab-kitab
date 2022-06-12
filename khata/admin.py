from curses import meta
from django.contrib import admin
from khata.models import AppUser, Transaction, Group, ExpenseCategory, ExpenseItem

# Register your models here.


class AppUserAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass

class ExpenseItemAdmin(admin.ModelAdmin):
    pass

class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass



admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ExpenseItem, ExpenseItemAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
