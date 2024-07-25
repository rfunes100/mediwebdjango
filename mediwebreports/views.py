from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponse
from mediwebreports.models import sqlserverconn , UsuarioAdd, Enfermera
import pyodbc
from  .DatabaseConnection  import DatabaseConnection 
import datetime
from collections import deque



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
    SELECT usu.id, Userid, usu.Nombre + ' ' + Apellido AS nombre, correo, r.Nombre AS Rol, usu.Estado
    FROM Usuario usu
    INNER JOIN (
        SELECT * FROM rol
    ) r ON r.id = usu.RolId
    WHERE usu.Estado = 'REGISTRADO'
""")
    result =cursor.fetchall()
    print('resultados', result)
    return render(request, 'Usuarios.html', {'sqlserverconn': result})


def EnfermeraAddb(request):
    if request.method == "POST":
       nombre = request.POST["Nombre"]
       telefono = request.POST["Telefono"]
       dNI = request.POST["DNI"]
       direccion = request.POST["Direccion"]
       newenfermera = Enfermera( Nombre = nombre, Telefono = telefono, DNI = dNI, Direccion = direccion )
       newenfermera.save()
     # HttpResponse('enfermera agregada exitosamente')
       return render(request, 'EnfermeraAdd.html')
    else:
        return render(request, 'EnfermeraAdd.html')
  #  return render(request, 'EnfermeraAdd.html')


def EnfermeraAdd(request):
   if request.method == "POST":
        conn = pyodbc.connect('Driver={sql server};'
                              'Server=rdmwipdbuat;'
                              'Database=mediweb;'
                              'Trusted_Connection=yes;'
                              'UID=replicacion;'
                              'PWD=replicacion;')
        cursor = conn.cursor()
        cursor.execute("insert into  [mediweb].[dbo].[Enfermera]  (Nombre, Telefono, DNI, Direccion)   VALUES (?, ?, ?, ? ) ", 
                       (request.POST['Nombre'], request.POST['Telefono'], request.POST['DNI'], request.POST['Direccion']))
        conn.commit()
        cursor.execute("SELECT * FROM [mediweb].[dbo].[Enfermera]")
        result =cursor.fetchall()
        return render(request, 'Enfermera.html', {'sqlserverconn': result})
    
   return render(request, 'EnfermeraAdd.html')


def EnfermeraDelete(request, id):
    print("enfermeraid para hacer el borrado",id, request )
   # enfermera = get_object_or_404(Enfermera, id=id)
    if request.method == 'POST':
          print("enfermeraid",id, request )
          conn = pyodbc.connect('Driver={sql server};'
                              'Server=rdmwipdbuat;'
                              'Database=mediweb;'
                              'Trusted_Connection=yes;'
                              'UID=replicacion;'
                              'PWD=replicacion;')
          cursor = conn.cursor()
          cursor.execute("DELETE FROM [mediweb].[dbo].[Enfermera] WHERE id = ? ",
                          (id ))
          conn.commit()
          cursor.execute("SELECT * FROM [mediweb].[dbo].[Enfermera]")
          result =cursor.fetchall()
        #enfermera.delete()
          return render(request,'Enfermera.html', {'sqlserverconn': result})
    return render(request,'EnfermeraDelete.html', {'id': id})


def EnferemeraEdit(request, id):
     print("enfermeraid para hacer el editado",id, request )
     conn = pyodbc.connect('Driver={sql server};'
                              'Server=rdmwipdbuat;'
                              'Database=mediweb;'
                              'Trusted_Connection=yes;'
                              'UID=replicacion;'
                              'PWD=replicacion;')
     cursor = conn.cursor()
     cursor.execute("select * FROM [mediweb].[dbo].[Enfermera]  WHERE id = ? ",
                          (id ))
     result =cursor.fetchall()
     print("result",result )
   # enfermera = get_object_or_404(Enfermera, id=id)
     if request.method == 'POST':
          cursor = conn.cursor()
          cursor.execute("update  [mediweb].[dbo].[Enfermera] set  Nombre = ?, Telefono = ?, DNI = ?, Direccion = ?   WHERE id = ? ",
                          (request.POST['Nombre'], request.POST['Telefono'], request.POST['DNI'], request.POST['Direccion'], id ))
          conn.commit()
          cursor.execute("SELECT * FROM [mediweb].[dbo].[Enfermera]")
          result =cursor.fetchall()
          return render(request,'Enfermera.html', {'sqlserverconn': result})
     return render(request,'EnferemeraEdit.html', {'sqlserverconn': result})

def Usuarioadd(request):   
   # Get the current date and time
   current_datetime = datetime.datetime.now()
   db = DatabaseConnection()

   db.execute_query("SELECT id , Nombre FROM [mediweb].[dbo].[Rol]")
   resroles = db.fetch_all()

   if request.method == "POST": 
        db.execute_query("insert into  [mediweb].[dbo].[usuario]  ( Userid, Nombre, Apellido, Correo, Estado, RolId, Clave, Huellabimoetrica, PreguntaRecuperacion, RespuestaRecuperacion, fechaCreacion ) "
                          " VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ? ) ", 
                       (request.POST['Userid'], request.POST['Nombre'], request.POST['Apellido'], request.POST['Correo'], 'REGISTRADO' , request.POST['RolId'], request.POST['Clave'] , 'NA', request.POST['PreguntaRecuperacion'] , request.POST['RespuestaRecuperacion'], current_datetime )  )
        db.commit()
        db.execute_query("""
    SELECT usu.id, Userid, usu.Nombre + ' ' + Apellido AS nombre, correo, r.Nombre AS Rol, usu.Estado
    FROM Usuario usu
    INNER JOIN (
        SELECT * FROM rol
    ) r ON r.id = usu.RolId
    WHERE usu.Estado = 'REGISTRADO'
""")
        result = db.fetch_all()
        return render(request, 'Usuarios.html', {'sqlserverconn': result})
   
   return render(request, 'Usuario/Add.html', {'resroles': resroles})


def CategoriaShow(request):
    db = DatabaseConnection()
    db.execute_query("SELECT Id , Descripcion , estado FROM [mediweb].[dbo].[categoria]")
    result = db.fetch_all()
    return render(request, 'Categoria/Show.html', {'sqlserverconn': result})


def ClasificacionEnfermedadesShow(request):
    db = DatabaseConnection()
    db.execute_query("SELECT Id	,Descripcion FROM [mediweb].[dbo].[ClasificacionEnfermedades]")
    result = db.fetch_all()
    return render(request, 'ClasificacionEnfermedades/Show.html', {'sqlserverconn': result})

def ClasificacionExamenMedicoShow(request):
    db = DatabaseConnection()
    db.execute_query("SELECT id ,	Descripcion,	estado  FROM [mediweb].[dbo].[ClasificacionExamenMedico]")
    result = db.fetch_all()
    return render(request, 'ClasificacionExamenMedico/Show.html', {'sqlserverconn': result})



def pedidoventarpt(request):
    informacion = [1400,1500,12000,13000,45000] 
    db = DatabaseConnection()
    db.execute_query(" select  DATENAME(month, FechaCreacion) , CAST(SUM(total) AS INT) AS Total from PedidoEnca where  year(FechaCreacion) = 2024 group by  DATENAME(month, FechaCreacion) ")
    result = db.fetch_all()
    month_names = [item[0] for item in result]
    print('result',result, month_names)
    context = {"categories": month_names, 'values': result, 'table_data':result}
 
    return render(request, 'Reportes/PedidosRpt.html',  context=context)

def Enfermedadesrpt(request):
    informacion = [1400,1500,12000,13000,45000] 
    db = DatabaseConnection()
   # db.execute_query(" select  DATENAME(month, FechaCreacion) as mes , CAST(SUM(total) AS INT) AS Total from PedidoEnca where  year(FechaCreacion) = 2024 group by  DATENAME(month, FechaCreacion) ")
    db.execute_query("""
select  max(clas.Descripcion) as clasificacion , count(*) enfermedades from Enfermedades
inner join 
(
 select * from ClasificacionEnfermedades

) clas on clas.Id =  clasificacionId
group by clasificacionId

""" )

    result = db.fetch_all()
    month_names = [item[0] for item in result]
    print('result',result, month_names)
    context = {"categories": month_names, 'values': result, 'table_data':result}
 
 
    return render(request, 'Reportes/Enfermedades.html',  context=context)


def Pacientesrpt(request):
    db = DatabaseConnection()
    db.execute_query("  select  DATENAME(month, FechaCreacion) , CAST(count(*) AS INT) AS Total from expediente group by  DATENAME(month, FechaCreacion) ")
    result = db.fetch_all()
    month_names = [item[0] for item in result]
    print('result',result, month_names)
    context = {"categories": month_names, 'values': result, 'table_data':result}
 
    return render(request, 'Reportes/Pacientesrp.html',  context=context)


def Pacientesrp(request):
    db = DatabaseConnection()
    db.execute_query("select DATENAME(month, FechaCreacion), CAST(count(*) AS INT) AS Total from expediente group by DATENAME(month, FechaCreacion)")
    result = db.fetch_all()
    
    # Usar una cola para procesar los resultados
    queue = deque(result)
    processed_result = []
    
    while queue:
        item = queue.popleft()
        processed_result.append(item)
    
    month_names = [item[0] for item in processed_result]
    print('result', processed_result, month_names)
    context = {"categories": month_names, 'values': processed_result, 'table_data': processed_result}

    return render(request, 'Reportes/Pacientesrp.html', context=context)

def MedicamentosMasVendidosrptc(request):
    db = DatabaseConnection()
   # db.execute_query(" select  DATENAME(month, FechaCreacion) as mes , CAST(SUM(total) AS INT) AS Total from PedidoEnca where  year(FechaCreacion) = 2024 group by  DATENAME(month, FechaCreacion) ")
    db.execute_query("""
select   max(med.nombre) nombre ,  CAST( sum(pedidoDet.precio) AS INT)  ventas from pedidoDet
 inner join Medicamento med on med.Id = ProductoID
group by ProductoID
order by ventas desc
""" )

    result = db.fetch_all()
      # Ordenar los tres primeros elementos
    top_5 = sorted(result[:5], key=lambda x: x[1], reverse=True)[:5]
    
    # Añadir los elementos restantes sin ordenar
    sorted_result = top_5 + result[5:]
    month_names = [item[0] for item in sorted_result]
    #month_names = [item[0] for item in result]
    print('result',result, month_names)
    context = {"categories": month_names, 'values': sorted_result, 'table_data':sorted_result}
 
 
    return render(request, 'Reportes/MedicamentosMasVendidosrpt.html',  context=context)


def MedicamentosMasVendidosrpt(request):
    db = DatabaseConnection()
    db.execute_query("""
    select max(med.nombre) nombre, CAST(sum(pedidoDet.precio) AS INT) ventas 
    from pedidoDet
    inner join Medicamento med on med.Id = ProductoID
    group by ProductoID
    order by ventas desc
    """)

    result = db.fetch_all()
    
    # Asegurarse de que solo se muestren los primeros cinco elementos
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)[:5]
    
    month_names = [item[0] for item in sorted_result]
    print('result', sorted_result, month_names)
    context = {"categories": month_names, 'values': sorted_result, 'table_data': sorted_result}

    return render(request, 'Reportes/MedicamentosMasVendidosrpt.html', context=context)

