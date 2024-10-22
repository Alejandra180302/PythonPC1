#!pip install requests

# 1 Descargar un archivo .zip mediante código del siguiente url (https://netsg.cs.sfu.ca/youtubedata/) (recomiendo descargar el archivo 0333.zip que es menos pesado)


import requests
import os
import zipfile

# Descargar el archivo zip
url = 'https://netsg.cs.sfu.ca/youtubedata/0306.zip'
response = requests.get(url)

# Guardar el archivo zip
with open('0306.zip', 'wb') as f:
    f.write(response.content)

output_path = './unzip'
os.makedirs(output_path, exist_ok=True)


# 2 Descomprimir los datos en una carpeta que genere y leer mediante pandas alguno de los archivos en esta.

# Descomprimir el archivo
with zipfile.ZipFile('0306.zip', 'r') as zip_ref:
    zip_ref.extractall(path=output_path)

print('Archivo descomprimido exitosamente')

import pandas as pd

# Lee el archivo de texto delimitado por tabulaciones
df = pd.read_csv('/workspaces/PythonPC1/PC5/unzip/0306/2.txt', sep='\t', header=None)

# Asigna los nombres de las primeras 10 columnas
column_names = ['video ID', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 'comments', 'related IDs']

# Autogenera los nombres de las columnas restantes (11 a 29)
for i in range(11, 30):
    column_names.append(f'columna {i}')

# Asigna los nombres de las columnas al DataFrame
df.columns = column_names

# Muestra las primeras filas para verificar
df.head()

# 3 Procesar los datos

# Asigna los nombres de las columnas al DataFrame
df.columns = column_names

# Define las columnas que quieres seleccionar
columns_select = ['video ID', 'age', 'category', 'views', 'rate']

# Filtra el DataFrame con las columnas seleccionadas
df_subset = df[columns_select]

# Muestra las primeras filas del DataFrame filtrado
df_subset.head()

# 4 Procesamiento en Mongo Db

import pandas as pd
from pymongo import MongoClient

# Conectar a MongoDB Atlas
client = MongoClient("mongodb+srv://alebr180302:Alejandra123@cluster0.kh8td.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Seleccionar la base de datos y la colección
db = client['python_pc5']  # Nombre de la base de datos
collection = db['reporte_videos']  # Nombre de la colección

# Definir el subconjunto de columnas
columns_select = ['video ID', 'age', 'category', 'views', 'rate']
df_subset = df[columns_select]

condicion = df_subset['age'] > 10

collection.insert_many(df_subset[condicion].to_dict('records'))

print("Puedes ver los gráficos aquí: https://charts.mongodb.com/charts-project-0-tdffint/public/dashboards/d9b40df0-7d4b-4a39-ae00-5e9555fab0df")
