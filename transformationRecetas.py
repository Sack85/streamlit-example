import streamlit as st
import base64
from openai import OpenAI  # Ensure the `openai` package is installed and authenticate properly
client = OpenAI(api_key="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")

from prompts import prompts
import tratamientoFicheros as tF

def openAiconfig(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=16000,
    )

    reponseOpenAI = response.choices[0].message.content

    return reponseOpenAI


def AdaptacionIngredientes(textsImages, transformation):

    # Recupero el prompt que me interesa incluyendo el texto extraido de las imagenes
    prompt = prompts(textsImages, transformation)

    # Hago la modificacion
    recetaSimplificada = openAiconfig(prompt)
    
    # Guardo el resultado en un archivo de texto de la ULTIMA transformacion
    tF.guardadoArchivo(recetaSimplificada, "ingredientesSimplificados")
    
    return recetaSimplificada


def AdaptacionRecetas(textsImages, transformation):

    # Recupero el prompt que me interesa incluyendo el texto extraido de las imagenes
    prompt = prompts(textsImages, transformation)

    # Hago la modificacion
    recetaSimplificada = openAiconfig(prompt)
    textsImages['UltimaPreparacion'] = recetaSimplificada

    # Guardo el resultado en un archivo de texto de la transformacion
    tF.guardadoArchivo(recetaSimplificada, transformation)
    # Guardo el resultado en un archivo de texto de la ULTIMA transformacion
    tF.guardadoArchivo(recetaSimplificada, "recetaSimplificada")

    return textsImages