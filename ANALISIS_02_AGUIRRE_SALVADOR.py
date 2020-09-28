#Hecho por salvador para proyecto 02
#####funciones:


#para ordenar rutas sin importar la direccion
def checkExistence_AndOrAdd_unordered(dictArg, name1, name2):
    if (name1 in dictArg):
        dictArg[name1] = dictArg[name1] + 1
    elif (ruta2 in dictArg):
        dictArg[name2] = dictArg[name2] + 1
    else:
        dictArg.update({name1: 1})


#para ir reuniondo valores segun una referencia comun como pais o transporte
def checkExistence_AndOrAdd(dictArg, name, value):
    if (name in dictArg):
        dictArg[name] = dictArg[name] + value
    else:
        dictArg.update({name: 1})


#ordena e imprime hasta el numero n en la lista
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
        print(idx, '. ', key, ': ', num, sep='')
        idx = idx + 1


#ordena e imprime hasta el porcentil n en la lista
def orderANDprintlist_till_percentile(dictArg, percentile, totalValue):
    stop = totalValue * percentile
    copyDict = dictArg.copy()
    copyDict = dict({
        key: value
        for key, value in sorted(
            copyDict.items(), key=lambda item: item[1], reverse=True)
    })

    idx = 1
    auxCounter = 0
    for key in copyDict:
        num = '{:,}'.format(int(copyDict[key]))
        auxCounter += int(copyDict[key])
        if (auxCounter > stop): break
        print(idx, '. ', key, ': ', num, sep='')
        idx = idx + 1

#para responder la ultima pregunta de la consigna 3, diferenciando el
# motivo por que se genera ese valor y el pais
def creaListaPorMotivo(lineas, dictArg, direccionDeseada):
    valorTotal = 0
    for linea in lineas:
        direccion = linea['direction']
        #similar a arriba, pero ahora difiero motivo entre lista de paises
        if (direccion != direccionDeseada): continue
        if (direccion == "Imports"):
            #claramente si se importa la demanda fue generada por el pais de destino
            pais = linea['destination']
        elif (direccion == "Exports"):
            #viceversa
            pais = linea['origin']
        else:
            print("error: " + direccion)
        valor = int(linea['total_value'])
        valorTotal += valor
        checkExistence_AndOrAdd(dictArg, pais, valor)
    return valorTotal


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

    #aqui ya segun importacion o exportacion voy haciendo el conteo de las rutas
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
    #de una
    checkExistence_AndOrAdd(transportesPorValor, medioTrans, valor)

orderANDprintlist_till_n(transportesPorValor, 5)

#consigna 3 paises que le generan el 80% de valor de imp y exp
#en que grupo deberia enfocarse más?
print("**************************************")
print("*************Consigna 3***************")
print("---Paises que generan mayor valor de los movimientos")
paisesPorValor = {}
valorTotal = 0
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
    valorTotal += valor
    checkExistence_AndOrAdd(paisesPorValor, pais, valor)
print('El 80% del valor viene de los paises:')
#obteniendo lista de paises por porcentil del valor
orderANDprintlist_till_percentile(paisesPorValor, 0.8, valorTotal)

#viendo bien la pregunta "en que grupo concentrarse?"
# se entiende difiere entre paises que exportan e importan
print("--------------------------------------")
print("---------Por Importaciones------------")
IMP_paisesPorValor = {}
valorTotal = creaListaPorMotivo(lineas, IMP_paisesPorValor, 'Imports')
print('El 80% del valor viene de los paises:')
#obteniendo lista de paises por porcentil del valor
orderANDprintlist_till_percentile(IMP_paisesPorValor, 0.8, valorTotal)
#imprimiendo todos los paises
#orderANDprintlist_till_percentile(IMP_paisesPorValor, 1, valorTotal)

print("--------------------------------------")
print("---------Por Exportaciones------------")
EXP_paisesPorValor = {}
valorTotal =creaListaPorMotivo(lineas, EXP_paisesPorValor, 'Exports')
print('El 80% del valor viene de los paises:')
#obteniendo lista de paises por porcentil del valor
orderANDprintlist_till_percentile(EXP_paisesPorValor, 0.8, valorTotal)
#imprimiendo todos los paises
#orderANDprintlist_till_percentile(EXP_paisesPorValor, 1, valorTotal)
