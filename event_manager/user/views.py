from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


@extend_schema(
    description="Register a new user and return the user data along with JWT tokens.",
    summary="Register User",
    request=RegisterSerializer,
    responses={201: UserSerializer},
)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    **UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Retrieve information about the current authenticated user.",
    summary="Get Current User",
    responses={200: UserSerializer},
)
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
