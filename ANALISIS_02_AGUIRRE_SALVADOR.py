#Hecho por salvador para proyecto 02
#####funciones:


def checkExistence_AndOrAdd_unordered(dictArg, name1, name2):
    if (name1 in dictArg):
        dictArg[name1] = dictArg[name1] + 1
    elif (ruta2 in dictArg):
        dictArg[name2] = dictArg[name2] + 1
    else:
        dictArg.update({name1: 1})


def checkExistence_AndOrAdd(dictArg, name, value):
    if (name in dictArg):
        dictArg[name] = dictArg[name] + value
    else:
        dictArg.update({name: 1})


def orderANDprintlist_till_n(dictArg, n):
    copyDict = dictArg.copy()
    copyDict = dict({
        key: value
        for key, value in sorted(
            copyDict.items(), key=lambda item: item[1], reverse=True)
    })

    idx = 1
    for key in copyDict:
        if (idx > n): break
        #print(str(idx) + '. ' + key + ' : ' + str(copyDict[key]))
        num = '{:,}'.format(int(copyDict[key]))
        print(idx,'. ',key,': ',num,sep='')
        idx = idx + 1


##########
import csv

#abro el archivo y obtengo la informacion necesaria
lineas = []
with open("synergy_logistics_database.csv", "r") as archivo_csv:
    #lector = csv.reader(archivo_csv, delimiter=",")
    lector = csv.DictReader(archivo_csv)

    for linea in lector:
        lineas.append(linea)

    #lector = list(lector)
    #print(lector)

####consigna 1 rutas mas usadas####
print("*************Consigna 1***************")
#lrd = listaRutasDemandadas #aunque son diccionarios
#Imp = Importacion
#Exp = Importacion
lrd_Imp = {}
lrd_Exp = {}
for linea in lineas:
    #print(linea)
    #declaro variables para evitar repetir accesos a la informacion
    direccion = linea['direction']
    origen = linea['origin']
    destino = linea['destination']
    #como solo importa la ruta, no direccion, checo ambos
    #y los juntos
    ruta = origen + " - " + destino
    ruta2 = destino + " - " + origen

    if (direccion == "Imports"):
        checkExistence_AndOrAdd_unordered(lrd_Imp, ruta, ruta2)
    elif (direccion == "Exports"):
        checkExistence_AndOrAdd_unordered(lrd_Exp, ruta, ruta2)
    else:
        print("error: " + direccion)
print("Rutas de IMPORTACIONES más demandadas:")
orderANDprintlist_till_n(lrd_Imp, 10)
print("--------------------------------------")
print("Rutas de EXPORTACIONES más demandadas:")
orderANDprintlist_till_n(lrd_Exp, 10)

#consigna 2 medios de transporte mas importantes segun valor de import Y export
# cual medio deberia reducirse?
print("**************************************")
print("*************Consigna 2***************")
print("---Medios de transporte importantes segun el valor del producto")
transportesPorValor = {}
for linea in lineas:
    #simplemente saco los transportes usados y les voy agregando los valores
    medioTrans = linea['transport_mode']
    valor = int(linea['total_value'])
    checkExistence_AndOrAdd(transportesPorValor,medioTrans ,valor)

orderANDprintlist_till_n(transportesPorValor, 5)

#consigna 3 paises que le generan el 80% de valor de imp y exp
#en que grupo deberia enfocarse más?
print("**************************************")
print("*************Consigna 3***************")
print("---Paises que generan mayor valor de los movimientos")
paisesPorValor = {}
for linea in lineas:
    direccion = linea['direction']
    #saco los paises segun cual genera la demanda (por direccion), para así agregar
    # el valor correspondiente y evita mezclas irrelevantes.
    if (direccion == "Imports"):
        #claramente si se importa la demanda fue generada por el pais de destino
        pais = linea['destination']
    elif (direccion == "Exports"):
        #viceversa para el pais de origen
        pais = linea['origin']
    else:
        print("error: " + direccion)
    valor = int(linea['total_value'])
    checkExistence_AndOrAdd(paisesPorValor,pais ,valor)

numPaisesRelevantes = int(len(paisesPorValor) * 0.8)
#orderANDprintlist_till_n(paisesPorValor, numPaisesRelevantes)
print('El 80% es hasta (inclusivo) el pais número:',numPaisesRelevantes)
orderANDprintlist_till_n(paisesPorValor, 500) #para ver cuantos paises hay