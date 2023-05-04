from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from users.models import Confirm_User
from users.serializers import UserCreateSerializer, UserAuthoSerializer, ConfirmUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from allauth.account.models import EmailConfirmationHMAC
from rest_framework.permissions import AllowAny


@api_view(['POST'])
def register_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    user.is_active = False
    return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def confirm_user(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         confirmation = EmailConfirmationHMAC.from_key(uid=uid, key=token)
#         confirmation.confirm(request)
#         return Response({'message': 'Email confirmed successfully'})
#     except Exception as e:
#         return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_user(request):
    serializer = ConfirmUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        if Confirm_User.objects.filter(code=request.data['code']):
            User.objects.update(is_active=True)
            return Response(status=status.HTTP_200_OK,
                            data={'Ok!': 'User is active'})
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Code or id not found!'})
    except ValueError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'value error'})


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
