import re
import numpy as np
from Utils.plot_utils import setup_graphs

def obtener_datos_archivo(nombre):
    r"""
    Lee los datos del archivo {nombre}.sjupm. Devuelve el numero de maquinas,
    numero de ordenes, matriz de tiempo de procesamiento por maquina, y matriz de
    tiempo de ajuste por maquina
    
    Se espera que el archivo contenga al inicio dos numeros (N, M) el numero de ordenes
    y el numero de maquinas. 
    Despues siguen M lineas, una por cada maquina, con N numeros cada linea, representando el 
    tiempo de procesamiento cada tarea si fuese realizada por esa maquina.
    
    Despues siguen M matricez, una por cada maquina, donde cada matriz tiene tamanio N*N
    donde el valor de la fila i, columna j, representa el tiempo de ajuste de 
    pasar de la tarea i => j 
    
    """
    with open(f'{nombre}.sjupm', 'r') as file:
        lines = list(line for line in (l.strip() for l in file) if line)
    numeros = lines[0]

    # colocar en lista el número de máquinas y de órdenes
    numbers = [int(s) for s in numeros.split() if s.isdigit()]
    # print(numbers)
    nMaquinas = numbers[1]
    nOrdenes = numbers[0]
    lines = lines[1:]  # remover encabezado de números

    tiemposMaquina = []

    for i in range(nMaquinas):
        numbersLinesMaquinas = [int(s)
                                for s in lines[i].split() if s.isdigit()]
        tiemposMaquina.append(numbersLinesMaquinas)

    lines = lines[nMaquinas:]
    
    tiemposAjuste = []
    for i in range(nMaquinas):
        tiemposAjuste.append([])
        tiemposAjusteMaquina = []
        for j in range(nOrdenes):
            numbersTiemposAjuste = [int(s)
                                    for s in lines[j].split() if s.isdigit()]
            tiemposAjusteMaquina.append(numbersTiemposAjuste)
        tiemposAjuste[i] = tiemposAjusteMaquina
        lines = lines[nOrdenes:]
        
    return nMaquinas, nOrdenes, tiemposMaquina, tiemposAjuste


def obtener_datos_consola():
    r"""
    No esta optimizado a velocidad, no usar para pruebas, usar la version que lee de archivo
    
    Lee los datos de consola. Devuelve el numero de maquinas,
    numero de ordenes, matriz de tiempo de procesamiento por maquina, y matriz de
    tiempo de ajuste por maquina
    
    Se espera que el archivo contenga al inicio dos numeros (N, M) el numero de ordenes
    y el numero de maquinas. 
    Despues siguen M lineas, una por cada maquina, con N numeros cada linea, representando el 
    tiempo de procesamiento cada tarea si fuese realizada por esa maquina.
    
    Despues siguen M matricez, una por cada maquina, donde cada matriz tiene tamanio N*N
    donde el valor de la fila i, columna j, representa el tiempo de ajuste de 
    pasar de la tarea i => j 
    
    """ 
    Input = input()
    Input = re.findall(r"[\w']+", Input)
    nMaquina = int(Input[1])
    nOrdenes = int(Input[0])
    # remover numeros leidos
    Input = Input[2:]
    
    tiemposMaquina = []
    for i in range(nMaquina):
        tiemposMaquina.append(Input[:nOrdenes])
        Input = Input[nOrdenes:]
    #convertir tiemposMaquina a enteros
    for i in range(nMaquina):
        for j in range(nOrdenes):
            tiemposMaquina[i][j] = int(tiemposMaquina[i][j])
    
    tiemposAjuste = []
    for i in range(nMaquina):
        tiemposAjusteMaquina = []
        for j in range(nOrdenes):
            tiemposAjusteMaquina.append(Input[:nOrdenes])
            Input = Input[nOrdenes:]
        tiemposAjuste.append(tiemposAjusteMaquina)
    
    for i in range(nMaquina):
        for j in range(nOrdenes):
            for k in range(nOrdenes):
                tiemposAjuste[i][j][k] = int(tiemposAjuste[i][j][k])
        
    return nMaquinas, nOrdenes, tiemposMaquina, tiemposAjuste


def solucionAleatoria(nMaquinas, nOrdenes):
    r"""
    Regresa un vector de tamanio (nMaquinas - 1 + nOrdenes). El vector va a tener (nMaquina - 1)
    elementos iguales a -1, que representan los separadores, y (nOrdenes) elementos que conformen
    una permutaciones de 0 -> nOrdenes - 1
    
    Cada solucion aleatoria es unica, y tienen la misma probabilidad
    """
    rng = np.random.default_rng()
    X = rng.permutation(np.concatenate((np.arange(nOrdenes), np.ones(nMaquinas-1)*-1), axis = None))
    X = X.tolist()
    X = [int(x) for x in X]
    return X



def generarVecino(X):
    r"""
    Genera un nuevo vetor Y, a partir de una solucion X.
    Toma la ultima tarea de una maquina, y la pone al final de la lista de tareas de cualquier otra maquina
    """
    
    # Genero lista de adyacencia a partir de solucion
    adjacencyList = []
    tempList = []
    for x in X:
        if(x == -1):
            adjacencyList.append(tempList)
            tempList = []
        else:
            tempList.append(x)
    adjacencyList.append(tempList)
    
    # Contar cantidad de maquinas, con listas de trabajo no vacias
    machinesWorking = 0
    nMachines = len(adjacencyList)
    for i in range(nMachines):
        if(len(adjacencyList[i]) != 0):
            machinesWorking += 1
    
    # Escoger una de esas maquinas
    rng = np.random.default_rng()
    randomMachine = int(rng.random()*machinesWorking)
    it = 0
    while(randomMachine >= 0):
        if(len(adjacencyList[it]) == 0):
            it += 1
            continue
        if(randomMachine == 0):
            indexRandom = it
            break
        else:
            it += 1
            randomMachine -= 1
    
    num = adjacencyList[it][-1]
    adjacencyList[it] = adjacencyList[it][:-1]
    
    # Selecionar otra maquina, y agregarle la tarea
    randomMachine = int(rng.random()*(nMachines-1))
    if(randomMachine >= it):
        randomMachine += 1
    adjacencyList[randomMachine].append(num)
    
    # Regresar a la representacion de un solo vector
    Y = []
    primero = True
    for vec in adjacencyList:
        if(primero == False):
            Y.append(-1)
        primero = False
        Y.extend(vec)
    return Y


def funcionObjetivo(X, tiempoProcesamiento, tiempoAjuste):
    r"""
    Calcula el tiempo en el que las maquinas acabaran con todas las tareas, dado cierto acomodo
    X
    """
    x = 0
    y = 0
    ans = 0
    prev = -1
    for i in range(len(X)):
        if(X[i] == -1):
            x = x + 1
            y = 0
            prev = -1
        else:
            if(prev != -1):
                y += tiempoAjuste[x][X[i-1]][X[i]]
            y += tiempoProcesamiento[x][X[i]]
            ans = max(ans, y)
            prev = 1
    return ans

def imprimirSolucion(X, tiempoProcesamiento, tiempoAjuste, ax = setup_graphs()):
    r"""
    Para cada maquina, dibuja una grafica de barras que representa las tareas hechas y el tiempo
    total de procesamiento.
    
    Al final regresa la grafica
    """    
    jet = plt.get_cmap('BuPu')
    colors = jet((np.linspace(0, 1, 13)))
    colors = colors[::-1]
    prev = -1
    xAxis = .8
    yAxis = 0
    x = 0
    colorIndex = 0
    ansC = 0
    ans = 0
    for i in range(len(X)):
        if(X[i] == -1):
            prev = -1
            x = x + 1
            xAxis = xAxis + 1
            yAxis = 0
            colorIndex = 0
        else:
            if(prev != -1):
                tiempoExtra = tiempoAjuste[x][X[i-1]][X[i]]
                ax.bar(x = xAxis, height = tiempoExtra, bottom = yAxis, color = colors[colorIndex])
                yAxis += tiempoExtra
                if(colorIndex >= len(colors) - 1):
                    colorIndex = 0
            prev = X[i]
            tiempoPros = tiempoProcesamiento[x][X[i]]
            ax.bar(x = xAxis, height = tiempoPros, bottom = yAxis, color = colors[colorIndex])
            yAxis += tiempoPros
            colorIndex += 1
            if(colorIndex >= len(colors) - 1):
                colorIndex = 0
            ans = max(ans, yAxis)
            ansC = max(ansC, colorIndex)
    ax.axhline(y = ans, color = colors[ansC], linestyle = "dashed",linewidth = 4)
    return ax