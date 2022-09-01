import argparse
from distutils.log import info
import os
import sys
import itertools

# Convertir cada mintérmino de la función booleana por su equivalente en representación binaria

#Agrupar mintérminos por la cantidad de 1s en la representación binaria. Ej: 1010 tiene dos unos y se puede agrupar con 1100 y 0110. Si se está trabajando por con 4 literales, se van a encontrar
#máximo 5 grupos: 0 unos, 1 uno, 2 unos, 3 unos y 4 unos. Los grupos encontrados se ordenan en una tabla.

#Comparar cada número del mintérmino en el grupo superior con canda mintérmino del grupo inferior. Si entre dos números, cada posición es igual menos solo un dígito, se
#anota un número nuevo en otra tabla con la misma representación binaria pero con una x en el dígito que difieren. Asimismo, se le coloca de categoría la composición 
#de los mintérminos que crean el nuevo elemento. En caso que un mintérmino no se puede emparejar con ningún otro de la tabla, este se retira y se marca como implicante primo.

#Con la nueva tabla elaborada por el emparejamiento de implicantes anterior, se agrupan cadaimplicante compuesto por la cantidad de 1s que lo comprenden y se vuelve a
#emparejar elementos como en el paso 3. Considere las x como un dígito más. Si se repiten implicantes primos, preserve uno. Encaso de no poderse simplificar más elementos, se
#seleccionan los implicantes primos encontrados.

#Encontrar los implicantes primos esenciales. Para encontrarlo se elabora la tabla de implicantes primos donde cada implicante primo encontrado se coloca en una fila y los 
#mintérminos que lo componen se marcan como columnas.

#De acuerdo a la tabla, si un mintérmino solo es cubierto por un solo implicante primo, estees un implicante esencial. En caso contrario, si cada mintérmino de un implicante 
#primo puede ser cubierto por los demás, este se retira de la tabla.

#Los implicantes primos esenciales corresponden a la ecuación booleana reducida

def leer_minterminos(nombre_archivo):
    # directorio del archivo
    dir_path = os.path.dirname(os.path.realpath(__file__))
    archivo_abierto = open(dir_path + "\\"+ nombre_archivo,"r")
    linea = archivo_abierto.readline()
    # los minterminos se leen como un string '1,2,4,5',
    # Por lo que hay que convertirlos en una lista de numeros 
    minterminos_strings = linea.split(',')
    minterminos_numeros = list(map(int, minterminos_strings))
    return minterminos_numeros


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Nombre del archivo de salida")
    parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
    args = parser.parse_args()

    if args.file is None:
        print ("Debe de ingresar el nombre del archivo a procesar que tiene los terminos, -f FILE")
        # termina el programa
        sys.exit() 
    if args.output is None:
        print ("Debe de ingresa el nombre del archivo de salida, -o OUTPUT")
        # termina el programa
        sys.exit() 
    
    nombre_archivo_minterminos = args.file
    nombre_archivo_salida = args.output 

    minterminos = leer_minterminos(nombre_archivo_minterminos)
    print(minterminos)



def convertMinTermABinario(numBits, decMinTerm):
    """
    Resumen: convierte una lista de minterminos en decimal a un diccionario con representacion binaria

    Entradas
    - numBits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - decMinTerm: lista con minterminos en decimal. Ejemplo: [1,3,5,7]

    Salidas:
    - un diccionario donde cada pareja es la representacion decimal y binaria del mintermino
    Ejemplo: { 1: '0001', 3: '0011', 5:'0101', 7:'0111'} -> numBits es 4
    """
    diccionario = dict() #Crea un diccionario vacio
    minTerBin = str()    #Crea una cadena vacia

    for i in decMinTerm:
        minTerBin = bin(i)  #Convierte de dec a bin: bin(11) -> '0b1011'
        minTerBin = minTerBin[2:] #Trunca el '0b' para que quede solo '1011'

        #Anade ceros segun el numero de bits. Por ejemplo 8 bits es '00001011'
        diccionario[i]= minTerBin.zfill(numBits) 
    return diccionario

def agruparPorUnos(numBits, minTerSinAgrupar):
    """
    Resumen: agrupa los minterminos segun el numero de 1's

    Entradas
    - numBits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTerm: diccionario con minterminos sin agrupar. Ejemplo: {1:'0001', 2:'0010', 3:'0011', 7:'0111', 8:'1000', 15:'1111'}

    Salidas:
    - una lista de diccionarios con los minterminos agrupados. El indice equivale al num de 1's del grupo
    Ejemplo: [{}, {1: '0001', 2: '0010', 8: '1000'}, {3: '0011'}, {7: '0111'}] -> numBits es 4
    """
    minTerAgrupados = list()

    for i in range(0, numBits):         #i es el numero de 1's a buscar.
        diccionario = dict()            #Cree un diccionario vacio
        for key in minTerSinAgrupar:    #Itere por el diccionario desagrupado en busqueda de un mintermino con i numero de 1's
            if minTerSinAgrupar[key].count('1') == i:    
                diccionario[key] = minTerSinAgrupar[key] # Si coincide anadalo al diccionario

        minTerAgrupados.append(diccionario)  #Agregue el diccionario a la lista
    return minTerAgrupados

def difierenUnaCifra(numBits, minTer1, minTer2):
    """
    Resumen: comprueba si un mintermino difiere en una cifra.

    Entradas
    - numBits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTer1 y minTer2: las cadenas de minterminos a comparar. Ejemplo: minTer1-> '1100' & minTer2 -> '1111'

    Salidas:
    - si difieren en una cifra retorna true. De lo contrario false. (Si difieren en X's retorna false)
    Ejemplo: '1101' y '1111' -> True
             '1100' y '1111' -> False
             '1XX1' y '10X1' -> False
    """
    cifrasDiferidas = 0

    for i in range(0, numBits):
        if (minTer1[i] != minTer2[i]) and (minTer1[i] == 'X'): #Pueden distinguir en 1's pero no en X's
            return False
        elif minTer1[i] != minTer2[i]: # Compare si difieren en una cifra
            cifrasDiferidas += 1
        else:
            continue
    if cifrasDiferidas > 1: #Si difieren en mas de una cifra entonces no
        return False
    else:
        return True

def imprimirImpEsencialesLit(numBits, impEsenBin):
    '''
    Resumen: imprime los minterminos esenciales en su forma literal

    Entrada: lista de minterminos mezclados en su forma binaria. Ejemplo: ['1XX1','0X1X','111X']

    Salida: la cadena con los minterminos en su forma literal. Ejemplo: ' AD + A*C + ABC '
    '''
    cadena = 'ABCDEF'
    impEsenLit = str()

    for i in range(0, len(impEsenBin)): #i representa los indices de la lista
        for j in range(0, numBits): #j representa los indices de las cadenas
            if impEsenBin[i][j] == '1': 
                impEsenLit += cadena[j]
            elif impEsenBin[i][j] == '0':
                impEsenLit += cadena[j] + '*'
            else:
                impEsenBin[i][j] == 'X'
        if i != len(impEsenBin)-1:
            impEsenLit += ' + '
    return impEsenLit

#Funcion necesaria para utilizar metodo de Petrick
#multplicacion logica de dos terminos 
def multiplicacion(lista1, lista2):
    lista_resultante = []
    #Si ambas listas estan vacias
    if (len(lista1) == 0 and len(lista2)== 0):
        return lista_resultante
    #if solo 1 lista esta vacia
    elif len(lista1)==0:
        return lista2
    #if la otra lista esta vacia
    elif len(lista2)==0:
        return lista1

    #Si ninguna de las 2 listas esta vacia
    else:
        for i in lista1:
            for j in lista2:
                #if hay 2 terminos iguales
                if (i == j):
                    lista_resultante.append(i)
                else:
                    lista_resultante.append(list(set(i+j)))

        #ordenar(sort) y eliminar las listas redundantes y devolver esta lista
        lista_resultante.sort()
        return list(lista_resultante for lista_resultante,_ in itertools.groupby(lista_resultante))

    
    
#Metodo petrick 
def petrick(Chart):
    #Lista P inicial
    P = []
    for columna in range(len(Chart[0])):
        #lista p temporal util para lista P inicial
        p =[]
        for fila in range(len(Chart)):
            if Chart[fila][columna] == 1:
                p.append([fila])
        P.append(p)
    # multiplicacion logica
    for l in range(len(P)-1):
        P[l+1] = multiplicacion(P[l],P[l+1])
    #El sorted crea una nueva lista ordenada a partir de un iterable
    P = sorted(P[len(P)-1],key=len)
    lista_final = []
    #encontrar los términos con la longitud mínima = este es el de menor coste (resultado optimizado)
    min=len(P[0])
    for i in P:
        if len(i) == min:
            lista_final.append(i)
        else:
            break
    #final es el resultado de metodo Petrick
    return lista_final

def mezclarMinTer(numBits, minTer1, minTer2):
    '''
    Resumen: sustituye con una X el valor de los mintérminos en que difieren

    Entradas:
    -num bits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    -minTer1 y minTer2: las cadenas de los mintérminos a mezclar. Ejemplo: '1011' y '1111'

    Salidas:
    - una cadena con el correspondiente resultado. Ejemplo: '1X11'
    '''
    resultado = str()

    for i in range(0, numBits):
        if minTer1[i] != minTer2[i]: # Compare si difieren en un bit
            resultado += 'X'
        else:
            resultado += minTer1[i]
    return resultado

def convertirBinarioALiteral(numBits, minTerBinario):
    '''
    Resumen: 

    Entradas:
    -num bits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4

    Salidas:
    '''
    cadena = 'ABCDEF'
    resultado = str()

    for i in range(0, numBits):

        if minTerBinario[i] == '1':  
            resultado += cadena[i]  
        elif minTerBinario[i] == '0':
            resultado += cadena[i] + '*'
        else:
            pass
    return resultado

def combinarMinTerDecBin(numBits, num):
    cadena = str()
    cadena = bin(num)  #Convierte de dec a bin: bin(11) -> '0b1011'
    cadena = cadena[2:] #Trunca el '0b' para que quede solo '1011'

    #Anade ceros segun el numero de bits. Por ejemplo 8 bits es '00001011'
    return cadena.zfill(numBits) 

def combinarMin(numBits, lista):
    if len(lista) != 2:
        a = combinarMin(numBits, partirListaEnDos(lista)[0])
        b = combinarMin(numBits, partirListaEnDos(lista)[1])
        return mezclarMinTer(numBits, a, b)
    return mezclarMinTer(numBits, combinarMinTerDecBin(numBits, lista[0]), combinarMinTerDecBin(numBits, lista[1]))

def combinarMinter2(numBits, lista, implicantesPrimos, cont):
    '''
    Entrada:
    [[1],[3],[5],[7]]

    Salida:
    
    '''
    paresAgrupados = list()
    implicantesUtilizados = list()
    huboCombinacion = False

    for i in range(0, len(lista)):
        if len(lista[i]) == 0:
            pass
        else:
            for j in range(0, len(lista)):
                if len(lista[j]) == 0:
                    pass
                else:
                    if j > i and cont == 0:
                        if difierenUnaCifra(numBits, combinarMinTerDecBin(numBits, lista[i][0]),
                            combinarMinTerDecBin(numBits, lista[j][0])) == True:
                            paresAgrupados.append([lista[i][0], lista[j][0]])
                            huboCombinacion = True

                            ########################################################################
                            if implicantesUtilizados.count(lista[i]) < 0:
                                implicantesUtilizados.append(lista[i])
                            if implicantesUtilizados.count(lista[j]) < 0:
                                implicantesUtilizados.append(lista[j])                                
                            ###########################################################################

                    elif j > i:
                        if difierenUnaCifra(numBits, combinarMin(numBits, lista[i]),
                            combinarMin(numBits, lista[j])) == True:
                            paresAgrupados.append(lista[i] + lista[j])
                            huboCombinacion = True

                            #########################################################
                            if implicantesUtilizados.count(lista[i]) < 0:
                                implicantesUtilizados.append(lista[i])
                            if implicantesUtilizados.count(lista[j]) < 0:
                                implicantesUtilizados.append(lista[j])   
                            #########################################################
    for k in lista:
        if implicantesUtilizados.count(k) < 0:
            implicantesPrimos.append(k)

    if huboCombinacion == False:
        return implicantesPrimos
    else:
        cont += 1
        combinarMinter2(numBits, paresAgrupados, implicantesPrimos, cont)

