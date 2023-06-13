# -----------  Librerias de la interfaz grafica  -----------
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from ui.login import *
from mplwidget import MplWidget

# -----------  Librerias de calculos y graficas matplotlib  -----------
import geopandas as gpd 
import numpy as np
import pandas as pd 
import threading
import matplotlib
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

matplotlib.use('QT5Agg')

# -----------  conexion con base de datos  -----------
# from connection import create
# from connection import login 
# from connection import update 
# from connection import delete



col = []
fila =[]

# -----------  Clase de variables globales  -----------
class varGlobal:
    def __init__(self, curv, dis, m1, mO1, bO1, bO2, b1, direccion, Z, df):
        self.curv = curv
        self.dis = dis
        self.m1 = m1
        self.mO1 = mO1
        self.bO1 = bO1
        self.bO2 = bO2
        self.b1 = b1
        self.direccion = direccion
        self.Z = Z
        self.df = df

# -----------  Interfaz de usuario  -----------
class MainLogin(QMainWindow):
    def __init__(self):
        # =============================================
        # =           Definicion de elementos           =
        # =============================================
        
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

        self.ui.btn_login.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_browse1.clicked.connect(self.browseFilesD)
        self.ui.btn_browse2.clicked.connect(self.browseFilesC)
        self.ui.btn_browse3.clicked.connect(self.browseRoute)
        self.ui.btn_csv.clicked.connect(self.saveCSV)
        self.ui.btn_png.clicked.connect(self.savePNG)

        #los botones hacen los mismo pero de esta manera es que se puso mostrar el mensaje
        self.ui.btn_calculate.clicked.connect(lambda x: self.advice(2, "Procesando..."))
        self.ui.btn_calculate.clicked.connect(self.alert)
        
        
        # ======  End of Section =======

    # -----------  Funcion mensaje (1-verde, 2-amarillo, 3-rojo)  -----------
    
    def advice(self, value, message):
        if value == 1:
            self.ui.lbl_message.setStyleSheet("color: #0d8f11;")
        elif value == 2:
            self.ui.lbl_message.setStyleSheet("color: #e5be01;") 
        elif value == 3:
            self.ui.lbl_message.setStyleSheet("color: #e82344;")

        self.ui.lbl_message.setText(message)

    # -----------  Funcion graficar  -----------
    def grap(self):

        self.axes = self.ui.mplwidget.canvas.axes

        x = varGlobal.df[0]
        y = varGlobal.df[1]
        z = varGlobal.df[2]
        colorD = varGlobal.df[3]

        # # # Definimos los datos de prueba
        # x = [1,2,3,4,5,6,7,8,9,10]
        # y = [5,6,7,8,2,5,6,3,7,2]
        # z = [1,2,6,3,2,7,3,3,7,2]

        # # # Datos adicionales
        # x2 = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
        # y2 = [-5,-6,-7,-8,-2,-5,-6,-3,-7,-2]
        # z2 = [1,2,6,3,2,7,3,3,7,2]

        # # Agregamos los puntos en el plano 3D
        sc = self.axes.scatter(x, y, z, c=colorD, cmap='jet', s=1)
        self.ui.mplwidget.canvas.figure.colorbar(sc)

        self.ui.mplwidget.show()
        self.ui.widget_2.show()

    # -----------  Funcion buscar archivo diseño  -----------
    def browseFilesD(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/Practica_Ivan_Giraldo/taludes/ituango')
            self.ui.lbl_design.setText(fname[0])
            #Variables que captura los datos shapefile y dxf
            varGlobal.dis = gpd.read_file(self.ui.lbl_design.text())
        except:
            pass

    # -----------  Funcion buscar archivos de curvas  -----------
    def browseFilesC(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/Practica_Ivan_Giraldo/taludes/ituango')
            self.ui.lbl_curv.setText(fname[0])
            varGlobal.curv = gpd.read_file(self.ui.lbl_curv.text())
        except:
            pass

    # -----------  Funcion buscar ruta de descarga de resultados  -----------
    def browseRoute(self):
        try:
            fname = QFileDialog.getExistingDirectory(self, 'Open directory', 'C:/')
            self.ui.lbl_route.setText(fname)
        except:
            pass

    # -----------  Funcion alerta "procesando" y ejecucion de calculos  -----------
    def alert(self):
        if self.ui.lbl_design.text() and self.ui.lbl_curv.text() and self.ui.lbl_route.text():

            t = threading.Timer(3, self.calculateFiles)
            t.start()

            print ("procesando")

        else:
            self.advice(2, "Favor, seleccione los archivos mencionados")

    # -----------  Funcion calcular archivos  -----------
    def calculateFiles(self):
        varGlobal.direccion = self.ui.cmb_direction.currentText()

        # Funcion para obtener xyz de cada punto de la linea de diseño
        def getCoordsDis(n):

            #Variable vacia para capturar primera cota que encuentre
            x1 = None
            
            #Variable vacia para capturar segunda cota que encuentre
            x2 = None
            
            #Recorre cada punto y extrae xyz
            for point in n.coords:
                x, y, z = point
                
                #obtener z de referencia
                varGlobal.Z = z

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

        #Calculo de la recta
        def rec(x1, y1, x2, y2):
            try:
                # Calcular pendientes de las rectas te la linea de diseño 
                varGlobal.m1 = (y2 - y1) / (x2 - x1)

                if varGlobal.direccion == "Noreste" or varGlobal.direccion == "Suroeste":
                    try: 
                        if varGlobal.m1 < 0:
                            varGlobal.mO1 = (-1 /varGlobal.m1)
                            varGlobal.bO1 = y1 - (varGlobal.mO1 * x1)
                            varGlobal.bO2 = y2 - (varGlobal.mO1 * x2)
                            varGlobal.b1 = (varGlobal.m1 * x1) - y1
                            
                            for i in varGlobal.curv.itertuples():
                                p = (i.geometry)
                                GetCoordsCur(p)
                    except:
                        print("problema pendiente menor a 0")

                elif varGlobal.direccion == "Sureste" or varGlobal.direccion == "Noroeste":
                    try:
                        if varGlobal.m1 > 0:
                            varGlobal.mO1 = (-1 /varGlobal.m1)
                            varGlobal.bO1 = y1 - (varGlobal.mO1 * x1)
                            varGlobal.bO2 = y2 - (varGlobal.mO1 * x2)
                            varGlobal.b1 = (varGlobal.m1 * x1) - y1
                            
                            for i in varGlobal.curv.itertuples():
                                p = (i.geometry)
                                GetCoordsCur(p)
                    except:
                        print("problema pendiente mayor a 0")
            except:
                pass

        #obtener coordenadas de curva
        def GetCoordsCur(n):
            for punto in n.coords:
                x, y, z = punto
                if z==varGlobal.Z :
                    #llamado a la funcion para seccionar los puntos
                    seccion(x, y, z)

        def seccion (x, y, z):
            res1 = (varGlobal.mO1*x)+varGlobal.bO1
            res2 = (varGlobal.mO1*x)+varGlobal.bO2
    
            if res1 > y > res2 or res1 < y < res2:
                distancia(x, y, z, varGlobal.m1, varGlobal.b1)

        def distancia (x, y, z, m, b):

            global fila, col
            
            raiz = (np.sqrt((m)**2+(1*1)))
            resultado = (((m*x-y)-b)/raiz)
            
            # if varGlobal.direccion == "Noroeste":
            #     if m < 1:
            #         resultado = resultado * (-1)

            if varGlobal.direccion == "Suroeste":
                resultado = resultado * (-1)

            elif varGlobal.direccion == "Sureste":
                if m > 1:
                    resultado = resultado * (-1)
            
            fila.append(x)
            fila.append(y)
            fila.append(z)
            fila.append(resultado)
            col.append(fila)
            fila = []
        try:
            for j in varGlobal.dis.itertuples():
                getCoordsDis(j.geometry)

            self.advice(1, "Finalizado con exito")
            varGlobal.df = pd.DataFrame(col)
            print (varGlobal.df)

            
        except:
            self.advice(3, "Hubo un error, favor intente mas tarde")
        self.grap()

    # -----------  Funcion guardar resultados en csv  -----------
    def saveCSV(self):

        global col
        cadena = self.ui.lbl_curv.text()
        cadena = cadena.split("/")
        cadena = (cadena[-1].split("."))
        df = pd.DataFrame(col)
        df = df.to_csv(self.ui.lbl_route.text()+"/"+cadena[0]+".csv")
        self.advice(1, "Guardado")

    # -----------  Funcion guardar resultados en png  -----------
    def savePNG(self):
        
        cadena = self.ui.lbl_curv.text()
        cadena = cadena.split("/")
        cadena = (cadena[-1].split("."))
        self.ui.mplwidget.canvas.figure.savefig(self.ui.lbl_route.text()+"/"+cadena[0]+"_Graph.png", dpi=300, bbox_inches='tight')
        self.advice(1, "Guardado")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = MainLogin()
    login.show
    sys.exit(app.exec_())