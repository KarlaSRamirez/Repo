# sld_practice.py
from KB import HECHOS, REGLAS_ALERGENOS, REGLAS_INGREDIENTES_EVITAR


# Esta funcion es especifica para la unificacion
def unificar(x, y, sustitucion=None):
    """
    Se podía usar una pila de pares por unificar: stack = [(x, y)]
    Mientras stack no sea vacío:
        a, b = stack.pop()
        si a == b entonces continuar
        si a es variable entonces aplicar/actualizar sustitucion
        si b es variable entonces idem
        si ambos son tuplas y misma cabeza y también longitud:
            for i in range(1, len(a)):
                stack.append((a[i], b[i]))
        sino: fallo -> devolver None
    Si es que se completa sin fallos se va a devolver sustitucion
    """
    if sustitucion is None:
        sustitucion = {}
    if x == y:
        return sustitucion
    if isinstance(x, str) and x.isupper():
        return unificar_variable(x, y, sustitucion)
    if isinstance(y, str) and y.isupper():
        return unificar_variable(y, x, sustitucion)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return None
        for a, b in zip(x[1:], y[1:]):
            sustitucion = unificar(a, b, sustitucion)
            if sustitucion is None:
                return None
        return sustitucion
    return None

def unificar_variable(var, valor, sustitucion):
    if var in sustitucion:
        return unificar(sustitucion[var], valor, sustitucion)
    nueva = sustitucion.copy()
    nueva[var] = valor
    return nueva

def aplicar_sustitucion(meta, sustitucion):
    if isinstance(meta, tuple):
        return tuple(aplicar_sustitucion(arg, sustitucion) for arg in meta)
    if isinstance(meta, list):
        return [aplicar_sustitucion(arg, sustitucion) for arg in meta]
    if isinstance(meta, dict):
        return {k: aplicar_sustitucion(v, sustitucion) for k, v in meta.items()}
    elif isinstance(meta, str) and meta in sustitucion:
        return sustitucion[meta]
    else:
        return meta

def contiene_algun_alergeno(receta, alergenos):
    #Verifica si una receta contiene alguno de los alérgenos especificados
    ingredientes = obtener_ingredientes(receta)
    if isinstance(alergenos, (str,)):
        alergenos = [alergenos]
    al_set = set(alergenos)
    for ing in ingredientes:
        if ing in al_set and ("alergeno", ing) in HECHOS:
            return True
    return False

def contiene_algun_ingrediente(receta, ingredientes_evitar):
    #Verifica si una receta contiene alguno de los ingredientes a evitar
    ingredientes = obtener_ingredientes(receta)
    if isinstance(ingredientes_evitar, (str,)):
        ingredientes_evitar = [ingredientes_evitar]
    ev_set = set(ingredientes_evitar)
    return any(ing in ev_set for ing in ingredientes)

def resolver_sld(metas, hechos, reglas, sustitucion=None):
    if sustitucion is None:
        sustitucion = {}
    if not metas:
        return [sustitucion]
    
    meta_actual = metas[0]
    resto_metas = metas[1:]
    resultados = []

    # Manejo de negación
    if isinstance(meta_actual, tuple) and len(meta_actual) > 0 and meta_actual[0] == "not":
        meta_negada = meta_actual[1]
        if not resolver_sld([meta_negada], hechos, reglas, sustitucion):
            return resolver_sld(resto_metas, hechos, reglas, sustitucion)
        return []

    # Unificación con hechos
    for hecho in hechos:
        sigma = unificar(meta_actual, hecho, sustitucion)
        if sigma is not None:
            nuevas_metas = [aplicar_sustitucion(m, sigma) for m in resto_metas]
            resultados.extend(resolver_sld(nuevas_metas, hechos, reglas, sigma))

    # Unificación con reglas
    for cabeza, cuerpo in reglas:
        sigma = unificar(meta_actual, cabeza, sustitucion)
        if sigma is not None:
            nuevas_metas = [aplicar_sustitucion(m, sigma) for m in cuerpo + resto_metas]
            resultados.extend(resolver_sld(nuevas_metas, hechos, reglas, sigma))

    return resultados

def obtener_ingredientes(receta):
    # Obtiene todos los ingredientes de una receta
    ingredientes = set()
    for hecho in HECHOS:
        if isinstance(hecho, tuple) and len(hecho) >= 3 and hecho[0] == "incluye" and hecho[1] == receta:
            ingredientes.add(hecho[2])
    return list(ingredientes)

def obtener_todas_recetas():
    # Obtiene todas las recetas de manera segura
    recetas = set()
    for hecho in HECHOS:
        if len(hecho) >= 2 and hecho[0] == "incluye":
            recetas.add(hecho[1])
    return list(recetas)

def query_regla_alergenos():
    print("QUERY 1: Recetas que NO contienen alérgenos seleccionados")
    print("Alérgenos a evitar: ['cacahuates', 'nueces']")
    print("-" * 50)
    
    todas_recetas = obtener_todas_recetas()
    recetas_validas = []
    
    for receta in todas_recetas:
        # Usamos una variable en lugar de la lista directamente
        consulta = ("no_contiene_alergenos", receta, "A")
        resultados = resolver_sld([consulta], HECHOS, REGLAS_ALERGENOS)
        if resultados:
            recetas_validas.append(receta)
    
    for receta in recetas_validas:
        print(f"{receta}")
    return recetas_validas

def query_regla_ingredientes():
    print( "\nQUERY 2: Recetas que NO contienen ingredientes a evitar")
    print("Ingredientes a evitar: ['chile_serrano', 'pescado_blanco']")
    print("-" * 50)
    
    todas_recetas = obtener_todas_recetas()
    recetas_validas = []
    
    ingredientes_evitar = ['chile_serrano', 'pescado_blanco']

    for receta in todas_recetas:
        # Comprobamos si la receta contiene ALGUNO de los ingredientes a evitar
        contiene_prohibido = any(
            resolver_sld(
                [("contiene_algun_ingrediente", receta, ingr)],
                HECHOS,
                REGLAS_INGREDIENTES_EVITAR
            )
            for ingr in ingredientes_evitar
        )

        # Si no contiene ninguno → la receta es válida
        if not contiene_prohibido:
            recetas_validas.append(receta)

    for receta in recetas_validas:
        print(f"{receta}")
    return recetas_validas

if __name__ == "__main__":    
    # Query 1: Regla de alérgenos
    resultado1 = query_regla_alergenos()
    
    # Query 2: Regla de ingredientes a evitar
    resultado2 = query_regla_ingredientes()
