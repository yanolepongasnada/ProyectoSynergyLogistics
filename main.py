import csv
""" TOMAR EL PAIS DE ORIGEN COMO EL QUE CONTRATA EL SERVICIO """

print("\n")
#print(lectorCSV)

""" INICIALIZACION DE LOS DICCIONARIOS Y CONJUNTOS QUE SE UTILIZARÁN.
Se crean de manera que se tengan colecciones separadas para las exportaciones e importaciones
Los conjuntos se utilizan para tener siempre un listado completo de los origenes, destinos y medios de transporte sin preocuparse por repetirlos
"""
origenes_exp=set()
destinos_exp=set()

origenes_imp=set()
destinos_imp=set()

rutas_exp=set()
rutas_imp=set()

TransportationTypes_exp=set()
TransportationTypes_imp=set()

"""Los diccionarios se utilizan para tener bien identificados los ingesos correspondientes a las tres opciones requeridas"""
IngresosTransporte_exp=dict()
IngresosTransporte_imp=dict()

IngresosRutas_exp=dict()
IngresosRutas_imp=dict()

IngresosPais_exp=dict()
IngresosPais_imp=dict()

"""Se abre la base de datos y se inicializa el lector de archivos csv"""
Database=open("synergy_logistics_database.csv")
lectorDatabase=csv.reader(Database)

"""Se lee todo el documento una sola vez en este for"""
UnaVez=True
for linea in lectorDatabase:
  #Se desecha la primera linea del archivo
  if UnaVez:
    UnaVez=False
    print(linea)
    continue

  """ Primeramente se encuentra si la operacion leida corresponde a Exportaciones o Importaciones """

  if linea[1]=="Exports":
    #Se llenan los conjuntos
    TransportationTypes_exp.add(linea[7])
    origenes_exp.add(linea[2])
    destinos_exp.add(linea[3])

    #Se suman los ingresos de los paaises
    if len(IngresosPais_exp)<len(origenes_exp):
      IngresosPais_exp[linea[2]]=0;
    IngresosPais_exp[linea[2]]+=int(linea[9])

    #Se suman los ingresos de los medios de transporte
    if len(IngresosTransporte_exp)<len(TransportationTypes_exp):
      IngresosTransporte_exp[linea[7]]=0
      #print(linea[7])
      #print(IngresosTransporte_exp[linea[7]])
    IngresosTransporte_exp[linea[7]]+=int(linea[9])

    #Se suman los ingresos de las rutas
    ruta=linea[2]+'-'+linea[3]
    if ruta in rutas_exp:
      None
    else:
      rutas_exp.add(ruta)
      IngresosRutas_exp[ruta]=0
    IngresosRutas_exp[ruta]+=int(linea[9])
  
  #El codigo es igual para las importaciones
  if linea[1]=="Imports":
    TransportationTypes_imp.add(linea[7])
    origenes_imp.add(linea[2])
    destinos_imp.add(linea[3])

    if len(IngresosPais_imp)<len(origenes_exp):
      IngresosPais_imp[linea[2]]=0;
    IngresosPais_imp[linea[2]]+=int(linea[9])

    if len(IngresosTransporte_imp)<len(TransportationTypes_imp):
      IngresosTransporte_imp[linea[7]]=0
    IngresosTransporte_imp[linea[7]]+=int(linea[9])

    ruta=linea[2]+'-'+linea[3]
    if ruta in rutas_imp:
      None
    else:
      rutas_imp.add(ruta)
      IngresosRutas_imp[ruta]=0
    IngresosRutas_imp[ruta]+=int(linea[9])

  #print(i)
  #if i==10:
  #  break
Database.close()

#Se encuentran los ingresos totales para las rutas de transporte, cosniderando importaciones y exportaciones
IngresosTotalesTransporte=dict()
for medio in TransportationTypes_exp:
  IngresosTotalesTransporte[medio]=IngresosTransporte_exp[medio]+IngresosTransporte_imp[medio]
print("\nIngresosTotalesTransporte:\n",IngresosTotalesTransporte,"\n")

"""
ListaIngresosTransporte_exp=list(IngresosTransporte_exp.values())
ListaIngresosTransporte_exp.sort(reverse=True)
print("\nListaIngresosTransporte_exp:\n",ListaIngresosTransporte_exp,"\n")

ListaIngresosTransporte_imp=list(IngresosTransporte_imp.values())
ListaIngresosTransporte_imp.sort(reverse=True)
print("\nListaIngresosTransporte_imp:\n",ListaIngresosTransporte_imp,"\n")
"""

"""Se define una funcion que obtiene los valores de un diccionario y los ordena de mayor a menor"""
def ValoresOrdenados(dicc):
  lista=list(dicc.values())
  lista.sort(reverse=True)
  return lista


#print("\ListaIngresosTotalesTransporte:\n",ListaIngresosTotalesTransporte,"\n")

"""
Caso2=open("Top3IngresosPorTransporte.txt","w")
Caso2.writelines("Rank \t Medio \t Total de Ingresos\n")
for contador in range(0,3):
  for medio in TransportationTypes_exp:
    if ListaIngresosTotalesTransporte[contador]==IngresosTotalesTransporte[medio]:
      Caso2.writelines(f"{contador+1} \t {medio} \t {ListaIngresosTotalesTransporte[contador]}\n")
Caso2.close()
"""

"""Se define una funcion que escribe en un archivo de texto el top de ingresos dado basado en la informacion dada."""
def ImprimirTop(Top,Lista,Sets,Dicc,Totales,Filename,ColumnName):
  #Top=Numero de elementos a imprimir
  #Lista=Lista de ingresos ordenada descendiente de donde se tomaran los ingresos
  #Sets=Conjunto que contiene las claves del diccionario de donde se obtiene el pais/medio de trsnsporte/ruta
  #Dicc=diccionario que contiene los datos de pais/medio/ruta y sus ingresos totales
  #Totales=Ingresos totales obtenidos de todos los paises/medios/rutas
  #Filename=Nombre del archivo de texto que se generara
  #ColumnName=Identificador de si se trata de un ranking de paises/medios/rutas
  File=open(Filename,"w")
  File.writelines(f"Rank \t {ColumnName} \t Total de Ingresos \t Porcentaje\n")
  Total=0
  #contador va de 0 a Top e indica el numero en el ranking, siendo 0 el ranking de mayores ingresos
  for contador in range(0,Top):
    #clave recorre todas las claves de Dicc
    for clave in Sets:
      #Se en cuanto Lista[contador] sea igual a Dicc[clave], se ha encontrado el pais/medio/ruta (indicado por 'clave') que corresponde al rank indicado por 'contador'. En este punto solo es necesario imprimirlos. Ademas se aniade la informacion que indica a que porcentaje del total le corresponde a cada pais/medio/ruta
      if Lista[contador]==Dicc[clave]:
        File.writelines(f"{contador+1} \t {clave} \t {Lista[contador]} \t {round(100*Lista[contador]/Totales,2)} %\n")
        Total+=Lista[contador]
        LastKey=clave
        break
    #Para evitar repeticiones en el ranking en caso de que haya un pais/medio/ruta con la misma cantidad de ingresos, se elimina del conjunto la ultima clave usada
    Sets.remove(LastKey)
  File.writelines(f"\nRepresentan el {round(100*Total/Totales,2)} % de ingresos en este rubro")
  File.close()

"""Para encontrar el grupo de paises que conforman el 80% de los ingresos, se suman los valores de los ingresos ordenados de manera descendiente hasta que se encuentre que la suma es mayor o igual al 80%. Cuando esto se cumple, se obtiene el numero de paises que son necesarios para alcanzar el 80% de los ingresos"""
ListaIngresosPais_exp=ValoresOrdenados(IngresosPais_exp)
Total=sum(ListaIngresosPais_exp)
suma=0
for i in range(0,len(ListaIngresosPais_exp)):
  suma+=ListaIngresosPais_exp[i]
  #print(suma/Total)
  if suma/Total>=0.8:
    print(i)
    break
#print("\nListaIngresosPais_exp:\n",ListaIngresosPais_exp,"\n")
ImprimirTop(i+1,ListaIngresosPais_exp,origenes_exp,IngresosPais_exp,Total,"Top80%IngresosPais_exp.txt","Pais")

ListaIngresosPais_imp=ValoresOrdenados(IngresosPais_imp)
Total=sum(ListaIngresosPais_imp)
suma=0
for i in range(0,len(ListaIngresosPais_imp)):
  suma+=ListaIngresosPais_imp[i]
  #print(suma/Total)
  if suma/Total>=0.8:
    print(i)
    break
#print("\nListaIngresosPais_imp:\n",ListaIngresosPais_imp,"\n")
ImprimirTop(i+1,ListaIngresosPais_imp,origenes_imp,IngresosPais_imp,Total,"Top80%IngresosPais_imp.txt","Pais")

"""Para el resto de rankings el top ya esta definido, por lo que no es necesario calcularlo y simplemente se llama la funcion 'ImprimirTop' con los argumetos correspondientes"""
ListaIngresosTotalesTransporte=ValoresOrdenados(IngresosTotalesTransporte)
Total=sum(ListaIngresosTotalesTransporte)
ImprimirTop(3,ListaIngresosTotalesTransporte,TransportationTypes_exp,IngresosTotalesTransporte,Total,"Top3IngresosPorTransporte.txt","Medio")

ListaIngresosRutas_exp=ValoresOrdenados(IngresosRutas_exp)
Total=sum(ListaIngresosRutas_exp)
ImprimirTop(10,ListaIngresosRutas_exp,rutas_exp,IngresosRutas_exp,Total,"Top10IngresosRutas_exp.txt","Ruta")

ListaIngresosRutas_imp=ValoresOrdenados(IngresosRutas_imp)
Total=sum(ListaIngresosRutas_imp)
ImprimirTop(10,ListaIngresosRutas_imp,rutas_imp,IngresosRutas_imp,Total,"Top10IngresosRutas_imp.txt","Ruta")

#print("\nTransportationTypes:\n",TransportationTypes_exp,"\n")
#print("Ingresos por exportaciones por transporte",IngresosTransporte_exp,"\n")
#print("Ingresos por importaciones por transporte",IngresosTransporte_imp,"\n")


#print("Ingresos por exportaciones por transporte",IngresosPais_exp,"\n")
#print("Ingresos por importaciones por transporte",IngresosPais_imp,"\n")

#print("origenes_exp:\n",origenes_exp, "\ntotal de origenes de exportacion: ",len(origenes_exp),"\n")
#print("destinos_exp:\n",destinos_exp,"\ntotal de destinos de exportacion: ",len(destinos_exp),"\n")

#print("origenes_imp:\n",origenes_imp, "\ntotal de origenes de importacion: ",len(origenes_imp),"\n")
#print("destinos_imp:\n",destinos_imp,"\ntotal de destinos de importacion: ",len(destinos_imp),"\n")

