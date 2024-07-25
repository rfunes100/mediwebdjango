"""mediwebreports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.connsql ),
     path('Index',views.connsql , name="Index" ),
    path('Usuarios',views.Usuarios,name="Usuarios" ),
    path('Login',views.login, name="login"),
    path('menuheader',views.MenuHeader),
    path('Enfermera',views.Enfermera, name="Enfermera"),
    path('Enfermeraadd',views.EnfermeraAdd, name="Enfermeraadd"),
    path('EnfermeraDelete/<int:id>',views.EnfermeraDelete, name="EnfermeraDelete"),
    path('EnferemeraEdit/<int:id>',views.EnferemeraEdit, name="EnferemeraEdit"),
    path('Usuarioadd',views.Usuarioadd, name="Usuarioadd"),
    path('CategoriaShow',views.CategoriaShow, name="CategoriaShow"),
    path('ClasificacionEnfermedadesShow',views.ClasificacionEnfermedadesShow, name="ClasificacionEnfermedadesShow"),
    path('ClasificacionExamenMedicoShow',views.ClasificacionExamenMedicoShow, name="ClasificacionExamenMedicoShow"),
    path('pedidoventarpt',views.pedidoventarpt, name="pedidoventarpt"),
    path('Enfermedadesrpt',views.Enfermedadesrpt, name="Enfermedadesrpt"),
    path('Pacientesrp',views.Pacientesrp, name="Pacientesrp"),
    path('MedicamentosMasVendidosrpt',views.MedicamentosMasVendidosrpt, name="MedicamentosMasVendidosrpt")


]
