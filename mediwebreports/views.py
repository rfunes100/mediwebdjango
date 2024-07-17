from django.shortcuts import render
from django.contrib import messages
from mediwebreports.models import sqlserverconn , UsuarioAdd
import pyodbc

def connsql(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=rdmwipdbuat;'
                          'Database=mediweb;'
                          'Trusted_Connection=yes;'
                          'UID=replicacion;'
                          'PWD=replicacion;')
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM [mediweb].[dbo].[Enfermera]")
    result =cursor.fetchall()
    return render(request, 'Index.html', {'sqlserverconn': result})


def login(request):
    if request.method == "POST":
        conn = pyodbc.connect('Driver={sql server};'
                              'Server=rdmwipdbuat;'
                              'Database=mediweb;'
                              'Trusted_Connection=yes;'
                              'UID=replicacion;'
                              'PWD=replicacion;')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [mediweb].[dbo].[Usuario] WHERE Userid = ? AND Clave = ?", 
                       (request.POST['Userid'], request.POST['Clave']))
        userdetails = cursor.fetchone()
        if userdetails is not None:
            print("userdetails", userdetails)
            request.session["Userid"] = userdetails.Userid
            return render(request, 'Enfermera.html')
        else:
            messages.success(request, 'Username / password invalid')
    return render(request, 'login.html')


def logindb(request):
    if request.method == "POST":
        try:
            userdetails = UsuarioAdd.objects.get(Userid= request.POST['Userid'], Clave= request.POST['Clave'], )
            print("userdetails",userdetails)
            request.session["Userid"] = userdetails.Userid
            return render(request, 'Usuarios.html')
        except UsuarioAdd.DoesNotExist:
            messages.success(request, 'Username / password invalid')
    return render(request, 'login.html')


def MenuHeader(request):
    return render(request, 'MenuHeader.html')



def Enfermera(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=rdmwipdbuat;'
                          'Database=mediweb;'
                          'Trusted_Connection=yes;'
                          'UID=replicacion;'
                          'PWD=replicacion;')
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM [mediweb].[dbo].[Enfermera]")
    result =cursor.fetchall()
    return render(request, 'Enfermera.html', {'sqlserverconn': result})



def Usuarios(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=rdmwipdbuat;'
                          'Database=mediweb;'
                          'Trusted_Connection=yes;'
                          'UID=replicacion;'
                          'PWD=replicacion;')
    cursor= conn.cursor()
    cursor.execute("""
    SELECT usu.id, Userid, CONCAT(usu.Nombre, ' ', Apellido) AS nombre, correo, r.Nombre AS Rol, usu.Estado
    FROM Usuario usu
    INNER JOIN (
        SELECT * FROM rol
    ) r ON r.id = usu.RolId
    WHERE usu.Estado = 'REGISTRADO'
""")
    result =cursor.fetchall()
    return render(request, 'Usuarios.html', {'sqlserverconn': result})


def EnfermeraAdd(request):
    return render(request, 'EnfermeraAdd.html')
