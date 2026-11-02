# Nota técnica — Normalizador de transacciones
**Estudiante:** William Antonio Hernández Iraheta

El sistema usa Python y Streamlit para cargar archivos JSON y explorar sus transacciones mediante filtros por identificador, estado, moneda, fuente y fecha. El esquema elegido contiene id, amount, currency, timestamp, status y source. Normalización, validación, métricas e interfaz están separadas para facilitar su mantenimiento.

Las fuentes se detectan por sus identificadores característicos. La fuente A contiene montos en unidades, la B se interpreta en centavos (10050 equivale a 100.50) y la C usa un símbolo monetario y coma decimal. La unidad de B es una decisión de este proyecto, pues el enunciado no la especifica. Se admiten USD y EUR sin convertir divisas. Los estados completed/OK/success se unifican como SUCCESS; failed/error como FAILED; pending/processing como PENDING.

Se reconocen los formatos de fecha de las tres fuentes. Las fechas sin zona se interpretan con offset -06:00 y se exportan en UTC con formato ISO 8601. Se usa Decimal para los montos, evitando la representación binaria de float en las conversiones y exportaciones.

Se exigen campos completos y montos mayores que cero. Los ceros, negativos, monedas o estados desconocidos y formatos inválidos se separan con motivo y original para permitir su corrección. Para duplicados de la misma fuente e identificador se conserva el primer registro válido. Las métricas cuentan registros válidos por estado y suman sus montos por moneda, incluyendo todos los estados; estos totales no representan necesariamente ingresos cobrados.

**Uso de IA y revisión:** ChatGPT apoyó la estructura, implementación, interfaz y pruebas, y propuso reglas iniciales. El estudiante revisó las reglas y decidió mantenerlas; no realizó cambios en su lógica. Tras esa revisión se actualizó la documentación y se desactivó el indicador de revisión pendiente. No se atribuyen al estudiante cambios de código que no realizó.

**Validación:** pasaron siete pruebas automatizadas del núcleo y comprobaciones de inicio, filtro y archivo vacío en Streamlit. El estudiante verificó en su equipo las inconsistencias, las métricas y la carga de un JSON válido (5 procesadas, 5 válidas y 0 inválidas).
