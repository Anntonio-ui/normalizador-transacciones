# Nexo — Normalizador de transacciones
Proyecto Python local con interfaz Streamlit. Python 3.10 o superior.

## Windows / PowerShell
1. Extrae el ZIP completo y abre la carpeta normalizador_transacciones.
2. En esa carpeta abre PowerShell y ejecuta:
```powershell
code .
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
No es necesario activar el entorno. Abre la dirección local que indique Streamlit (normalmente http://localhost:8501). Para detenerlo pulsa Ctrl+C.

## Linux / macOS
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Pruebas
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Las pruebas del núcleo solo necesitan la biblioteca estándar.

## Demostración
1. Se carga automáticamente transacciones_mixtas.json: 15 procesadas, 5 válidas y 10 inválidas.
2. Explora los filtros; busca tx_001 y compara el original con el normalizado.
3. Consulta errores y descarga sus originales.
4. Métricas: SUCCESS 3, PENDING 1, FAILED 1. USD 201.30 y EUR 99.99 (no sumarlos entre sí).
5. Carga datos/transacciones_validas.json y después datos/vacio.json.
6. Para comprobar el manejo de JSON malformado, copia datos/json_malformado.txt a un archivo con extensión .json y cárgalo.
7. Descarga resultados y métricas.

## Decisiones y uso de IA
Lee DECISIONES.md y nota_tecnica.md. El estudiante revisó y confirmó el esquema y las reglas propuestas con apoyo de IA. La documentación registra el uso real de IA y las verificaciones realizadas.
Los cambios de configuración se leen al volver a ejecutar la interfaz. Mantén las claves y tipos del archivo.
El sistema no requiere base de datos ni servicios externos. Los archivos se procesan en memoria durante la sesión y no se guardan automáticamente en disco.
