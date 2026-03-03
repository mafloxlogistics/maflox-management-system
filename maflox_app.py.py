#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:38:36 2026

@author: nato
"""

import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Gestión de Viajes MAFLOX", layout="centered")

# 2. ESTILO DARK MODE Y BLOQUEO DE BOTONES DE IMAGEN
st.markdown("""
    <style>
    /* Fondo principal y barra superior */
    .stApp {
        background-color: #000000;
    }
    header[data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    
    /* ELIMINAR EL BOTÓN DE EXPANDIR/FULLSCREEN EN IMÁGENES */
    button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* Barra lateral negra */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333;
    }
    
    /* Slogan Naranja en Sidebar */
    .slogan-sidebar {
        color: #FF8C00 !important;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Bloqueo de interacción en imágenes */
    img {
        pointer-events: none;
        user-select: none;
    }
    
    /* Letras blancas generales */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: white !important;
    }
    
    /* Botón general (Blanco) */
    .stButton>button {
        background-color: #ffffff;
        color: black;
        border-radius: 20px;
        font-weight: bold;
        border: none;
    }

    /* Botón de Consultar (Naranja MAFLOX) */
    div.stButton > button:first-child {
        background-color: #FF8C00 !important;
        color: #000000 !important;
    }

    /* Inputs con estilo oscuro */
    input {
        background-color: #1A1A1A !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL CON LOGO, SLOGAN Y NAVEGACIÓN
try:
    # Nota: Para el dominio web, cambiaremos esta ruta local por una URL o archivo relativo
    st.sidebar.image("/Users/nato/Desktop/Maflox/Logos/1.png", width=180)
    st.sidebar.markdown('<p class="slogan-sidebar">Un respaldo en cada recorrido</p>', unsafe_allow_html=True)
except:
    st.sidebar.header("MAFLOX LOGISTICS")
    st.sidebar.markdown('<p style="color: #FF8C00;">Un respaldo en cada recorrido</p>', unsafe_allow_html=True)

st.sidebar.markdown("---")
opcion = st.sidebar.radio("Seleccione Portal:", ["Inicio", "Registro Interno", "Portal de Clientes"])

# BASE DE DATOS TEMPORAL
if 'viajes' not in st.session_state:
    st.session_state.viajes = pd.DataFrame(columns=["ID Viaje", "Cliente", "Unidad", "Ruta", "Estatus", "Evidencia POD"])

# --- PÁGINA DE INICIO ---
if opcion == "Inicio":
    st.title("Bienvenido a Gestión de Viajes MAFLOX")
    st.write("Seleccione una opción en el menú lateral para comenzar.")
    try:
        st.image("/Users/nato/Desktop/Maflox/Logos/1.png", width=400)
    except:
        pass

# --- PORTAL INTERNO (SEGURIDAD CON CÓDIGO) ---
elif opcion == "Registro Interno":
    st.title("Acceso Operativo MAFLOX")
    password = st.text_input("Ingrese Código de Autorización", type="password")
    
    if password == "MAFLOX2026": 
        st.success("Acceso Autorizado")
        with st.expander("Registrar Nuevo Embarque"):
            with st.form("nuevo_viaje"):
                cliente = st.text_input("Nombre del Cliente")
                unidad = st.selectbox("Unidad", ["Torton", "Rabon", "Caja Seca 53'"])
                ruta = st.text_input("Ruta (Origen - Destino)")
                if st.form_submit_button("Generar Folio"):
                    nuevo_id = f"MAF-{len(st.session_state.viajes) + 1:03d}"
                    nueva_fila = {"ID Viaje": nuevo_id, "Cliente": cliente, "Unidad": unidad, 
                                  "Ruta": ruta, "Estatus": "En Ruta", "Evidencia POD": "Pendiente"}
                    st.session_state.viajes = pd.concat([st.session_state.viajes, pd.DataFrame([nueva_fila])], ignore_index=True)
                    st.success(f"Viaje {nuevo_id} creado.")

        st.markdown("---")
        st.subheader("Tablero de Control")
        st.dataframe(st.session_state.viajes)
    elif password != "":
        st.error("Código incorrecto")

# --- PORTAL DE CLIENTES (SEGURIDAD) ---
elif opcion == "Portal de Clientes":
    st.title("Portal de Trazabilidad para Clientes")
    st.write("Consulte el estatus de su carga y evidencias.")
    
    cliente_id = st.text_input("Número de Cuenta / ID Cliente")
    guia_id = st.text_input("Número de Guía (Ej: MAF-001)")
    
    if st.button("Consultar Servicio"):
        resultado = st.session_state.viajes[
            (st.session_state.viajes["ID Viaje"] == guia_id) & 
            (st.session_state.viajes["Cliente"].str.upper() == cliente_id.upper())
        ]
        
        if not resultado.empty:
            st.success("Información Localizada")
            st.write(resultado)
        else:
            st.error("No se encontraron registros con esos datos.")