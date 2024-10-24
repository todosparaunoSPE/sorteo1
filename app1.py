# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 18:01:14 2024

@author: jperezr
"""

import streamlit as st
import sqlite3
import pandas as pd
import random
import time

# Función para conectarse a la base de datos SQLite
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Cargar los participantes desde la base de datos
def cargar_participantes(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, folio FROM participantes")
    participantes = cursor.fetchall()
    conn.close()
    return participantes

# Título de la app
st.title("Simulación de Sorteo por Folios")

# Cargar el archivo de base de datos SQLite
uploaded_file = st.file_uploader("Cargar archivo SQLite (.db)", type=["db"])

if uploaded_file is not None:
    # Guardar el archivo en una ubicación temporal
    with open("temp_sorteo_participantes.db", "wb") as f:
        f.write(uploaded_file.read())
    
    # Cargar los participantes desde el archivo cargado
    try:
        participantes = cargar_participantes("temp_sorteo_participantes.db")

        # Convertir los participantes a un DataFrame
        df_participantes = pd.DataFrame(participantes, columns=["Nombre", "Folio"])
        
        # Mostrar el DataFrame en la app
        st.write("Participantes y Folios:")
        st.dataframe(df_participantes)

        # Botón para iniciar el sorteo
        folio_display = st.empty()

        if st.button("Iniciar sorteo"):
            st.write("Iniciando sorteo...")
            folio_ganador = None  # Inicializar el folio ganador

            # Obtener la lista de folios
            folios = df_participantes['Folio'].tolist()
            
            # Simular el "desfile" de folios
            for _ in range(50):  # Desfila 50 veces antes de elegir el ganador
                folio_actual = random.choice(folios)
                folio_display.markdown(f"### Folio: {folio_actual}")
                time.sleep(0.1)
                folio_ganador = folio_actual  # Actualizar el folio ganador con el actual
            
            # Ahora, folio_ganador contendrá el último folio mostrado
            ganador = df_participantes[df_participantes['Folio'] == folio_ganador].iloc[0]
            
            # Mostrar el ganador
            st.success(f"¡El ganador es: {ganador['Nombre']} con el folio {folio_ganador}!")
    
    except Exception as e:
        st.error(f"Error al cargar los participantes: {e}")
else:
    st.info("Por favor, carga un archivo SQLite para comenzar.")
