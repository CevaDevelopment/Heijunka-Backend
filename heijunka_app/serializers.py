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
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), allow_null=True, required=False)
    site_name = serializers.CharField(source='site.name', read_only=True, default='No Site Assigned')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role', 'site_id','is_active', 'site_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},  # Hacer que el role no sea obligatorio
            'is_active': {'required': False},
        }

    def create(self, validated_data):
        site = validated_data.pop('site_id', None)  # Extraer el sitio si está presente
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', User.EMPLOYEE),  # Rol por defecto es EMPLOYEE
            is_active=validated_data.get('is_active', True),
            site=site
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Evitar que la contraseña sea obligatoria en las actualizaciones
        password = validated_data.pop('password', None)

        # Actualizar otros campos
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.site = validated_data.get('site_id', instance.site)

        # Si se proporciona una contraseña, actualizarla
        if password:
            instance.set_password(password)

        instance.save()
        return instance



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
        site = validated_data.pop('site_id')  # Esto ahora es una instancia de Site
        type_client = validated_data.pop('type_id')  # Esto ahora es una instancia de TypeClient

        # Crea el cliente usando las instancias extraídas
        client = Client.objects.create(site=site, type=type_client, **validated_data)
        return client

    def update(self, instance, validated_data):
        # Actualizar solo los campos presentes en la solicitud
        instance.name = validated_data.get('name', instance.name)
        instance.site = validated_data.get('site_id', instance.site)
        instance.type = validated_data.get('type_id', instance.type)

        instance.save()
        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class TaskAssignmentSerializer(serializers.ModelSerializer):
    collaborator_name = serializers.CharField(source='collaborator', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ('id', 'hour', 'description', 'quantity', 'collaborator', 'collaborator_name', 'client', 'client_name', 'site', 'site_name')
