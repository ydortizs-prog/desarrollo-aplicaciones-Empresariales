"""Exercise the five operations through the browsable API session.

Logs in at /admin/login/ (the browsable API shares the session) and sends the
same JSON requests the "Raw data" tab sends from the browser.
"""
import http.cookiejar
import json
import re
import urllib.error
import urllib.parse
import urllib.request

BASE = 'http://127.0.0.1:8000'
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

login_page = opener.open(BASE + '/admin/login/').read().decode()
token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page).group(1)
form = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123',
    'csrfmiddlewaretoken': token,
    'next': '/api/',
}).encode()
opener.open(urllib.request.Request(BASE + '/admin/login/', data=form, headers={
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': BASE + '/admin/login/',
}))


def csrf():
    for cookie in jar:
        if cookie.name == 'csrftoken':
            return cookie.value
    return ''


def call(method, path, payload=None, accept='application/json'):
    headers = {'Accept': accept, 'X-CSRFToken': csrf(), 'Referer': BASE + path}
    data = None
    if payload is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(payload).encode()
    request = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with opener.open(request) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()


print('GET  /api/exams/          ->', call('GET', '/api/exams/', accept='text/html')[0])
print('GET  /api/exams/5/        ->', call('GET', '/api/exams/5/', accept='text/html')[0])

status, body = call('POST', '/api/exams/', {'title': 'Examen navegable', 'description': 'Desde la API navegable.'})
print('POST /api/exams/          ->', status)
exam_id = json.loads(body)['id']

print('GET  /api/exams/%s/       ->' % exam_id, call('GET', f'/api/exams/{exam_id}/', accept='text/html')[0])
print('PATCH /api/exams/%s/      ->' % exam_id,
      call('PATCH', f'/api/exams/{exam_id}/', {'description': 'Descripción cambiada.'})[0])

status, body = call('POST', '/api/questions/', {
    'statement': '¿Qué verbo HTTP crea un recurso?',
    'score': 10,
    'exam': exam_id,
    'choices': [
        {'text': 'POST', 'is_correct': True},
        {'text': 'GET', 'is_correct': False},
    ],
})
print('POST /api/questions/      ->', status)
question_id = json.loads(body)['id']

print('GET  /api/questions/%s/   ->' % question_id,
      call('GET', f'/api/questions/{question_id}/', accept='text/html')[0])
print('PATCH /api/questions/%s/  ->' % question_id,
      call('PATCH', f'/api/questions/{question_id}/', {'score': 20})[0])
print('DELETE /api/questions/%s/ ->' % question_id, call('DELETE', f'/api/questions/{question_id}/')[0])
print('DELETE /api/exams/%s/     ->' % exam_id, call('DELETE', f'/api/exams/{exam_id}/')[0])
