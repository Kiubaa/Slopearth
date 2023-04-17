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
curv = gpd.read_file('C:/Practica_Ivan_Giraldo/Taludes_v3.0/Curvas.dxf')
dis = gpd.read_file('C:/Practica_Ivan_Giraldo/Taludes_v3.0/Diseño.dxf')

mA = 0 #Variable aux global que contiene pendiente media (debe usarse en el siguiente bucle como mO1 solo para seccionar)

m1 = 0
mO1 = 0
bO1 = 0 
mM = 0
bM = 0
b1 = 0
bOA = 0
cont = 0

fila = []
columna = []

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
    
    #Variable vacia para capturar tercera cota que encuentre
    x3 = None
    
    #Recorre cada punto y extrae xyz
    for point in n.coords:
        x, y, z = point
        
        #obtener z de referencia
        Z = z
        #si x no esta lleno, llenelo con el primero
        if not x3:
            if not x2:
                if not x1:
                    x1 = x
                    y1 = y
                else:
                    x2 = x
                    y2 = y
            else:
                x3=x
                y3=y
                # print (x1, x2, x3, z)
                # ejecutar el calculo de recta de diseño con los datos obtenidos
                rec(x1, y1, x2, y2, x3, y3)
                
                # xr = x1
                x1 = x2
                y1 = y2
                x2 = x3
                y2 = y3
                x3 = None
    recF(x1, y1, x2, y2)

#Calculo de la recta
def rec(x1, y1, x2, y2, x3, y3):
    
    # Variables globales
    global m1, mO1, mM, bM, bO1, mA, bOA, b1
    
    # print ("paso 1")
    
    # Calcular pendientes de las rectas te la linea de diseño 
    m1 = (y2 - y1) / (x2 - x1)
    m2 = (y3 - y2) / (x3 - x2)
    
    # Calculo de ortogonales perpendiculares a las rectas
    mO1 = (-1 /m1)
    mO2 = (-1 /m2)
    
    # Pendiente media entre ambas ortogonales
    mM =  (mO1 + mO2)/2
    
    #calculo para b media
    bM = (mM * x2) - y2
    
    #calculo para b de la recta ortogonal 1 mO1
    bO1 = (mO1 * x1) - y1
    
    #calculo para b de la recta 1
    b1 = (m1 * x1) - y1
    
    if mA == 0:
        mA = mM
        bOA = bM
        
    else:
        mO1 = mA
        mA = mM
        bO1 = bOA
        bOA = bM
    
    for i in curv.itertuples():
        p = (i.geometry)
        GetCoordsCur(p)
    mO1 = 0
    bO1 = 0
    
#Calculo de la recta
def recF(x1, y1, x2, y2):
    
    # Variables globales
    global m1, mO1, mM, bM, bO1, mA, bOA, b1

    # Calcular pendientes de las rectas te la linea de diseño 
    m1 = (y2 - y1) / (x2 - x1)
    
    # Calculo de ortogonales perpendiculares a las rectas
    mO1 = (-1 /m1)
    
    #calculo para b de la recta ortogonal 1 mO1
    bO1 = (mO1 * x2) - y2
    
    #calculo para b de la recta 1
    b1 = (m1 * x1) - y1
    
    for i in curv.itertuples():
        GetCoordsCur(i.geometry)
    
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
    global mM, mO1, m1, b1, bM, bO1
   
    res1 = (mO1*x)+bO1
    res2 = (mM*x)+bM
    
    if (res1<=0 and res2>=0)or(res2<=0 and res1>=0):
        distancia(x, y, z, m1, b1)
        
def distancia (x, y, z, m, b):
    
    global fila
    raiz = (np.sqrt((m)**2+(1*1)))
    resultado = (((m*x-y)-b)/raiz)
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
df = df.to_csv("intento01.csv")