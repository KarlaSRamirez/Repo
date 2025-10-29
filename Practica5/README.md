### Programación Lógica Funcional
### Práctica
# Resolución SLD (Selective Linear Definite-clause resolution) en Python
### Karla Sugey Ramirez Morales 
### 22760593

Dentro del archivo KB.py se encuentra la base de conocimiento de las recetas. Pero los hechos principales utilizados fueron los siguientes:
#### Alergenos
- ("alergeno", "cacahuates"),
- ("alergeno", "nueces"),
- ("alergeno", "almendras"),
- ("alergeno", "mariscos"),
- ("alergeno", "huevo"),
- ("alergeno", "leche"),
- ("alergeno", "soya"),
- ("alergeno", "gluten"),
- ("alergeno", "pescado"),

#### Hechos de ingredientes por receta
- ("incluye", "chilaquiles_verdes", "tortillas_de_maiz"),
- ("incluye", "chilaquiles_verdes", "cebolla"),
- ("incluye", "chilaquiles_verdes", "tomates_verdes"),
- ("incluye", "chilaquiles_verdes", "chiles_serranos"),
- ("incluye", "chilaquiles_verdes", "chiles_jalapenos"),
- ("incluye", "chilaquiles_verdes", "cebolla_blanca") ... Y así sucesivamente con todas las recetas.

### Reglas
Se tuvo que agregar dos nuevas reglas para que funcionara la resolución ya que una regla comprueba la presencia y la otra la ausencia.

#### Alergenos
- Si una receta incluye un ingrediente que es alérgeno, entonces la receta contiene alérgenos.
- Si una receta no contiene ningún alérgeno, entonces se considera que no contiene alérgenos.
#### Ingrediente que no quiere el usuario
- Una receta contiene un ingrediente a evitar si incluye alguno de los ingredientes que la persona desea evitar.
- Una receta no contiene ingredientes a evitar si ninguno de los ingredientes incluidos está en la lista de ingredientes prohibidos o no deseados.
