# Create your views here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from pytz import unicode
from rest_framework import viewsets, authentication, permissions, routers, generics, renderers, parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cloudinary.templatetags import cloudinary
from random import randint
from rest_framework.parsers import MultiPartParser, FormParser, FormParser, MultiPartParser
from django.http import JsonResponse
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions
from .models import MyUser, Equipes, CadastroOS, Projetos, ParametrosOS, Feriado, Clientes
from .serializers import MyUserSerializer, ParametrosOSSerializer, ProjetosOSSerializer, \
    FeriadoSerializer, EquipesSerializer, CadastroOSSerializer, ClientesSerializer, EquipesSerializer, MyUserSerializer, \
    AuthCustomTokenSerializer

# A estrutura REST inclui uma série de classes incorporadas no Parser, que permitem que você aceite solicitações
# com vários tipos de mídia. Há também suporte para definir seus próprios analisadores personalizados, o que lhe dá
# flexibilidade para projetar os tipos de mídia que sua API aceita.

from django.shortcuts import get_object_or_404


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)


class OSAPIRootView(routers.APIRootView):
    """
    Controls appearance of the API root view
    """

    def get_view_name(self) -> str:
        return "My API"

    def get_view_description(self, html=False) -> str:
        text = "OS REST API"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


def token_request(request):
    try:
        new_token = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': new_token[0].key}, status=status.HTTP_200_OK)
    except Exception as message:
        return JsonResponse({'messagem': 'você não tem permissão.'}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes((permissions.AllowAny,))
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cadastro-os': reverse('cadastro-os', request=request, format=format),
        'usuarios': reverse('usuarios', request=request, format=format),
        'feriado': reverse('feriado', request=request, format=format),
        'projetos': reverse('projetos', request=request, format=format),
        'parametros': reverse('parametros', request=request, format=format),
        'clientes': reverse('clientes', request=request, format=format),
    })


# CadastroOS
class CadastroOSViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CadastroOSSerializer

    # Parser
    parser_classes = (MultiPartParser, FormParser,)

    queryset = CadastroOS.objects.all()

    def get(self, request, pk):
        cadastro = Clientes.objects.get(pk=pk)
        serializer = self.serializer_class(cadastro)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, image_name):
        cloudinary.uploader.upload(
            request.FILES['imagem'],
            public_id=image_name,
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ],
            tags=['anexo', 'anexoAPI']
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                image_name = '{0}_v{1}'.format(request.FILES['imagem'].name.split('.')[0], randint(0, 100))
                self.upload_image_cloudinary(request, image_name)
                serializer.save(icon_perfil=image_name)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'imagem': 'Envie uma imagem valida'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        cadastro_os = CadastroOS.objects.get(pk=pk)
        serializer = self.serializer_class(cadastro_os, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cadastro_os = CadastroOS.objects.get(pk=pk)
            cadastro_os.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# MyUser (Funcionarios)
class MyUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    # # Parser
    # parser_classes = (MultiPartParser, FormParser,)
    print("Sr. Incrivel!!!")

    def get(self, request, pk):
        print("Sr. Incrivel!!!")
        myuser = MyUser.objects.get(pk=pk)
        serializer = self.serializer_class(myuser)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, selfie_usuario):
        cloudinary.uploader.upload(
            request.FILES['imagem'],
            public_id=selfie_usuario,
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ],
            tags=['selfie_usuario', 'imagem_usuario']
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                image_name = '{0}_v{1}'.format(request.FILES['imagem'].name.split('.')[0], randint(0, 100))
                self.upload_image_cloudinary(request, image_name)
                serializer.save(selfie_usuario=image_name)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'imagem': 'Envie uma imagem valida'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        myuser = MyUser.objects.get(pk=pk)
        serializer = self.serializer_class(myuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            myuser = MyUser.objects.get(pk=pk)
            myuser.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Feriado
class FeriadoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EquipesSerializer

    queryset = Feriado.objects.all()

    # Parser
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, pk):
        feriados = Clientes.objects.get(pk=pk)
        serializer = self.serializer_class(feriados)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = FeriadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        feriado = self.get_object(pk)
        serializer = FeriadoSerializer(feriado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            feriado = Feriado.objects.get(pk=pk)
            feriado.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Equipes
class EquipesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EquipesSerializer

    queryset = Equipes.objects.all()

    # Parser
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, pk):
        queryset = self.get_object()
        serializer = self.serializer_class(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = EquipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        equipes = Equipes.objects.get(pk=pk)
        serializer = self.serializer_class(equipes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            equipes = Equipes.objects.get(pk=pk)
            equipes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Projetos
class ProjetosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientesSerializer

    # Parser
    # parser_classes = (MultiPartParser, FormParser,)

    queryset = Projetos.objects.all()

    def get(self, request, pk):
        projetos = Clientes.objects.get(pk=pk)
        serializer = self.serializer_class(projetos)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, anexo_projeto):
        cloudinary.uploader.upload(
            request.FILES['imagem'],
            public_id=anexo_projeto,
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ],
            tags=['anexo_projeto', 'anexo_projeto_cli']
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                anexo_projeto_cli = '{0}_v{1}'.format(request.FILES['anexo_projeto'].name.split('.')[0],
                                                      randint(0, 100))
                self.upload_image_cloudinary(request, anexo_projeto_cli)
                serializer.save(logomarca=anexo_projeto_cli)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'imagem': 'Envie uma imagem valida'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        projetos = Projetos.objects.get(pk=pk)
        serializer = self.serializer_class(projetos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            projetos = Projetos.objects.get(pk=pk)
            projetos.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Parametros OS
@permission_classes((permissions.AllowAny,))
class ParametrosOSViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ParametrosOSSerializer

    # Parser
    # parser_classes = (MultiPartParser, FormParser,)

    queryset = ParametrosOS.objects.all()

    def get(self, request, pk):
        parametros = Clientes.objects.get(pk=pk)
        serializer = self.serializer_class(parametros)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ParametrosOSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        parametros = ParametrosOS.objects.get(pk=pk)
        serializer = ClientesSerializer(parametros, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            parametros = ParametrosOS.objects.get(pk=pk)
            parametros.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Clientes
class ClientesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientesSerializer

    queryset = Clientes.objects.all()

    # Parser
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, pk):
        clientes = Clientes.objects.get(pk=pk)
        serializer = self.serializer_class(clientes)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ClientesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        clientes = Clientes.objects.get(pk=pk)
        serializer = ClientesSerializer(clientes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            clientes = Clientes.objects.get(pk=pk)
            clientes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)