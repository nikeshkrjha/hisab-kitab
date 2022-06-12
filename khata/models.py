from unicodedata import category
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from khata.managers import CustomUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(
        max_length=100, blank=False, verbose_name="First Name")
    last_name = models.CharField(
        max_length=100, blank=False, verbose_name="Last Name")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(
        max_length=14, blank=True, verbose_name="Phone Number")

    def user_directory_path(self, instance, filename):
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    profile_pic = models.ImageField(
        verbose_name="Profile Picture", upload_to='user_uploads', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Transaction(models.Model):
    title = models.CharField(max_length=200, blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    item_date = models.DateTimeField(null=True)
    amount = models.DecimalField(
        blank=False, verbose_name="Total Amount", max_digits=15, decimal_places=2)
    paid_by = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, verbose_name="Paid By")
    # group = models.ForeignKey("Group", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} - ${self.amount}"


class Group(models.Model):
    # group_name = models.CharField(
    #     verbose_name="Group Name", max_length=200, blank=False)
    # date_created = models.DateTimeField(default=timezone.now)
    # created_by = models.ForeignKey(
    #     AppUser, on_delete=models.CASCADE, verbose_name="Created By", related_name="group")
    # members = models.ManyToManyField(AppUser, related_name="group_membership")
    pass


class ExpenseItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title", blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    item_date = models.DateTimeField()
    amount = models.DecimalField(
        blank=False, verbose_name="Amount", max_digits=11, decimal_places=2)
    appuser = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, verbose_name="User")
    expense_category = models.OneToOneField(
        "ExpenseCategory", on_delete=models.SET_NULL, verbose_name="Category", null=True)

    def __str__(self):
        return f"{self.title} {str(self.item_date)}"


class ExpenseCategory(models.Model):
    category_name = models.CharField(
        max_length=200, verbose_name="name", blank=False)

    def __str__(self):
        return self.category_name
