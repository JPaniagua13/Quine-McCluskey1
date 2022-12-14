import argparse
from distutils.log import info
import sys
from xml.dom import minicompat
from pylatex import Document, Section, Subsection, Command, Math, TikZ, Axis, Plot, Figure,VectorName, Matrix, Alignat,  PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Itemize, Hyperref, Package, Table, Tabular, MultiColumn, MultiRow, Label, Ref, NoEscape

from pylatex.utils import italic, bold, NoEscape, escape_latex
import pandas as pd
import numpy as np
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

def representarBinario(impPrimo, listaInicialMin):
    '''
    Resumen: los números que la lista no contiene son 0's, aquellos que sí tiene son 1's
    Entradas:
    - impPrimo(list): lista de numeros enteros. Ejemplo: [3,7,11,15]
    - listaInicialMin(list): lista incial de minterminos. Ejemplo: [1,3,4,5,7,9,10,11,15]
    Salida:
    - respuesta(str): Ejemplo: '010010011'
    '''
    #repreBits me dira si un elemento es repetido o no, sera util en petrick para identificar implicantes primos esenciales
    repreBits= str()
    for i in range(0,len(listaInicialMin)):     
        if impPrimo.count(listaInicialMin[i])!=0:
            repreBits+= '1' #si el elemento se repite, se identifica con 1
        else:
            repreBits+= '0'#si el elemento no se repite, se identifica con 0        
    return repreBits

def Petricks(listaInicialMin, listaPrimos):
    '''
    Resumen: encuentra los implicantes esenciales

    Entradas:
    - listaPrimos(list): lista de los implicantes primos.
    Ejemplo: [[4, 5], [10, 11], [1, 3, 5, 7], [1, 3, 9, 11], [3, 7, 11, 15]]
    - listaInicialMin(list): lista incial de minterminos.
    Ejemplo: [1,3,4,5,7,9,10,11,15]
    

    Salidas:
    - listaEsenciales(list): lista de los implicantes esenciales. 
    Ejemplo: [[4, 5], [10, 11], [1, 3, 9, 11], [3, 7, 11, 15]]              
    '''
    listaPrimoBits = list()
    listaEsenciales = list()

    #Añade los implicantes primos a una lista en una representación en Bits.
    for i in range(0, len(listaPrimos)):
        listaPrimoBits.append(representarBinario(listaPrimos[i],listaInicialMin))

    for j in range(0, len(listaPrimos)):
        for k in range(0, len(listaInicialMin)): #Itera cifra por cifra
            unico = True
            #Si dos cifras coinciden entonces el implicante no es esencial
            for z in range(0, len(listaPrimos)):
                if j != z and listaPrimoBits[j][k] == listaPrimoBits[z][k]:
                    unico = False
            #Si en ninguna cifra coincida anadala a la lista de esenciales
            if unico == True and listaEsenciales.count(listaPrimos[j]) == 0:
                listaEsenciales.append(listaPrimos[j])

    return listaEsenciales

def implicanteRepetido(numBits, implicante, lista):
    '''
    Resumen: verifica si un implicante primo se encuentra en la lista pero en diferente orden.

    Entradas:
    - numBits(int): numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - implicante(list): el correspondiente implicante a comprobar. Ejemplo: [1,5,3,7]
    - lista(list): lista de listas de implicantes primos. Ejemplo: [[10,11], [1,3,5,7]]

    Salida:
    - (bool) retorna true si sí se encuentra. Ejemplo: [1,5,3,7] -> [[10,11], [1,3,5,7]] = True
    '''
    a = combinarMin(numBits, implicante)
    for k in lista:
        if a == combinarMin(numBits, k):
            return True
    return False

def mezclarMinTer(numBits, minTer1, minTer2):
    '''
    Resumen: toma dos mintérminos que difieren en una cifra y los mezcla. Esto es, coloca una 'X' en la cifra que difieren

    Entradas:
    - numBits(int): numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTer1(str): cadena de un mintérmino. Ejemplo: '01X1'
    - minTer2(str): cadena de un mintérmino. Ejemplo: '00X1'

    Salida:
    - resultado(str): su respectiva combinación. Ejemplo: '0XX1'
    '''
    resultado = str()

    for i in range(0, numBits):
        if minTer1[i] != minTer2[i]: # Compare si difieren en un bit
            resultado += 'X'
        else:
            resultado += minTer1[i]
    return resultado

def partirListaEnDos(lista):
    '''
    Resumen: parte una lista en dos.

    Entradas:
    - lista(list): lista de numeros enteros. Ejemplo: [1,3,5,7]

    Salida:
    - primerMitad, segundaMitad (tuple): una tupla de las dos mitades. Ejemplo: ([1,3] , [5,7])
    '''
    halfpoint = len(lista)/2
    halfpoint = int(halfpoint)

    primerMitad = lista[:halfpoint]
    segundaMitad = lista[halfpoint:]
    return primerMitad, segundaMitad

def combinarMin(numBits, secuencia):
    '''
    Resumen: dada una secuencia de combinaciones halla su representación.

    Entradas: 
    - secuencia (list):la secuencia de una combinación. Ejemplo: [1,3,5,7]

    Salida:
    - (str) la representación que se consigue dada dicha combinación. Ejemplo: [1,3,5,7] -> [1,3] y [5,7]. 
                                                                                Entonces '00X1' y '01X1'
                                                                                Finalmente -> '0XX1'
    '''
    if len(secuencia) == 1:
        return combinarMinTerDecBin(numBits, secuencia[0])                                                                                               
    elif len(secuencia) != 2:
        a = combinarMin(numBits, partirListaEnDos(secuencia)[0])
        b = combinarMin(numBits, partirListaEnDos(secuencia)[1])
        return mezclarMinTer(numBits, a, b)



    return mezclarMinTer(numBits, combinarMinTerDecBin(numBits, secuencia[0]), combinarMinTerDecBin(numBits, secuencia[1]))

def combinarMinTerDecBin(numBits, minDec):
    '''
    Resumen: convierte un mintérmino de decimal a binario

    Entadas:
    - numBits(int): numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTer(int): el mintérmino en representación decimal

    Salida
    - (str) retorna una cadena del mintérmino en decimal

    '''
    cadena = str()
    cadena = bin(minDec)  #Convierte de dec a bin: bin(11) -> '0b1011'
    cadena = cadena[2:] #Trunca el '0b' para que quede solo '1011'

    #Anade ceros segun el numero de bits. Por ejemplo 8 bits es '00001011'
    return cadena.zfill(numBits)

def difierenUnaCifra(numBits, minTer1, minTer2):
    """
    Resumen: comprueba si un mintermino difiere en una cifra.

    Entradas
    - numBits(int): numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTer1(str) y minTer2(str): las cadenas de minterminos a comparar. Ejemplo: minTer1-> '1100' & minTer2 -> '1111'

    Salidas:
    - (bool) si difieren en una cifra retorna true. De lo contrario false. (Si difieren en X's retorna false)
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
    if cifrasDiferidas == 0: #Si difieren en mas de una cifra entonces no
        return False
    elif cifrasDiferidas > 1:
        return False
    else:
        return True

def hallarPrimos( numBits, listaInicial, listaPrimos, primerCorrida, documentoPylatex):
    '''
    Resumen: la función recursiva combina los mintérminos y finalmente halla los primos.

    Entrada:
    - numBits(int): numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - listaInicial(list): una lista de listas de mintérminos. 
    Ejemplo: [1,3,4],[5],[7],[9],[10],[11],[15]]
    - listaPrimos(list): aquí almacena los implicantes primos que encuentra. Comienza vacía
    Ejemplo: []

    Salida:
    - (list) la lista de implicantes primos. 
    Ejemplo: [[4, 5], [10, 11], [1, 3, 5, 7], [1, 3, 9, 11], [3, 7, 11, 15]]
    
    '''
    imprimir_terminos_primos_latex(documentoPylatex, listaInicial,listaPrimos)



    paresAgrupados = list()
    implicantesUtilizados = list()
    huboCombinacion = False

    for i in range(0, len(listaInicial)):
        if len(listaInicial[i]) == 0: # si la lista esta vacía no tiene que comparar
            pass
        else:
            for j in range(0, len(listaInicial)):
                if len(listaInicial[j]) == 0: # si la lista esta vacía no tiene que comparar
                    pass
                else:
                    # la comparación 'j > i' compara dos elementos una sola vez. 
                    # 'primerCorrida = True' porque la primera combinacion es diferente del resto
                    
                    if j > i and primerCorrida == True:
                        if difierenUnaCifra(numBits, combinarMinTerDecBin(numBits, listaInicial[i][0]),
                            combinarMinTerDecBin(numBits, listaInicial[j][0])) == True:
                            paresAgrupados.append([listaInicial[i][0], listaInicial[j][0]])
                            huboCombinacion = True
                            if implicantesUtilizados.count(listaInicial[i]) == 0:
                                
                                implicantesUtilizados.append(listaInicial[i])
                            if implicantesUtilizados.count(listaInicial[j]) == 0:
                                implicantesUtilizados.append(listaInicial[j])                                

                    elif j > i:
                        if difierenUnaCifra(numBits, combinarMin(numBits, listaInicial[i]),
                            combinarMin(numBits, listaInicial[j])) == True:
                            paresAgrupados.append(listaInicial[i] + listaInicial[j])
                            huboCombinacion = True

                            if implicantesUtilizados.count(listaInicial[i]) == 0:
                                implicantesUtilizados.append(listaInicial[i])
                            if implicantesUtilizados.count(listaInicial[j]) == 0:
                                implicantesUtilizados.append(listaInicial[j])   

    for k in listaInicial:
        if implicantesUtilizados.count(k) == 0:
            if primerCorrida == False and implicanteRepetido(numBits, k ,listaPrimos) == False:
                listaPrimos.append(k)
            if primerCorrida == True:
                listaPrimos.append(k)

    if huboCombinacion == False: #No hubo combinaciones, no repita más
        return listaPrimos
    
    else:
        primerCorrida = False

        #Con los elementos que mezclo vuelva a hacer el mismo procedimiento hasta que no se puedan mezclar más
        return hallarPrimos(numBits, paresAgrupados, listaPrimos, primerCorrida, documentoPylatex)

def leer_minterminos(nombre_archivo):
    # directorio del archivo
    archivo_abierto = open(nombre_archivo,"r")
    linea = archivo_abierto.readline()
    # los minterminos se leen como un string '1,2,4,5',
    # Por lo que hay que convertirlos en una lista de numeros 
    minterminos_strings = linea.split(',')
    minterminos_numeros = list(map(int, minterminos_strings))
    return minterminos_numeros


def crear_documento_latex():
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(documentclass='beamer')
    
    with doc.create(Section('titlepage')):
        doc.preamble.append(Command('title', 'Quine McCluskey'))
        doc.preamble.append(Command('institute', 'Tecnologico de Costa Rica'))
        doc.preamble.append(Command('subtitle', 'Diseño Logico'))
        doc.preamble.append(Command('author', 'Fiorela Chavarria, Samuel Montenegro, Jeaustin Paniagua, David Vargas' ))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))   
    doc.append(NewPage())
    return doc

def imprimir_terminos_primos_latex(doc, lista_pares_agrupados,lista_primos ):
    df = pd.DataFrame(np.array(lista_pares_agrupados))

    subsection = Section('Lista de pares agrupados')
    vec = Matrix(np.array(lista_pares_agrupados))
    vec_name = VectorName('a')
    math = Math(data=[vec_name, '=', vec])
    subsection.append(math)
    doc.append(subsection)
        
def guardar_pdf(documento_pylatex, nombre_archivo):
    documento_pylatex.generate_pdf(nombre_archivo, clean_tex=False, compiler='pdflatex')

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
    

    numeroBits = (max(minterminos)).bit_length() # Según el mintérmino más grande, coloca el mínimo num de bits necesarios

    listaX = list()
    for i in range(0, len(minterminos)): #Convierte [1,4,6,15] a -> [[1], [4], [6], [15]].                       
        listaX.append(minterminos[i])             #Esto porque la funcion hallarPrimos los acepta así
        resultado = list()  
        resultado.append(minterminos[i])
        minterminos[i] = resultado


    documento_pylatex = crear_documento_latex()    

    implicantesPrimos = hallarPrimos(numeroBits,minterminos, [], True, documento_pylatex)

    print( Petricks(listaX, implicantesPrimos) )

    guardar_pdf(documento_pylatex, nombre_archivo_salida)



# Ejecuta el programa 
main()
