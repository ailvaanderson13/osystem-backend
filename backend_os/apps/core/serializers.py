import re
from abc import ABC
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from rest_framework import serializers, viewsets, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from .models import MyUser, CadastroOS, ParametrosOS, Projetos, Feriado, Equipes, Clientes


class CadastroOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastroOS
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            nome=validated_data['nome'],
            sobrenome=validated_data['sobrenome']
        )
        Token.objects.create(user=user)

        user.set_password(validated_data['password'])
        user.save()

        return user


class ParametrosOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametrosOS
        fields = '__all__'


class ProjetosOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projetos
        fields = '__all__'


class FeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = '__all__'


class EquipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipes
        fields = '__all__'


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'


def validateEmail(email):
    if len(email) > 6:
        if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return 1
    return 0


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs