from rest_framework import serializers
from .models import Site, Client, TypeClient, Schedule, User, TaskAssignment
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', User.EMPLOYEE)  # Rol por defecto es EMPLOYEE
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class TypeClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeClient
        fields = '__all__'

from rest_framework import serializers
from .models import Client, Site, TypeClient


from rest_framework import serializers
from .models import Client, Site, TypeClient

class ClientSerializer(serializers.ModelSerializer):
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), write_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=TypeClient.objects.all(), write_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'site_id', 'type_id', 'site_name', 'type_name')

    def create(self, validated_data):
        # Extrae site y type directamente de validated_data
        site = validated_data.pop('site_id')  # Esto ahora es una instancia de Site
        type_client = validated_data.pop('type_id')  # Esto ahora es una instancia de TypeClient

        # Crea el cliente usando las instancias extraídas
        client = Client.objects.create(site=site, type=type_client, **validated_data)
        return client



class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = '__all__'
