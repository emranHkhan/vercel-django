from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(request.data['password']):
            return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


