# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 08:50:51 2023

@author: Usuario
"""
 
import shapely
import math
import geopandas as gpd 
import pandas as pd 
import matplotlib as plt
import numpy as np
from shapely import LineString, Point

#Variables que captura los datos shapefile y dxf
curv = gpd.read_file('C:/Practica_Ivan_Giraldo/taludes/ituango/Curvas.dxf')
dis = gpd.read_file('C:/Practica_Ivan_Giraldo/taludes/ituango/Diseño.dxf')

#Variables globales de calculo
m1 = 0
mO1 = 0
bO1 = 0 
bO2 = 0
b1 = 0

fila = []
columna = []

while True:
    
    try:
        direccion = int(input('Hacia que direccion se hace la excavacion? Seleccione un numero de la lista\n'
            '1. Norte\n'
            '2. Sur\n'
            '3. Este\n'
            '4. Oeste\n'
            '5. Nor-este\n'
            '6. Sur-este\n'
            '7. Nor-oeste\n'
            '8. Sur-oeste\n'))
        if 0 < direccion < 9:
            break
        else:
            print('Error, seleccione una opcion de la lista')
    except:
        print('Opcion invalida, por favor verifique su respuesta')

#Clase para crear los objetos
class restante:
    def __init__(self, x, y, z, distancia):
        self.cota = z
        self.x = x
        self.y = y
        self.distancia = distancia

# Funcion para obtener xyz de cada punto de la linea de diseño
def getCoordsDis(n):
    
    # llamar a las variable globales
    global Z
    
    #Variable vacia para capturar primera cota que encuentre
    x1 = None
    
    #Variable vacia para capturar segunda cota que encuentre
    x2 = None
    
    #Recorre cada punto y extrae xyz
    for point in n.coords:
        x, y, z = point
        
        #obtener z de referencia
        Z = z
        #si x no esta lleno, llenelo con el primero
        if not x2:
            if not x1:
                x1 = x
                y1 = y
            else:
                x2 = x
                y2 = y
                rec(x1, y1, x2, y2)
                
                # xr = x1
                x1 = x2
                y1 = y2
                x2 = None
    # recF(x1, y1, x2, y2)

#Calculo de la recta
def rec(x1, y1, x2, y2):
    
    # Variables globales
    global m1, mO1, bO1, bO2, b1, direccion

    try:
        # Calcular pendientes de las rectas te la linea de diseño 
        m1 = (y2 - y1) / (x2 - x1)
        
        if direccion == 5 or direccion == 8:
            if m1 < 0:
                mO1 = (-1 /m1)
                bO1 = y1 - (mO1 * x1)
                bO2 = y2 - (mO1 * x2)
                b1 = (m1 * x1) - y1
                
                for i in curv.itertuples():
                    p = (i.geometry)
                    GetCoordsCur(p)
        elif direccion == 6 or direccion == 7:
            if m1 > 0:
                mO1 = (-1 /m1)
                bO1 = y1 - (mO1 * x1)
                bO2 = y2 - (mO1 * x2)
                b1 = (m1 * x1) - y1
                
                for i in curv.itertuples():
                    p = (i.geometry)
                    GetCoordsCur(p)
    except:
        pass
    
#Calculo de la recta
# def recF(x1, y1, x2, y2):
    
#     # Variables globales
#     global m1, mO1, mM, bM, bO1, mA, bOA, b1

#     # Calcular pendientes de las rectas te la linea de diseño 
#     m1 = (y2 - y1) / (x2 - x1)
    
#     # Calculo de ortogonales perpendiculares a las rectas
#     mO1 = (-1 /m1)
    
#     #calculo para b de la recta ortogonal 1 mO1
#     bO1 = (mO1 * x2) - y2
    
#     #calculo para b de la recta 1
#     b1 = (m1 * x1) - y1
    
#     for i in curv.itertuples():
#         GetCoordsCur(i.geometry)
    
# Funcion para obtener xyz de cada punto de la linea de las curvas
def GetCoordsCur(n):
    
    global Z
    # Recorre cada punto y extrae xyz
    
    for punto in n.coords:
        x, y, z = punto
        if z==Z :
            #llamado a la funcion para seccionar los puntos
            seccion(x, y, z)

def seccion (x, y, z):
    #calculo de distancias para seccionar 
    global mO1, m1, b1, bO1, bO2
    
    res1 = (mO1*x)+bO1
    res2 = (mO1*x)+bO2
    
    if res1 > y > res2 or res1 < y < res2:
        distancia(x, y, z, m1, b1)

def distancia (x, y, z, m, b):
    
    global fila, direccion, columna
    
    raiz = (np.sqrt((m)**2+(1*1)))
    resultado = (((m*x-y)-b)/raiz)
    
    if direccion == 7 or direccion == 8:
        resultado = resultado * (-1)
    
    fila.append(x)
    fila.append(y)
    fila.append(z)
    fila.append(resultado)
    columna.append(fila)
    fila = []
    # print ("guardado con exito")
    # print("{:.4}".format(resultado))

for j in dis.itertuples():
    mA = 0
    getCoordsDis(j.geometry)

df = pd.DataFrame(columna)
df = df.to_csv("C:\Practica_Ivan_Giraldo\Generados\intento01.csv")
