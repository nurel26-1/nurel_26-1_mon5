from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.utils import send_email_confirmation

from users.models import Confirm_User


class UserAuthoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(UserAuthoSerializer):
    email = serializers.EmailField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already is existed')


# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#                 six.text_type(user.pk) + six.text_type(timestamp) +
#                 six.text_type(user.is_active)
#         )
#
#
# account_activation_token = TokenGenerator()


# class Custom_Register_Serializer(RegisterSerializer):
#     def save(self, request):
#         user = super().save(request)
#         user.is_active = False
#         user.save()
#         send_verification_email(request, user)
#         return user
#
#
# def send_verification_email(request, user):
#     send_email_confirmation(request, user)


class ConfirmUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_user_id(self, user_id):
        try:
            Confirm_User.objects.get(id=user_id)
        except Confirm_User.DoesNotExist:
            return user_id
        raise ValidationError("User_id does not exists!")
