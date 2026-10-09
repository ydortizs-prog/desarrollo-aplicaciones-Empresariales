# Justificación de Tipos de Campo por Modelo

## Modelo Exam

| Atributo | Tipo de Campo | Justificación |
|----------|---------------|---------------|
| `title` | `CharField(max_length=200)` | 1. **Longitud controlada**: El título de un examen no debería exceder 200 caracteres, garantizando consistencia en BD e interfaz. 2. **Índice eficiente**: CharField permite crear índices B-tree para búsquedas rápidas por título. 3. **Validación automática**: Django valida la longitud máxima a nivel de formulario y BD, previniendo datos corruptos. |
| `description` | `TextField()` | 1. **Texto sin límite fijo**: Las descripciones pueden variar desde unas pocas líneas a párrafos extensos; TextField no impone límite arbitrario. 2. **Almacenamiento optimizado**: En SQLite/PostgreSQL usa almacenamiento TOAST/overflow, eficiente para textos variables. 3. **Sin truncamiento silencioso**: A diferencia de CharField con max_length muy alto, TextField evita cortes inesperados. |
| `created_at` | `DateTimeField(auto_now_add=True)` | 1. **Timestamp inmutable**: `auto_now_add` fija la fecha al crear el registro, imposible de modificar después, garantizando auditoría. 2. **Zona horariaaware**: Con `USE_TZ=True` almacena en UTC, evitando problemas de zona horaria en despliegues globales. 3. **Ordenación natural**: Permite ordenar exámenes cronológicamente (`-created_at`) sin campo extra. |

---

## Modelo Question

| Atributo | Tipo de Campo | Justificación |
|----------|---------------|---------------|
| `statement` | `TextField()` | 1. **Enunciados variables**: Las preguntas pueden ser cortas o incluir contexto largo (casos, código, imágenes en base64). 2. **Búsqueda full-text**: TextField es compatible con índices GIN/TSVector en PostgreSQL para búsqueda textual avanzada. 3. **Separación semántica**: Distingue claramente el enunciado (texto libre) de metadatos (score, exam). |
| `score` | `IntegerField(default=10)` | 1. **Puntuación entera**: Los puntos en exámenes académicos son números enteros (1, 5, 10, 20), no requieren decimales. 2. **Rendimiento**: IntegerField usa 4 bytes vs 8 de FloatField; consultas de suma/agregación son más rápidas. 3. **Default seguro**: `default=10` asegura que preguntas existentes y nuevas tengan valor válido sin migración de datos compleja. |
| `exam` | `ForeignKey(Exam, on_delete=CASCADE, related_name="questions")` | 1. **Integridad referencial**: CASCADE elimina preguntas si se borra el examen, evitando huérfanos. 2. **Acceso inverso eficiente**: `related_name="questions"` permite `exam.questions.all()` sin joins manuales. 3. **Normalización 3FN**: Separa entidad Examen de Pregunta, reduciendo redundancia y permitiendo reutilizar preguntas (futuro). |

---

## Modelo Choice

| Atributo | Tipo de Campo | Justificación |
|----------|---------------|---------------|
| `text` | `CharField(max_length=200)` | 1. **Opciones concisas**: Las respuestas múltiples suelen ser frases cortas (<200 chars); límite evita respuestas tipo ensayo. 2. **Índice para búsqueda**: CharField indexable permite filtrar opciones por texto (ej. buscar "ninguna de las anteriores"). 3. **Consistencia UX**: Longitud uniforme mejora renderizado en plantillas y móvil. |
| `is_correct` | `BooleanField(default=False)` | 1. **Semántica binaria**: Una opción es correcta o no; BooleanField mapea directamente a BIT/BOOLEAN en BD. 2. **Validación a nivel BD**: `default=False` asegura que opciones nuevas sean incorrectas por defecto, forzando elección explícita. 3. **Consultas eficientes**: `filter(is_correct=True)` usa índice parcial en PostgreSQL, muy rápido para "opción correcta de cada pregunta". |
| `question` | `ForeignKey(Question, on_delete=CASCADE, related_name="choices")` | 1. **Cascada coherente**: Borrar pregunta elimina sus opciones, manteniendo consistencia. 2. **Acceso O(1) inverso**: `question.choices.all()` evita subconsultas; Django hace JOIN implícito optimizado. 3. **Cardinalidad 1:N natural**: Cada opción pertenece a una sola pregunta; FK en Choice es el patrón relacional estándar. |

---

## Resumen de Decisiones Transversales

- **Nombres en inglés** (title, description, score, is_correct): Cumple norma del proyecto y facilita i18n futura.
- **verbose_name en inglés**: Coherente con código; las etiquetas de UI se traducen en plantillas/forms.
- **related_name plural** (questions, choices): API intuitiva `exam.questions`, `question.choices`.
- **auto_now_add en created_at**: Inmutabilidad garantizada sin lógica extra en vistas/serializers.
- **default en score e is_correct**: Evita NOT NULL constraint errors y da comportamiento predecible.