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
    Ejemplo: '1100' y '1111' -> True
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

def combinarMinTerm(numBits, minTer1, minTer2):
    """
    Resumen: agrupa los minterminos que difieren en un bit.

    Entradas
    - numBits: numero de bits de la expresion booleana. Ejemplo: ABC || BC'D -> numBits es 4
    - minTer1 y minTer2: las cadenas de minterminos a comparar. Ejemplo: minTer1-> '1100' & minTer2 -> '1111'

    Salidas:
    - lista con los minterminos que difieren en un bit
    Ejemplo: 
    """
    bitDiferidos = 0

    for i in range(0, numBits):
        if minTer1[i] != minTer2[i]: # Compare si difieren en un bit
            bitDiferidos += 1
        else:
            continue
    if bitDiferidos > 1: #Si difieren en mas de un bit entonces no
        return False
    else:
        return True