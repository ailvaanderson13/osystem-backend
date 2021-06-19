"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.db import router
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from apps.core import views
from rest_framework import routers
from apps.core.views import api_root, MyUserViewSet, CadastroOSViewSet, ClientesViewSet, ProjetosViewSet, \
    ParametrosOSViewSet, EquipesViewSet, FeriadoViewSet

# path('admin/', admin.site.urls),
# path('', include(('apps.core.urls', 'core'), namespace='core')),
# path('token/', token_request, name='token')
router = routers.DefaultRouter()
router.register(r'usuarios', MyUserViewSet)
router.register(r'cadastro', CadastroOSViewSet)
router.register(r'cliente', ClientesViewSet)
router.register(r'projetos', ProjetosViewSet)
router.register(r'parametros', ParametrosOSViewSet)
router.register(r'equipes', EquipesViewSet)
router.register(r'feriado', FeriadoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include(router.urls)),
    url('auth/', obtain_auth_token),
]

