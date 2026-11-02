# Decisiones de diseño confirmadas por el estudiante
El estudiante aprobó los campos id, amount, currency, timestamp, status y source.
Las reglas se propusieron con apoyo de IA y fueron revisadas y aceptadas por el estudiante durante la conversación. A continuación se documenta la configuración adoptada.

- Fuente A: unidades decimales con punto. Fuente B: total en centavos (10050 → 100.50). Esta unidad es una decisión del proyecto: el ejemplo no la especifica.
- Fuente C: prefijo € → EUR o $ → USD; coma decimal; sin separadores de miles.
- USD y EUR soportadas; sin conversión de divisas.
- completed/OK/success → SUCCESS; failed/error → FAILED; pending/processing → PENDING. Estados desconocidos se separan.
- Fechas A: año-mes-día y hora; B: día/mes/año y hora; C: ISO 8601.
- Fechas sin zona: offset fijo -06:00 adoptado. Salida en UTC.
- Campos obligatorios no vacíos; ID texto o entero. Montos finitos estrictamente positivos. Cero y negativos rechazados según el criterio adoptado.
- Duplicados: misma fuente e ID; se conserva el primero válido y se separan los posteriores.
- Fuente ambigua, moneda desconocida, error de formato o dato incompleto: registro separado con motivo y original; no se elimina silenciosamente.
- Las métricas monetarias incluyen todos los estados válidos. No equivalen a cobros realizados.

