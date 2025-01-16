import streamlit as st
import os

def subirFotos(etap):
    st.header(etap)
    files = st.file_uploader(f"Sube tus fotos para el {etap}", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=etap)
    if files:
        st.write(f"{len(files)} foto(s) subidas para el {etap}.")

    return files

def saveTXTfile(etap, combined_text):
    save_path = f"textExtracted/{etap}.txt"
    with open(save_path, "w") as text_file:
        text_file.write(combined_text)

    st.write(f"Texto combinado extraído para {etap} ha sido guardado en {save_path}")

    return save_path

def loadTextExtracted(etap):
    
    file_path = f"textExtracted/{etap}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            textExtracted = file.read()
    else:
        st.write(f"Archivo {file_path} no encontrado.")
    return textExtracted

def guardadoArchivo(texts, transformation):
    file_path = f"textExtracted/{transformation}.txt"
    with open(file_path, "w") as file:
        file.write(texts)
    return

def editarRecetaSimplificada(recetaSimplificada):
    file_path = f"textExtracted/{recetaSimplificada}.txt"
    
    # Display the simplified preparation text in an editable text area
    editable_preparation = st.text_area("Editar el texto simplificado de preparación", file_path, height=500)

    return
