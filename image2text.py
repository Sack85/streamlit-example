import streamlit as st
import base64
from prompts import prompts

from openai import OpenAI  # Ensure the `openai` package is installed and authenticate properly
client = OpenAI(api_key="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")

import tratamientoFicheros as tF

def extractTextFromImage(etap, file):
    # Define the etap prompts
    textsImages = {
        "Menu": "",
        "Ingredientes": "",
        "Preparacion": "",
        "UltimaPreparacion": ""
    }
    prompt = prompts(textsImages, etap)
    
    photoBitsFormat = file.read()
    photoBitsFormat64 = base64.b64encode(photoBitsFormat).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{photoBitsFormat64}"
                        },
                    },
                ],
            }
        ],
        temperature = 0.9,
        max_tokens=5000,
    )

    extracted_text = response.choices[0].message.content
    return extracted_text
    

def image2text(etap, files):
    combined_text = ""  # Initialize a variable to store combined text

    for file in files:
        extracted_text = extractTextFromImage(etap, file)
        combined_text = combined_text.append(extracted_text)

    tF.saveJSONfile(etap, combined_text)

    return