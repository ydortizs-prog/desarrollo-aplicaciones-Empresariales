# Entregable — Implementación de Servicios Web con Django (DRF)

Laboratorio sobre el proyecto de cuestionarios (`quiz`). La API expone exámenes,
preguntas y opciones con Django REST Framework, paginación, filtrado y búsqueda.

## 1. Configuración

`djangorestframework` y `django-filter` se instalaron en el entorno virtual y se
declararon en `INSTALLED_APPS` (`config/settings.py`), junto a la aplicación `quiz`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
    'quiz',
    ...
]
```

Bloque de configuración por defecto:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

Con `IsAuthenticatedOrReadOnly` cualquiera puede **leer** la API, pero para
**crear, modificar o eliminar** hay que autenticarse (sesión del admin o Basic
auth). Sin credenciales, una escritura responde `403`.

## 2. Serializadores y relaciones

Archivo `quiz/serializers.py`, todos derivados de `ModelSerializer`.

| Serializador | Campos | Solo lectura |
|---|---|---|
| `ExamSerializer` | `id`, `title`, `description`, `created_at`, `questions_count` | `id`, `created_at`, `questions_count` |
| `QuestionSerializer` | `id`, `statement`, `score`, `exam`, `choices` | `id` |
| `NestedChoiceSerializer` | `id`, `text`, `is_correct` | `id` |
| `ChoiceSerializer` | `id`, `text`, `is_correct`, `question` | `id` |

Decisiones sobre las relaciones:

- **Opciones anidadas dentro de la pregunta**: `QuestionSerializer.choices` usa
  `NestedChoiceSerializer(many=True)`. Al crear o modificar una pregunta se envían
  sus opciones en el mismo cuerpo JSON. En la actualización se reemplaza el
  conjunto de opciones (se borran las anteriores y se crean las nuevas) dentro de
  una transacción.
- **Examen referido por identificador**: en `QuestionSerializer` el campo `exam`
  es la clave foránea y viaja como `id` (no se anida el examen completo).
- **Opción suelta**: `ChoiceSerializer` expone `question` como identificador para
  poder gestionar opciones desde su propio recurso.

Validación propia de la pregunta (`QuestionSerializer.validate`): se cuentan las
opciones con `is_correct=True` y se exige **exactamente una**. También se piden al
menos dos opciones. Si el conteo es distinto de uno, la API responde `400`.

## 3. Rutas

`quiz/api_views.py` define tres `ModelViewSet`:

- `ExamViewSet`: búsqueda por `title` y `description`, orden por `title`/`created_at`.
- `QuestionViewSet`: `filterset_fields = ['exam']`, `search_fields = ['statement']`,
  orden por `id`/`score`; consulta optimizada con `select_related('exam')` y
  `prefetch_related('choices')`.
- `ChoiceViewSet`: filtros `question` e `is_correct`, búsqueda por `text`.

`quiz/api_urls.py` los registra en un `DefaultRouter` y `config/urls.py` incluye
ese enrutador bajo `api/`:

```python
router = DefaultRouter()
router.register('exams', ExamViewSet, basename='exam')
router.register('questions', QuestionViewSet, basename='question')
router.register('choices', ChoiceViewSet, basename='choice')

# config/urls.py
path('api/', include('quiz.api_urls')),
```

Raíz navegable: `http://127.0.0.1:8000/api/`.

## 4. Tabla de la API

Prefijo: `http://127.0.0.1:8000/api`.

| Recurso | Dirección | Método | Cuerpo de ejemplo | Respuesta esperada |
|---|---|---|---|---|
| Exámenes | `/exams/` | GET | — | `200` lista paginada (`count`, `next`, `previous`, `results`) |
| Exámenes | `/exams/{id}/` | GET | — | `200` objeto con `questions_count` |
| Exámenes | `/exams/` | POST | `{"title": "Examen creado por API", "description": "Creado con JSON."}` | `201` objeto creado con `id` |
| Exámenes | `/exams/{id}/` | PUT | `{"title": "Nuevo título", "description": "Nueva descripción."}` | `200` objeto actualizado |
| Exámenes | `/exams/{id}/` | PATCH | `{"description": "Descripción modificada."}` | `200` objeto actualizado |
| Exámenes | `/exams/{id}/` | DELETE | — | `204` sin cuerpo |
| Preguntas | `/questions/` | GET | — | `200` lista paginada con opciones anidadas |
| Preguntas | `/questions/?exam=5` | GET | — | `200` solo preguntas del examen 5 |
| Preguntas | `/questions/?search=serializador` | GET | — | `200` preguntas cuyo enunciado contiene el texto |
| Preguntas | `/questions/{id}/` | GET | — | `200` pregunta con `choices` |
| Preguntas | `/questions/` | POST | `{"statement": "¿Qué método HTTP elimina un recurso?", "score": 10, "exam": 5, "choices": [{"text": "DELETE", "is_correct": true}, {"text": "GET", "is_correct": false}, {"text": "POST", "is_correct": false}]}` | `201` pregunta con sus opciones creadas |
| Preguntas | `/questions/{id}/` | PATCH | `{"score": 20}` | `200` pregunta actualizada |
| Preguntas | `/questions/{id}/` | DELETE | — | `204` sin cuerpo |
| Opciones | `/choices/` | GET | — | `200` lista paginada |
| Opciones | `/choices/?question=5` | GET | — | `200` opciones de la pregunta 5 |
| Opciones | `/choices/{id}/` | GET | — | `200` opción con `question` |
| Opciones | `/choices/` | POST | `{"text": "DELETE", "is_correct": true, "question": 5}` | `201` opción creada |
| Opciones | `/choices/{id}/` | PATCH | `{"text": "DELETE método"}` | `200` opción actualizada |
| Opciones | `/choices/{id}/` | DELETE | — | `204` sin cuerpo |

## 5. Recorrido desde la API navegable

Con sesión iniciada en `/admin/login/` (usuario `admin`) la API muestra los
formularios de escritura. En preguntas, el formulario HTML no admite listas
anidadas, por lo que se usa la pestaña **Raw data** (JSON).

| Operación | Dirección | Código |
|---|---|---|
| Listar exámenes | `GET /api/exams/` | `200` |
| Ver detalle de examen | `GET /api/exams/{id}/` | `200` |
| Crear examen | `POST /api/exams/` | `201` |
| Ver detalle del examen creado | `GET /api/exams/{id}/` | `200` |
| Modificar parcialmente | `PATCH /api/exams/{id}/` | `200` |
| Crear pregunta con opciones | `POST /api/questions/` | `201` |
| Ver detalle de pregunta | `GET /api/questions/{id}/` | `200` |
| Modificar parcialmente pregunta | `PATCH /api/questions/{id}/` | `200` |
| Eliminar pregunta | `DELETE /api/questions/{id}/` | `204` |
| Eliminar examen | `DELETE /api/exams/{id}/` | `204` |

Los identificadores concretos cambian en cada ejecución; lo relevante es el código
de estado, que se mantiene.

## 6. Recorrido desde un cliente HTTP externo

Script `api_smoke.py` (autenticación Basic con `admin:admin123`, cuerpo JSON):

| Operación | Dirección | Código observado |
|---|---|---|
| Listar | `GET /api/exams/` | `200` |
| Detalle | `GET /api/exams/{id}/` | `200` |
| Crear | `POST /api/exams/` | `201` |
| Modificar parcialmente | `PATCH /api/exams/{id}/` | `200` |
| Crear pregunta anidada | `POST /api/questions/` | `201` |
| Eliminar pregunta | `DELETE /api/questions/{id}/` | `204` |
| Eliminar examen | `DELETE /api/exams/{id}/` | `204` |

Los códigos coinciden con los de la API navegable.

## 7. Errores provocados a propósito

| Error | Petición | Mensaje de la API | Código |
|---|---|---|---|
| Campo obligatorio ausente | `POST /api/exams/` con `{"description": "Sin título."}` | `{"title": ["This field is required."]}` | `400` |
| Tipo incorrecto | `POST /api/questions/` con `"score": "diez"` | `{"score": ["A valid integer is required."]}` | `400` |
| Número de correctas distinto de uno | `POST /api/questions/` con dos opciones `is_correct: true` | `{"choices": ["A question must have exactly one correct choice."]}` | `400` |
| Escritura sin credenciales | `POST /api/exams/` sin autenticación | `{"detail": "Authentication credentials were not provided."}` | `403` |

## 8. Filtrado, búsqueda y paginación

- Filtrado por examen: `GET /api/questions/?exam=5` → `200`, `count = 6`.
- Búsqueda por enunciado: `GET /api/questions/?search=serializador` → `200`,
  `count = 1` (la pregunta "¿Qué clase base usa un serializador de modelo?").
- Paginación (`PAGE_SIZE = 5`): con 8 preguntas,
  - `GET /api/questions/?page=1` → `200`, `count = 8`, `next` apunta a `page=2`.
  - `GET /api/questions/?page=2` → `200`, 3 resultados, `previous` presente.

## 9. Pruebas automatizadas

`quiz/tests_api.py` cubre los cinco verbos, la validación de la opción correcta,
los errores de campo y tipo, los filtros, la búsqueda, la paginación y el permiso
de escritura. Se ejecutan con:

```powershell
python manage.py test quiz.tests_api
```

Resultado: **7 pruebas, todas OK**.

## 10. Cómo ejecutar el proyecto

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python seed_api.py        # datos de ejemplo: examen con 6 preguntas
python manage.py runserver
```

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/` (`admin` / `admin123`)
- Scripts de comprobación: `api_smoke.py` (cliente externo) y
  `api_browse_session.py` (sesión de la API navegable).

## 11. Nota sobre el diseño

Se eligió anidar las opciones en la pregunta porque siempre se crean y se leen
junto a ella, y referir el examen por `id` porque es un recurso independiente que
puede compartirse entre muchas preguntas. Así se evita duplicar el examen en cada
respuesta y se mantiene una única ruta para consultarlo o modificarlo.
