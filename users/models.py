from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


class Confirm_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.code


    # def generate_code(self):
    #     self.code = get_random_string(length=6)
    #     self.save()
    #
    # def activate_comment(self, code):
    #     if self.code == code:
    #         self.is_active = True
    #         self.save()
    #         return True
    #     else:
    #         return False
