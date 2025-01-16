import streamlit as st
import os
from openai import OpenAI  # Ensure the `openai` package is installed and authenticate properly
import base64

client = OpenAI(api_key="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")

def extract_text_from_image(image_data, prompt):
    base64_image = base64.b64encode(image_data).decode('utf-8')

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
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1500,
    )

    extracted_text = response.choices[0].message.content
    return extracted_text

def handle_file_upload(header, key, sections_prompts):
        st.header(header)
        files = st.file_uploader(f"Sube tus fotos para el {header}", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=key)
        if files:
            st.write(f"{len(files)} foto(s) subidas para el {header}.")
            combined_text = ""  # Initialize a variable to store combined text
            for file in files:
                bytes_data = file.read()
                prompt = sections_prompts[header]
                extracted_text = extract_text_from_image(bytes_data, prompt)
                combined_text += extracted_text + "\n"

            save_path = f"{header}.txt"
            with open(save_path, "w") as text_file:
                text_file.write(combined_text)

            st.write(f"Texto combinado extraído para {header} ha sido guardado en {save_path}")

def load_generated_files(sections_prompts):
    loaded_text = {}
    for header in sections_prompts.keys():
        file_path = f"{header}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                loaded_text[header] = file.read()
        else:
            st.write(f"Archivo {file_path} no encontrado.")
    return loaded_text

def optimize_preparation_with_thermomix(preparation_text):
    prompt = (
        "Tienes el siguiente texto de preparación:\n\n"
        f"{preparation_text}\n\n"
        "0. Primero limpia el texto de la preparacion suprimiendo texto como por ejemplo ""Si necesitas más ayuda, no dudes en decírmelo. Claro, aquí tienes el texto extraído de la imagen:""\n\n"
        "Tengo 1 thermomix y su pelador de legumbres que permite de pelar rapidamente, solo como ejemplo las patatas, zanahorias, ajos, ... \n\n"
        "1. Quiero que mires la lista de ingredientes y me hagas un primer paso previo con los ingredientes que se tengan que pelar para hacerlo directamente. \n\n"
        "2. Dame los ingredientes que haya que picar.\n\n"
        "3. Dime tambien los ingredientes que se tengan que cortar en cubos (solo por saberlo)\n\n"
        "4. Busca los 2 paso donde la thermomix se lo mas util posible en la receta. El primer paso de los 2 no tiene que necesitar calentar y el segundo si. Estos seran los 2 unicos pasos donde vas a hablar de la thermomix y donde vas a modificar los pasos originales dando la temperatura, velocidad y tiempo. \n\n"
        "5. Por ultimo, no quiero que me des explicaciones de tu razonamiento. quiero que me des todos los puntos la preparacion original incluyendo las adaptaciones hechas anteriormente. \n\n"
        "6. No quiero que traduzacas la receta al espanol. Dejala en frances. \n\n"
        f"7. Quiero que mantengas la structura dela preparacion dada : {preparation_text}. Puedes anadir en la etapa previa los ingrediente a pelar, picar y cortar en cubos"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )

    optimized_text = response.choices[0].message.content
    return optimized_text

def enhance_preparation_with_quantities(ingredients_text, preparation_text):
    prompt = (
        "Tienes los siguientes ingredientes con sus cantidades:\n\n"
        f"{ingredients_text}\n\n"
        "Y tienes estas instrucciones de preparación:\n\n"
        f"{preparation_text}\n\n"
        "Introduce las cantidades de los ingredientes en el texto de preparación. Ejemplo: 'agrega los tomates' sería 'agrega [500g de tomates]'. \n\n"
        "No quiero que traduzacas la receta al espanol. Dejala en frances. \n\n"
        f"Quiero que mantengas la structura dela preparacion dada : {preparation_text}. Puedes anadir en la etapa previa los ingrediente a pelar, picar y cortar en cubos"
        )

    response = client.chat.completions.create( 
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,

    )

    enhanced_text = response.choices[0].message.content
    return enhanced_text

def simplify_preparation_steps(preparation_text):
    prompt = (
        "Quiero facilitar un poco el seguimento de la receta :\n\n"
        f"{preparation_text}\n\n"
        "1. Me gusta seguir las recetas de thermomix porque dans indicaciones precisas y paso a paso. Intenta seguir su estilo y enumera las subtareas de cada paso de la receta \n\n."
        "2. Los terminos de cocina tecnicos como por ejemplo : Équeutez, Sofritte, émincir, Ôtez, ..., quiero que los expliques a continuacion de la palabra entre corchetes con un maximo 10 palabras lo que viene a decir indicado tamano y temperatura aproximada. por ejemplo Équeutez [Quitar las puntas] \n\n"
        "3. No quiero que traduzacas la receta al espanol. Dejala en frances. \n\n"
        f"4. Quiero que mantengas la structura dela preparacion dada : {preparation_text}. Puedes anadir en la etapa previa los ingrediente a pelar, picar y cortar en cubos"
    ) #NO OLVIDAR DATOS COMO EL TIEMPO O LA TEMPERATURA, NI SUBTAREAS
    # SI HE CORTADO EN DADOS UNA CEBOLLA PARA EL PUNTO 3? TENGO QUE INDICARLO EN EL PUNTO 3
    # NO UTILICES LA TERMOMIX EN SUSTITUTO DE UNA SARTEN O PARA FREIR
    # cUANDO SON TIEMPOS CORTOS CORRIGE EL TIEMPO QUE LA TERMOMIX TARDA EN CALENTAR Y SOBRE TODO CUANDO HAY MUCHA COMIDA
    # CADA VEZ QUE SE DICE CHAUFFER? HAY QUE INDICAR MAS O MENOS LA INTENSIDAD DEL FUEGO; LO MISMO CON LA TEMPERATURA DEL HORNO
    # EN DES OU PETIS DES
    # VERIFICAR QUE LA INFORMACION COINCIDE CON EL ORIGINAL
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )

    simplified_text = response.choices[0].message.content
    return simplified_text

def process_files_and_enhance(sections_prompts):
    loaded_text = load_generated_files(sections_prompts)
    if all(header in loaded_text for header in ["Menu", "Ingredientes", "Preparacion"]):
        
        optimized_preparation = optimize_preparation_with_thermomix(
            loaded_text["Preparacion"]
        )
        optimized_prep_path = "Optimized_Preparacion.txt"
        with open(optimized_prep_path, "w") as file:
            file.write(optimized_preparation)

        enhanced_preparation = enhance_preparation_with_quantities(
            loaded_text["Ingredientes"],
            optimized_preparation
        )
        enhanced_prep_path = "Enhanced_Preparacion.txt"
        with open(enhanced_prep_path, "w") as file:
            file.write(enhanced_preparation)            

        simplified_preparation = simplify_preparation_steps(enhanced_preparation)
        simplified_prep_path = "Simplified_Preparacion.txt"
        with open(simplified_prep_path, "w") as file:
            file.write(simplified_preparation)

        st.write(f"Texto de preparación simplificado guardado en {simplified_prep_path}")
        # Display the simplified preparation text in an editable text area
        editable_preparation = st.text_area("Editar el texto simplificado de preparación", simplified_preparation, height=300)

        # Button to save any modifications made by the user
        if st.button("Guardar cambios"):
            # Save the modified preparation text to a file
            modified_prep_path = "Modified_Simplified_Preparacion.txt"
            with open(modified_prep_path, "w") as file:
                file.write(editable_preparation)
            st.write(f"Cambios guardados en {modified_prep_path}")
    else:
        st.write("Asegúrese de que todos los archivos de texto estén disponibles para la mejora.")

def main():
    st.title("Subir Fotos en Streamlit")

    # Define the section prompts
    sections_prompts = {
        "Menu": "Piensa paso a paso. Me puedes extraer TODO el texto que hay en estas 2 imagenes?  El texto dice lo que se come durante 5 dias de la semana (lunes, martes, miercoles, jueves, viernes) y la preparacion adicional que hay que hacer.",
        "Ingredientes": "Me puedes extraer el texto que hay en esta imagen y sacarme todos los ingredientes ?",
        "Preparacion": "Me puedes extraer el texto que hay en esta imagen? El texto dice lo primero la preparacion preable, luego te da todos los paso a seguir, esta es la parte mas importante hay mas de 10 pasos y quiero extraer todo el texto de cada uno de los pasos. Por ultimo, te dice lo que hay que hacer cuando todo se ha terminado (si va a frigorifico, congelador,...). ",
    }

    # Sidebar section
    st.sidebar.title("Navegación")
    stage = st.sidebar.radio("Seleccione la etapa:", ("Cargar Imágenes", "Mejorar Preparación"))

    if stage == "Cargar Imágenes":
        for section in sections_prompts.keys():
            handle_file_upload(section, section, sections_prompts)
    elif stage == "Mejorar Preparación":
        if st.button("Mejorar el archivo de preparación con cantidades"):
            process_files_and_enhance(sections_prompts)

if __name__ == "__main__":
    main()
