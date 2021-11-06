import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Returns an array of axis/ a single axis. 
def setup_graphs(graphs = 1, axes = True):
    r"""
    Inicializa un numero "n" de graficass.
    Todas las graficas son de tamaño 10*10 y usan el modo oscuro
    """
    plt.rcParams["figure.figsize"] = [10, graphs*10]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(graphs, 1)
    #Returns single element instead of array
    
    
    if(graphs == 1):
        setup_axis(ax)
    else:
        for a in ax:
            setup_axis(a)
    

    
    if(axes == True):
        if graphs == 1:
            plot_axes(ax)
        else:
            for a in ax:
                plot_axes(a)
    return ax    


#Setups an axis to dark mode
def setup_axis(ax):
    r"""
    Cambia el eje a modo oscuro
    """ 
    ax.set_facecolor((0,0,0))
    ax.spines['bottom'].set_color((1,1,1))
    ax.spines['left'].set_color((1,1,1))
    ax.spines['right'].set_color((1,1,1))
    ax.spines['top'].set_color((1,1,1))
    
    ax.xaxis.label.set_color((1,1,1))
    ax.yaxis.label.set_color((1,1,1))
    
    ax.tick_params(axis='y', colors=(1,1,1))
    ax.tick_params(axis='x', colors=(1,1,1))
    
#Returns RGB for pint in 2d space
def rgbcolor(x , y):
    r"""
    devuelve una tupla r,g,b para un punto bidimensional
    siguiendo el orden de los cuadrantes en dos 2d, los colores 
    son azul, verde, rojo, amarillo
    """
    gren = x - 1
    gren = min(gren , 0)
    gren = max(gren, -1)
    gren = gren*-1
    
    red = y - 1
    red = min(red, 0)
    red = max(red, -1)
    red = red*-1
    
    blue = y + 1
    blue = min(blue, x+1)
    blue = max(blue, 0)
    blue = min(blue , 1)

    return (red, gren, blue)

def plot_bases(basis, ax):
    r"""
    Grafica los vectores base de la grafica ax. Basis debe de ser una matriz de 4*2.
    Ejemplo: Basis = [[0 ,0] son los puntos iniciales de los vectores base en 2d
                      [0, 0]
                      [1, 0]
                      [0, 1]
    """
    base = basis.clone()
    base[2:] -= basis[:2]
    ax.arrow(*basis[0], *basis[2], length_includes_head = True, color = (1,0,0), width = 0.04)
    ax.arrow(*basis[1], *basis[3], length_includes_head = True, color = (0,1,0), width = 0.04)
    
def plot_axes(ax):
    r"""
    Plots x and y axes
    """
    ax.axvline(color = (1,1,1,.8))
    ax.axhline(color = (1,1,1,.8))
    
    
    