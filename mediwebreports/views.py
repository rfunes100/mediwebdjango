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
            return render(request, 'Index.html')
        else:
            messages.success(request, 'Username / password invalid')
    return render(request, 'login.html')


def logindb(request):
    if request.method == "POST":
        try:
            userdetails = UsuarioAdd.objects.get(Userid= request.POST['Userid'], Clave= request.POST['Clave'], )
            print("userdetails",userdetails)
            request.session["Userid"] = userdetails.Userid
            return render(request, 'Index.html')
        except UsuarioAdd.DoesNotExist:
            messages.success(request, 'Username / password invalid')
    return render(request, 'login.html')



