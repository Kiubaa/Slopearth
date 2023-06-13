# -----------  importe de librerias  -----------
import mysql.connector

# -----------  Conexion a base de datos  -----------
cnn = mysql.connector.connect(
	host='localhost',
	user='root',
	port=3306,
	password='', 
	database='slopearth')

# -----------  Funciones de crud  -----------
def login(user, passw, stat): 
	cur = cnn.cursor()
	cur.execute('SELECT user, password, status_id FROM user')
	datos = cur.fetchall()
	cur.close()
	cnn.close()

	for row in datos:
		if row[]

	return datos

# -----------  Procesamiento de los datos  -----------

dat = read()

# for fila in dat:
# 	print(fila)
