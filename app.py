from pathlib import Path
from datetime import datetime
import streamlit as st
from normalizacion import cargar_reglas, leer_json, exportar_json
from validacion import procesar
from metricas import calcular

st.set_page_config(page_title='Nexo · Transacciones', page_icon='💠', layout='wide')
st.markdown('<style>.stApp{background:linear-gradient(140deg,#080f20,#13243c)} [data-testid="stMetric"]{background:#152940;padding:18px;border-radius:15px;border:1px solid #254460} h1{color:#64d9e9}</style>',unsafe_allow_html=True)
st.caption('NEXO / EXPLORADOR DE DATOS')
st.title('Normalizador de transacciones')
st.write('Carga, transforma y explora transacciones de múltiples fuentes.')
reglas = cargar_reglas()
if reglas.get('revision_estudiante_pendiente'):
    st.warning('Modo demostración: el esquema fue aprobado; las reglas son propuestas de IA pendientes de revisión del estudiante. Consulta DECISIONES.md.')
archivo = st.sidebar.file_uploader('Cargar archivo JSON',type=['json'])
ejemplo = st.sidebar.selectbox('Datos de demostración',['transacciones_mixtas.json','transacciones_validas.json','vacio.json'])
try:
    texto = archivo.getvalue().decode('utf-8-sig') if archivo else (Path(__file__).parent/'datos'/ejemplo).read_text(encoding='utf-8')
    registros = leer_json(texto)
    validas, invalidas = procesar(registros, reglas)
except (ValueError, UnicodeError) as error:
    st.error('No se pudo leer el archivo: ' + str(error)); st.stop()
m = calcular(validas, invalidas)
for col, (etiqueta, clave) in zip(st.columns(3), [('Procesadas','procesadas'),('Válidas','validas'),('Inválidas','invalidas')]):
    col.metric(etiqueta,m[clave])
tabla, errores, metricas, reglas_tab = st.tabs(['Explorar','Inconsistencias','Métricas','Reglas'])
with tabla:
    st.caption('Los filtros afectan la tabla y su descarga. Las métricas globales abarcan todo el archivo.')
    buscar = st.text_input('Buscar identificador')
    c1,c2,c3 = st.columns(3)
    estados = c1.multiselect('Estado',sorted({t['status'] for t in validas}))
    monedas = c2.multiselect('Moneda',sorted({t['currency'] for t in validas}))
    fuentes = c3.multiselect('Fuente',sorted({t['source'] for t in validas}))
    fechas = st.date_input('Rango de fechas (UTC)', value=(), key='fechas')
    def coincide(t):
        dia = datetime.fromisoformat(t['timestamp']).date()
        return (buscar.lower() in t['id'].lower() and (not estados or t['status'] in estados)
            and (not monedas or t['currency'] in monedas) and (not fuentes or t['source'] in fuentes)
            and (not fechas or (len(fechas)==1 and dia==fechas[0]) or (len(fechas)==2 and fechas[0]<=dia<=fechas[1])))
    filtradas = [t for t in validas if coincide(t)]
    st.write(f'{len(filtradas)} de {len(validas)} transacciones válidas')
    st.dataframe([{**t,'amount':str(t['amount'])} for t in filtradas],use_container_width=True)
    st.download_button('Descargar resultados JSON',exportar_json(filtradas),'normalizadas.json','application/json')
    if registros:
        fila = st.selectbox('Comparar registro original y resultado',range(1,len(registros)+1))
        c1,c2 = st.columns(2)
        c1.code(exportar_json(registros[fila-1]),language='json')
        try:
            from normalizacion import normalizar
            # Solo se muestra como válido si superó también la validación del lote.
            error = next((e for e in invalidas if e['fila']==fila),None)
            if error: c2.error(error['motivo'])
            else: c2.code(exportar_json(normalizar(registros[fila-1],reglas)),language='json')
        except ValueError as error: c2.error(str(error))
with errores:
    st.write('Los registros inválidos se separan; el original se conserva para corrección.')
    st.dataframe([{'fila':e['fila'],'motivo':e['motivo'],'original':exportar_json(e['original'])} for e in invalidas],use_container_width=True)
    st.download_button('Descargar inconsistencias',exportar_json(invalidas),'inconsistencias.json','application/json')
with metricas:
    st.subheader('Conteo por estado · registros válidos')
    st.dataframe([{'estado':k,'cantidad':m['por_estado'].get(k,0)} for k in ['SUCCESS','FAILED','PENDING']])
    st.subheader('Totales por moneda · todos los estados válidos')
    st.dataframe([{'moneda':k,'total':str(v)} for k,v in m['por_moneda'].items()])
    st.caption('No se convierten divisas ni se suman monedas distintas. FAILED y PENDING también participan: son montos registrados, no ingresos cobrados.')
    st.download_button('Descargar métricas',exportar_json(m),'metricas.json','application/json')
with reglas_tab:
    st.json(reglas)
