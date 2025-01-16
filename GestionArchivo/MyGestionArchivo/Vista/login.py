from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from MyGestionArchivo.models import *
from rest_framework_simplejwt.tokens import  TokenError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

class LoginAPIView(APIView):
    authentication_classes = []  # No requiere autenticación previa
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email y contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        if not check_password(password, user.password):
            raise AuthenticationFailed('Credenciales incorrectas')

        # Usar el método personalizado para obtener el token
        token = user.get_token()
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)

class RefreshTokenAPIView(APIView):
      authentication_classes = []  # No requiere autenticación previa
      permission_classes = [AllowAny]
      def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            # Asegurarse de devolver una respuesta en caso de error
            return Response({'error': 'El token de actualización es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validar el token de refresco recibido
            token = RefreshToken(refresh_token)
            
            # Generar un nuevo access token
            new_access = token.access_token
            
            # Opcional: Generar un nuevo refresh token
            new_refresh = RefreshToken()  # Si deseas crear uno nuevo

            # Retornar la respuesta con los tokens
            return Response({
                'access': str(new_access),
                'refresh': str(new_refresh)  # Retornar si decides generar un nuevo refresh token
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            # Manejar el caso de token inválido o expirado
            return Response({'error': 'El token de actualización no es válido o ha expirado'}, status=status.HTTP_401_UNAUTHORIZED)