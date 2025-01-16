from typing import Optional
from dataclasses import dataclass

def prompts(textsImages, transformation):

    @dataclass
    class ListeIngredient:
        Ingredient: str
        Quantite : Optional[int] = None
        Unite : Optional[str] = None
        note: Optional[str] = None
    
    # etaps = ["Menu", "Ingredientes", "Preparacion"]
    transformaciones = { 
        "Menu": (
            "From the image attached of an invoice extract all the data and format it as a JSON object. Try to include all the fields that you get from the invoice. \n\n"
            "El texto dice lo que se come durante 5 dias de la semana (lunes, martes, miercoles, jueves, viernes) y la preparacion adicional que hay que hacer.  \n\n"
        ),

        "Ingredientes": (
            "Contexte : Extraction de données d'une image contenant des informations de liste de courses pour une recette. \n\n"
            "Instruction de prompt : À partir de l'image jointe contenant une liste d'ingrédients pour une recette, identifiez et extrayez toutes les données possibles (Ingredient, Quantite, Unite,  note). Formatez les résultats sous forme d'une liste d'objets JSON, en respectant la structure suivante pour chaque ingrédient :  \n\n"
            "Veuillez structurer la sortie JSON pour correspondre à la classe suivante : \n\n"
            "@dataclass class ListeIngredient: Ingredient: str, Quantite : Optional[int] = None, Unite : Optional[str] = None, note: Optional[str] = None \n\n"
            "Par exemple, ce texte : - 1 bûche ou un crottin de chèvre frais (environ 150 g), \n\n"
            "je veux qu'il soit transformé comme ça : {'Ingredient': 'bûche ou un crottin de chèvre frais', 'Quantite : 1, 'Unite': '', 'note': 'environ 150 g'} \n\n"
            "ou encore : - 1,5 kg d'aubergines fermes \n\n"
        ),

        "Preparacion": (
            "Me puedes extraer el texto que hay en esta imagen? El texto dice lo primero la preparacion preable, luego te da todos los paso a seguir, esta es la parte mas importante hay mas de 10 pasos y quiero extraer todo el texto de cada uno de los pasos. Por ultimo, te dice lo que hay que hacer cuando todo se ha terminado (si va a frigorifico, congelador,...). "
        ),

        "pOIngredientesAlternativos": (
            "Eres un experto cocinero en thermomix  \n\n"
            f"Tengo que hacer el menu siguiente : {textsImages['Menu']}  \n\n"
            f"Para ello tengo que comprar los ingredientes siguiente : {textsImages['Menu']} \n\n"
            "A veces, en la lista de ingredientes aparecen ciertos ingredientes que no conozco o que no encuentro en el supermercado. \n\n"
            "Como ejemplo : Chapelure, tandoori, linguines, millet, crottin\n\n"
            "1. Quiero que mires la lista de ingredientes y me identifiques los ingredientes raros y que me propongas una alternativa mas comun adaptada al menu."    
        ),

        "p1AdaptacionThermomix": (
            "Eres un experto cocinero en thermomix  \n\n"
            f"Tienes el siguiente texto de preparación: {textsImages['UltimaPreparacion']} \n\n"
            "0. Primero limpia el texto de la preparacion suprimiendo texto como por ejemplo : 'Si necesitas más ayuda, no dudes en decírmelo. Claro, aquí tienes el texto extraído de la imagen', 'Tengo 1 thermomix y su pelador de legumbres que permite de pelar rapidamente, solo como ejemplo las patatas, zanahorias, ajos, ...' \n\n"
            "1. Quiero que mires la lista de ingredientes y me hagas un primer paso previo  'Preparacion Con Thermomix' con los ingredientes que se tengan que pelar para hacerlo directamente. \n\n"
            "2. Dame los ingredientes que haya que picar y los pasos donde se utiliza. Por ejemplo, si tengo que cortar en dados o en pequenos dados la cebolla para el paso 3 quiero que lo indique en el paso 3 y en la 'Preparacion Con Thermomix'.  \n\n"
            "3. Dime también los ingredientes que se tengan que cortar en cubos (solo por saberlo). Por ejemplo, si tengo que cortar en dados pequenos dados la cebolla para el paso 3 quiero que lo indique en el paso 3 y en la 'Preparacion Con Thermomix'.\n\n"
            "4. Busca los 3 pasos donde la thermomix sea lo más útil posible en la receta (no quiero que utilices la thermomix en sustituto de una sarten para freir). El segundo paso de los 3 no tiene que necesitar calentar pero el primero o el tercero puede necesitar calentar (o no). Estos serán los 3 únicos pasos donde vas a hablar de la thermomix y donde vas a modificar los pasos originales dando la temperatura, velocidad y tiempo. Piensa bien el tiempo de cocinado con la thermomix porque cuando los tiempos son cortos, la thermomix puede tardar mas tiempo en subir de temperatura, tenlo en cuenta.\n\n"
            "5. Por último, no quiero que me des explicaciones de tu razonamiento. Quiero que me des todos los puntos de la preparacion original incluyendo las adaptaciones hechas anteriormente. \n\n"
            "6. No quiero que traduzcas la receta al español. Déjala en francés. \n\n"
            "7. Quiero que mantengas la estructura de la preparación dada : 'Au prealable', 'Preparacion Con Thermomix', 'Cest parti pour 2 h de cuisine' y 'Tout est prêt ! Laissez refroidir'."
        ),

# enumerar los ingredientes que tengo que sacar unicamente
# Badigeonnez ?
        "p2RecordarCantidades": (
            "Eres un experto cocinero en thermomix  \n\n"
            "Tienes los siguientes ingredientes con sus cantidades:\n\n"
            f"{textsImages['Ingredientes']}\n\n"
            "Y tienes estas instrucciones de preparación:\n\n"
            f"{textsImages['UltimaPreparacion']}\n\n"
            "Introduce las cantidades de los ingredientes en el texto de preparación. Ejemplo: 'agrega los tomates' sería 'agrega [500g de tomates]'. \n\n"
            "No quiero que traduzacas la receta al espanol. Dejala en frances. \n\n"
            "Quiero que mantengas la estructura de la preparación dada : 'Au prealable', 'Preparacion Con Thermomix (pelar, picar, ...)', 'Cest parti pour 2 h de cuisine' y 'Tout est prêt ! Laissez refroidir'."
        ),

        "p3SimplificarPreparacion": (
            "Eres un experto cocinero en thermomix  \n\n"
            "Quiero facilitar un poco el seguimento de la receta :\n\n"
            f"{textsImages['UltimaPreparacion']}\n\n"
            "1. Me gusta seguir las recetas de thermomix porque dans indicaciones precisas y paso a paso. Intenta seguir su estilo y enumera las subtareas de cada paso de la receta. Puedes simplificar, pero ten cuidado de no olvidar ninguna etapa, ni subtarea, ni paso, ni temperatua, ni tiempo. Y verifica que la informacion coincida con la original. \n\n."
            "2. Los terminos de cocina tecnicos. Quiero que los expliques a continuacion de la palabra entre corchetes con un maximo 5 palabras lo que viene a decir indicado tamano y temperatura aproximada. Por ejemplo : Équeutez [quitar puntas], émincir [Couper en fines tranches] ..., \n\n"
            "3. Quiero que cada vez que se haga referencia a calentar la sarten, cacerola, horno o thermomix que se indique una intensidad orientativa si no esta indicado (fuego bajo, medio o alto). \n\n"
            "4. No quiero que traduzacas la receta al espanol. Dejala en frances. \n\n"
            "5. Quiero que mantengas la estructura de la preparación dada : 'Au prealable', 'Preparacion Con Thermomix (pelar, picar, ...)', 'Cest parti pour 2 h de cuisine' y 'Tout est prêt ! Laissez refroidir'."
            )
    }
    return transformaciones[transformation]
    
    
