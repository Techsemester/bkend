from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class User(AbstractUser):

    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
        ]

    address         = models.CharField(max_length=254)
    city            = models.CharField(max_length=25)
    state           = models.CharField(max_length=25)
    country         = models.CharField(max_length=25)
    phone           = models.CharField(max_length=11)
    email           = models.EmailField()
    image           = models.ImageField(upload_to='account/user_image/', default=None, blank=True, null=True)
    updated         = models.DateTimeField(auto_now=True)
    created         = models.DateTimeField(auto_now_add=True)
    gender          = models.TextField(choices=GENDER_CHOICES, blank=True, null=True)
    dob             = models.CharField(max_length=25, blank=True, null=True)
    education       = models.CharField(max_length=100, default=None, null=True)
    surname         = models.CharField(max_length=25, default=None, null=True)
    first_name      = models.CharField(max_length=25, default=None, null=True)
    total_questions = models.IntegerField(default=0)
    total_upvotes   = models.IntegerField(default=0)
    total_downvotes = models.IntegerField(default=0)
    total_answers   = models.IntegerField(default=0)
    ts_rank         = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class LoginLogoutFail(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    device              = models.CharField(max_length=254, default="Non-Mobile")
    login               = models.BooleanField(default=False)
    login_time          = models.DateTimeField(default=None, null=True)
    logout              = models.BooleanField(default=False)
    logout_time         = models.DateTimeField(default=None, null=True)
    failed_login        = models.BooleanField(default=False)
    failed_login_time   = models.DateTimeField(default=None, null=True)
    message             = models.TextField(default=None, null=True)
    spare0              = models.CharField(max_length=100, default=None, null=True)
    spare1              = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "LoginLogoutFailures"
        verbose_name_plural = "LoginLogoutFailures"



class ContactUs(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type     = models.CharField(max_length=100, default="Android")
    created_at      = models.DateTimeField(auto_now_add=True)
    subject         = models.CharField(max_length=150)
    message         = models.TextField()
    spare           = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"



class DeviceId(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id       = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    device_type     = models.CharField(max_length=100, default="Android")
    active          = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Device ID"
        verbose_name_plural = "Device IDs"



class ResetRequests(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    token           = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    consumed_at     = models.DateTimeField(auto_now=True)
    consumed        = models.BooleanField(default=False)
    use_case        = models.CharField(max_length=100)

    @property
    def get_consumption(self):
        if self.created_at == self.consumed_at:
            return False
        return True

    def save(self, *args, **kwargs):
        self.consumed = self.get_consumption
        super(ResetRequests, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Reset Request"
        verbose_name_plural = "Reset Requests"

        


class OtherRequests(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    request_type    = models.CharField(max_length=100)
    details         = models.CharField(max_length=254, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Other Request"
        verbose_name_plural = "Other Requests"