"""Exercise the quiz API over HTTP and print every status code.

Run the development server first, then: python api_smoke.py
"""
import base64
import json
import urllib.error
import urllib.request

BASE = 'http://127.0.0.1:8000/api'
AUTH = 'Basic ' + base64.b64encode(b'admin:admin123').decode()
JSON = {'Content-Type': 'application/json'}


def call(method, path, payload=None, auth=True, raw=None):
    body = None
    if raw is not None:
        body = raw.encode()
    elif payload is not None:
        body = json.dumps(payload).encode()
    headers = {'Accept': 'application/json', **JSON}
    if auth:
        headers['Authorization'] = AUTH
    request = urllib.request.Request(BASE + path, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode()
            return response.status, text
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


def show(label, status, text, limit=220):
    print(f'{label}: {status}')
    print('  ' + text[:limit].replace('\n', ' '))


# 1. List
status, text = call('GET', '/exams/')
show('GET /exams/', status, text)

# 2. Detail
status, text = call('GET', '/exams/5/')
show('GET /exams/5/', status, text)

# 3. Create exam
status, text = call('POST', '/exams/', {'title': 'Examen creado por API', 'description': 'Creado con JSON.'})
show('POST /exams/', status, text)
created_id = json.loads(text)['id'] if status == 201 else None

# 4. Partial update
status, text = call('PATCH', f'/exams/{created_id}/', {'description': 'Descripción modificada.'})
show(f'PATCH /exams/{created_id}/', status, text)

# Create a question with nested choices
question_payload = {
    'statement': '¿Qué método HTTP elimina un recurso?',
    'score': 10,
    'exam': 5,
    'choices': [
        {'text': 'DELETE', 'is_correct': True},
        {'text': 'GET', 'is_correct': False},
        {'text': 'POST', 'is_correct': False},
    ],
}
status, text = call('POST', '/questions/', question_payload)
show('POST /questions/ (nested choices)', status, text)
question_id = json.loads(text)['id'] if status == 201 else None

# 5. Delete the created question and the created exam
if question_id:
    status, text = call('DELETE', f'/questions/{question_id}/')
    print(f'DELETE /questions/{question_id}/: {status}')
if created_id:
    status, text = call('DELETE', f'/exams/{created_id}/')
    print(f'DELETE /exams/{created_id}/: {status}')

# Filters and pagination
status, text = call('GET', '/questions/?exam=5')
show('GET /questions/?exam=5', status, text)
status, text = call('GET', '/questions/?search=serializador')
show('GET /questions/?search=serializador', status, text)
status, text = call('GET', '/questions/?page=1')
data = json.loads(text)
print(f'GET /questions/?page=1: {status} | count={data.get("count")} next={data.get("next")}')
status, text = call('GET', '/questions/?page=2')
data = json.loads(text)
print(f'GET /questions/?page=2: {status} | results={len(data.get("results", []))} previous={data.get("previous")}')

print('\n--- Intentional errors ---')
# Missing required field
status, text = call('POST', '/exams/', {'description': 'Sin título.'})
show('POST /exams/ (missing title)', status, text)
# Wrong type
status, text = call('POST', '/questions/', {
    'statement': 'Pregunta con score inválido',
    'score': 'diez',
    'exam': 5,
    'choices': [{'text': 'A', 'is_correct': True}, {'text': 'B', 'is_correct': False}],
})
show('POST /questions/ (score wrong type)', status, text)
# Wrong number of correct choices
status, text = call('POST', '/questions/', {
    'statement': 'Pregunta con dos respuestas correctas',
    'score': 10,
    'exam': 5,
    'choices': [
        {'text': 'A', 'is_correct': True},
        {'text': 'B', 'is_correct': True},
        {'text': 'C', 'is_correct': False},
    ],
})
show('POST /questions/ (two correct choices)', status, text)

# Write without credentials must be rejected
status, text = call('POST', '/exams/', {'title': 'Sin credenciales', 'description': 'x'}, auth=False)
show('POST /exams/ (anonymous)', status, text)
