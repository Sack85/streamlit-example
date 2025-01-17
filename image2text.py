import streamlit as st
import base64
from prompts import prompts
import json

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
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
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
        response_format={"type": "json_object"},
        temperature = 1,
        max_tokens=5000,
    )

    extracted_text = response.choices[0].message.content
    return extracted_text
    

def image2text(etap, files):
    combined_text = "[]"  # Initialize a variable to store combined text
    combined_text = json.loads(combined_text)

    for file in files:
        extracted_text = extractTextFromImage(etap, file)
        extracted_text = json.loads(extracted_text)
        combined_text.extend(extracted_text["INGREDIENTS"])
    tF.saveJSONfile(etap, combined_text)

    return