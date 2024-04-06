cara_opuesta = {
        0: 5,
        1: 3,
        2: 4,
        3: 1,
        4: 2,
        5: 0
    }


def heuristica_manhattan(cubo) -> int:
    distancia = 0

    for num_cara, cara in enumerate(cubo.caras):
        for num_casilla, casilla in enumerate(cara.casillas):
            distancia += calc_distancia(casilla, (num_cara, num_casilla))

    return distancia  # Devuelve la distancia total calculada


def calc_distancia(casilla, pos_actual) -> int:
    if pos_actual[1] != casilla.posicionCorrecta and pos_actual[1] != 8:
        dist_cara = 2  # Si la posición actual no es la correcta
    else:
        dist_cara = 0  # Si la posición actual es la correcta o el centro

    if pos_actual[0] != casilla.color:
        if pos_actual[0] == cara_opuesta[casilla.color]:
            dist_color = 6  # Si el color actual es el opuesto
        else:
            dist_color = 3  # Si el color actual no es el correcto ni el opuesto
    else:
        dist_color = 0

    return dist_cara + dist_color  # Devuelve la distancia calculada


def heuristica_comprueba_cara(cubo) -> int:
    casilla_en_cara = 0

    for num_cara, cara in enumerate(cubo.caras):
        for num_casilla, casilla in enumerate(cara.casillas):
            if num_casilla != 8:
                if num_cara != casilla.color:
                    casilla_en_cara += 1  # Solo tiene en cuenta la cara porque es muy optimista

    return casilla_en_cara  # Devuelve el nº de casillas que están en la cara correcta