"""Transformaciones técnicas; las políticas se leen de configuracion.json."""
import json
import re
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone, timedelta
from pathlib import Path

def cargar_reglas():
    return json.loads(Path(__file__).with_name('configuracion.json').read_text(encoding='utf-8'))

def leer_json(texto):
    def constante(valor):
        raise ValueError('Constante JSON no permitida: ' + valor)
    registros = json.loads(texto, parse_float=Decimal, parse_constant=constante)
    if not isinstance(registros, list):
        raise ValueError('La raíz del JSON debe ser una lista de transacciones.')
    return registros

def normalizar(registro, reglas):
    if not isinstance(registro, dict):
        raise ValueError('El registro debe ser un objeto JSON.')
    candidatas = [(nombre, f) for nombre, f in reglas['fuentes'].items() if f['id'] in registro]
    if len(candidatas) != 1:
        raise ValueError('Fuente desconocida o ambigua: revise los identificadores.')
    fuente, f = candidatas[0]
    necesarios = [f[k] for k in ('id','monto','fecha','estado')]
    if f['moneda']:
        necesarios.append(f['moneda'])
    for campo in necesarios:
        if campo not in registro or registro[campo] is None or str(registro[campo]).strip() == '':
            raise ValueError('Campo obligatorio ausente o vacío: ' + campo)
    identificador = registro[f['id']]
    if isinstance(identificador, bool) or not isinstance(identificador, (str, int)):
        raise ValueError('El identificador debe ser texto o entero.')
    valor = registro[f['monto']]
    if isinstance(valor, bool) or not isinstance(valor, (str, int, Decimal)):
        raise ValueError('Tipo de monto inválido.')
    texto = str(valor).strip()
    if f['moneda']:
        if not isinstance(registro[f['moneda']], str):
            raise ValueError('La moneda debe ser texto.')
        moneda = registro[f['moneda']].strip().upper()
    else:
        simbolos = [s for s in f['simbolos'] if texto.startswith(s)]
        if len(simbolos) != 1:
            raise ValueError('Símbolo de moneda ausente o desconocido.')
        simbolo = simbolos[0]
        moneda = f['simbolos'][simbolo]
        texto = texto[len(simbolo):].strip()
    separador = re.escape(f['decimal'])
    if not re.fullmatch(r'[+-]?\d+(?:' + separador + r'\d+)?', texto):
        raise ValueError('Monto inválido: no se admiten separadores de miles ni notación exponencial.')
    try:
        monto = Decimal(texto.replace(f['decimal'], '.')) / Decimal(f['divisor'])
    except (InvalidOperation, ZeroDivisionError):
        raise ValueError('No se pudo convertir el monto.')
    estado = reglas['estados'].get(str(registro[f['estado']]).strip().lower())
    if estado is None:
        raise ValueError('Estado desconocido: ' + str(registro[f['estado']]))
    fecha = registro[f['fecha']]
    if not isinstance(fecha, str):
        raise ValueError('La fecha debe ser texto.')
    try:
        fecha = datetime.fromisoformat(fecha.replace('Z','+00:00')) if f['formato']=='ISO8601' else datetime.strptime(fecha, f['formato'])
        if fecha.tzinfo is None:
            offset = reglas['zona_sin_offset']
            signo = 1 if offset[0]=='+' else -1
            fecha = fecha.replace(tzinfo=timezone(signo*timedelta(hours=int(offset[1:3]), minutes=int(offset[4:6]))))
    except (ValueError, TypeError):
        raise ValueError('Fecha inválida para el formato de la fuente.')
    return {'id':str(identificador).strip(), 'amount':monto, 'currency':moneda,
            'timestamp':fecha.astimezone(timezone.utc).isoformat(), 'status':estado, 'source':fuente}

def exportar_json(valor):
    # Decimal se emite como número JSON exacto, sin pasar por float.
    if isinstance(valor, Decimal):
        if not valor.is_finite():
            raise ValueError('Número no finito.')
        return format(valor, 'f')
    if isinstance(valor, dict):
        return '{' + ','.join(json.dumps(str(k),ensure_ascii=False)+':'+exportar_json(v) for k,v in valor.items()) + '}'
    if isinstance(valor, list):
        return '[' + ','.join(exportar_json(v) for v in valor) + ']'
    return json.dumps(valor,ensure_ascii=False,allow_nan=False)
