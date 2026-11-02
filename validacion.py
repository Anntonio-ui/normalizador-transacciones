from normalizacion import normalizar

def procesar(registros, reglas):
    validas, invalidas, vistos = [], [], set()
    for indice, original in enumerate(registros, 1):
        try:
            t = normalizar(original, reglas)
            if t['currency'] not in reglas['monedas']:
                raise ValueError('Moneda no soportada.')
            if t['amount'] == 0 and not reglas['permitir_cero']:
                raise ValueError('Monto cero no permitido.')
            if t['amount'] < 0 and not reglas['permitir_negativos']:
                raise ValueError('Monto negativo no permitido.')
            clave = (t['source'], t['id'])
            if clave in vistos and reglas['duplicados']=='rechazar_por_fuente_e_id':
                raise ValueError('Identificador duplicado dentro de la fuente.')
            vistos.add(clave)
            validas.append(t)
        except ValueError as error:
            invalidas.append({'fila':indice,'motivo':str(error),'original':original})
    return validas, invalidas
