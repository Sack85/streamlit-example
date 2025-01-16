import streamlit as st

from image2text import image2text
import transformationRecetas as tR
import tratamientoFicheros as tF

def simplificarIngredientes(textsImages):
    textsImages = tR.AdaptacionIngredientes(textsImages, "pOIngredientesAlternativos")

    return textsImages

def simplificarPreparacion(textsImages):
    textsImages = tR.AdaptacionRecetas(textsImages, "p1AdaptacionThermomix")
    textsImages = tR.AdaptacionRecetas(textsImages, "p2RecordarCantidades")
    textsImages = tR.AdaptacionRecetas(textsImages, "p3SimplificarPreparacion")

    return textsImages['UltimaPreparacion']

def main():


    etaps = ["Menu", "Ingredientes", "Preparacion"]
    st.title("Subir Fotos en Streamlit")
    
    # Botón para subir las fotos de las recetas que seran convertidas
    for etap in etaps:
        files = tF.subirFotos(etap)
        image2text(etap, files)

    # Botón para simplificar la preparación
    if st.button("Simplificar la preparacion"):
        textsImages = {etap: (tF.loadTextExtracted(etap)) for etap in etaps}
        textsImages['UltimaPreparacion'] = textsImages['Preparacion']
        # textsImages = simplificarIngredientes(textsImages)
        recetaSimplificada = simplificarPreparacion(textsImages)
        # Mostrar el resultado en Streamlit
        tF.editarRecetaSimplificada(recetaSimplificada)
if __name__ == "__main__":
    main()