import json

# Texto original con JSON incrustado en un formato no adecuado
texto_original = """{ "ingredients": [ {"Ingredient": "aubergines", "Quantite": 1.5, "Unite": "kg", "note": ""} ] }"""

# Limpieza para convertir el texto en JSON válido
# Reemplaza `null` (estilo JavaScript) con `None` (estilo Python) usando la función de lectura JSON
# print(texto_original)
ingredientes = json.loads(texto_original)
ingredientes["ingredients"].extend(ingredientes["ingredients"])

# Para asegurarnos de que el JSON está correctamente formateado
json_formateado = json.dumps(ingredientes, indent=4, ensure_ascii=False)

# combined_text = json_formateado + json_formateado 
print(json_formateado)