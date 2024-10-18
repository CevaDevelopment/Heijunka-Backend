from django.contrib.auth import authenticate
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Site, Client, TypeClient, Schedule, User, TaskAssignment
from .serializers import SiteSerializer, ClientSerializer, TypeClientSerializer, ScheduleSerializer, UserSerializer, \
    LoginSerializer, TaskAssignmentSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Validar los datos del serializador
        serializer.is_valid(raise_exception=True)
        # Crear el usuario utilizando el serializador
        self.perform_create(serializer)

        return Response({
            'message': 'Se le notificará al correo cuando se le asigne un rol por el admin de la aplicación.'
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'refresh': str(refresh),
                'Token': str(refresh.access_token),
            })
        return Response({'error': 'Credenciales inválidas'}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]  # Solo usuarios administradores pueden acceder

    def perform_create(self, serializer):
        # Puedes agregar lógica adicional aquí si es necesario
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class SiteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class TypeClientViewSet(viewsets.ModelViewSet):
    queryset = TypeClient.objects.all()
    serializer_class = TypeClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        site_id = self.request.query_params.get('siteId', None)
        if site_id is not None:
            queryset = queryset.filter(site__id=site_id)
        return queryset

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer


    @action(methods=['delete'], detail=False)
    def delete_all(self, request):
        count, _ = self.queryset.delete()  # Elimina todas las tareas y obtiene el conteo
        return Response({'deleted': count}, status=status.HTTP_204_NO_CONTENT)

