import pandas as pd
df_winemag = pd.read_csv("/workspaces/PythonPC1/PC5/winemag-data-130k-v2.csv")

## método shape (filas y columnas)
df_winemag.shape

## método head
# head retorna los primeros 2 resultados del dataframe
df_winemag.head(2)

##las columnas que la conforman
df_winemag.columns

# Describe (brinda un resumen de la cantidad de datos, promedio, desviación estandar, minimo, máximo, etc )
df_winemag.describe()

## RENOMBRES DE COLUMNAS
df_winemag_rename = df_winemag.rename(columns={
    'country': 'pais',
    'description': 'descripcion',
    'price': 'precio',
    'province': 'provincia'
})
df_winemag_rename.head(2)

## CREACION DE COLUMNAS
df_winemag['region_total'] = df_winemag.region_1 + df_winemag.region_2
df_winemag['puntos_miles'] = df_winemag.points * 1000
df_winemag['puntos_IGV'] = df_winemag.points * 0.18
df_winemag.head(2)

## REPORTES
#1
df_winemag = df_winemag.sort_values(by=['price', 'country'])
condicion  = (df_winemag.price>=2) & (df_winemag.country=="Portugal")
df_winemag[condicion].head(3)

#2
df_winemag.groupby(['country']).price.agg([len, 'min', 'max', 'mean'])

#3
df_group = df_winemag.groupby(['designation', 'points']).agg(
    {
     'price': ['mean', 'min', 'max']
    }
    # ordenando por points descendentemente y price ascendentemente
).sort_values(by=[('price', 'mean')], ascending=[True])

df_group.head(5)

#4
df_reporte = df_winemag.groupby(['taster_name', 'taster_twitter_handle']).agg(
    {
     'price': ['mean', 'min', 'max']
    }
    # ordenando por points descendentemente y price ascendentemente
).sort_values(by=[('price', 'mean')], ascending=[True])

df_reporte.head(5)

#Exportar a CSV
# Exportar reporte 1
df_winemag[condicion].to_csv('reporte1.csv', index=False)

# Exportar reporte 2
df_winemag.groupby(['country']).price.agg([len, 'min', 'max', 'mean']).to_csv('reporte2.csv', index=False)

# Exportar reporte 3
df_group.to_csv('reporte3.csv', index=False)

# Exportar reporte 4
df_reporte.to_csv('reporte4.csv', index=False)


#Exportar a Excel
# Reporte 1
df_winemag.sort_values(by=['price', 'country']).to_excel('reporte1.xlsx', index=False)

# Reporte 2
df_winemag.groupby(['country']).price.agg([len, 'min', 'max', 'mean']).to_excel('reporte2.xlsx', index=False)

# Aplanar MultiIndex para el Reporte 3
df_group.columns = ['_'.join(col).strip() for col in df_group.columns.values]
df_group.to_excel('reporte3.xlsx', index=False)

# Aplanar MultiIndex para el Reporte 4
df_reporte.columns = ['_'.join(col).strip() for col in df_reporte.columns.values]
df_reporte.to_excel('reporte4.xlsx', index=False)


#Exportar a SQL LITE

import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('reportes.db')

# Exportar reporte 1 a SQLite
df_winemag[condicion].to_sql('reporte1', conn, if_exists='replace', index=False)

# Exportar reporte 2 a SQLite
df_winemag.groupby(['country']).price.agg([len, 'min', 'max', 'mean']).to_sql('reporte2', conn, if_exists='replace', index=False)

# Exportar reporte 3 a SQLite
df_group.to_sql('reporte3', conn, if_exists='replace', index=False)

# Exportar reporte 4 a SQLite
df_reporte.to_sql('reporte4', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()


#Exportar a MONGO DB

#!pip install pymongo

import pandas as pd
from pymongo import MongoClient

# Conectar a MongoDB Atlas
client = MongoClient("mongodb+srv://alebr180302:Alejandra123@cluster0.kh8td.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Seleccionar la base de datos y la colección
db = client['python_pc5']  # Nombre de la base de datos

# Exportar reporte 1 a MongoDB
condicion = (df_winemag.price >= 2) & (df_winemag.country == "Portugal")
db.reporte1.insert_many(df_winemag[condicion].to_dict('records'))

# Exportar reporte 2 a MongoDB
df2 = df_winemag.groupby(['country']).price.agg([len, 'min', 'max', 'mean'])
df2 = df2.reset_index().rename(columns={'len': 'count'})
# Convertir a un diccionario con formato adecuado
db.reporte2.insert_one(df2.to_dict('records')[0])  # Inserta solo el primer documento

# Exportar reporte 3 a MongoDB
df_group = df_winemag.groupby(['designation', 'points']).agg({
    'price': ['mean', 'min', 'max']
}).sort_values(by=[('price', 'mean')], ascending=[True])

# Aplanar MultiIndex
df_group.columns = ['_'.join(col).strip() for col in df_group.columns.values]
db.reporte3.insert_many(df_group.reset_index().to_dict('records'))

# Exportar reporte 4 a MongoDB
df_reporte = df_winemag.groupby(['taster_name', 'taster_twitter_handle']).agg({
    'price': ['mean', 'min', 'max']
}).sort_values(by=[('price', 'mean')], ascending=[True])

# Aplanar MultiIndex
df_reporte.columns = ['_'.join(col).strip() for col in df_reporte.columns.values]
db.reporte4.insert_many(df_reporte.reset_index().to_dict('records'))

print("Todos los reportes han sido exportados a MongoDB.")


##enviar a correo

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Configuración del servidor y credenciales
import os 

smtp_server = 'smtp.gmail.com'  # Cambia esto al servidor SMTP que estés utilizando
smtp_port = 587  # Cambia esto al puerto adecuado
sender_email = 'alebr180302@gmail.com'
sender_password = open('token.txt').read().strip() #os.environ['gmail_pass'] #

# Detalles del correo electrónico
receiver_email = 'gonzalo.delgado.r@uni.pe'
subject = 'Re-envio Reporte EJERCICIO 2'
body = 'Adjunto lo solicitado'

# Crear el objeto MIMEMultipart
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))


# Adjuntar archivo
file_path = '/workspaces/PythonPC1/PC5/reporte2.csv'  # Cambia la ruta al archivo que quieras adjuntar
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype="csv")
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)
    
# Iniciar la conexión con el servidor SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Iniciar el modo seguro
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print('Correo enviado exitosamente')


