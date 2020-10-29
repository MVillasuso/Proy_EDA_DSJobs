import os, sys
import matplotlib.pyplot as plt
import plotly

# Guarda el resultado del gráfico dentro  del directorio indicado (creándolo si no existe)
def salvar_plot (dir_name, f_name):

    """ Guarda el archivo como .PNG en el directorio indicado """

    results_dir = os.path.join(dir_name) 
    if not os.path.isdir(results_dir): 
        os.makedirs(results_dir) 
    plt.savefig(results_dir + f_name,bbox_inches='tight') 

def salvarI_plot (fig, dir_name, f_name):

    """ Guarda el archivo dinámico como HTML en el directorio indicado """

    results_dir = os.path.join(dir_name) 
    if not os.path.isdir(results_dir): 
        os.makedirs(results_dir) 
    plotly.offline.plot(fig, filename= results_dir + f_name, auto_open = False)
 

def exportar_json (df, npath, fname):
    results_dir = os.path.join(npath) 
    if not os.path.isdir(results_dir): 
        os.makedirs(results_dir) 
    file_name = npath + fname + ".json"
    df.to_json(file_name)

def exportar_csv (df, npath, fname):
    results_dir = os.path.join(npath) 
    if not os.path.isdir(results_dir): 
        os.makedirs(results_dir) 
    file_name = npath + fname + ".csv"
    df.to_csv(file_name)
