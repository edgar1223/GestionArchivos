from rest_framework_simplejwt.authentication import JWTAuthentication
from MyGestionArchivo.models import Usuario
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Given a validated token, attempt to retrieve the user using
        the user_id.
        """
        try:
            user_id = validated_token["id"]
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        if not user.is_active:
            raise AuthenticationFailed('Usuario inactivo o eliminado')

        return user
