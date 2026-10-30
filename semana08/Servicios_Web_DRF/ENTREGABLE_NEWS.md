# Entregable — Motor de plantillas con Django (news)

## 1. Estructura de plantillas (`news/templates/news/`)
- `base.html`: estructura común con bloques `title`, `content`, `sidebar`.
- `_article_card.html`: fragmento reutilizable (una tarjeta). Se incluye con
  `{% include "news/_article_card.html" with article=article %}`.
- `frontpage.html`: hereda de base, recorre con `{% for %}`, caso vacío con
  `{% empty %}`, filtros `date` y `truncatewords`.
- `article_detail.html`: hereda de base; imagen, autor y categorías.
- `category_list.html`: hereda de base y reutiliza el mismo fragmento.
- Estilos: `news/static/news/css/portal.css` con `{% load static %}`.

## 2. Rutas (`news/urls.py`, `app_name = 'news'`)
- `''` → `frontpage`; `'article/<int:pk>/'` → `article-detail`;
  `'category/<int:pk>/'` → `category-list`.
- Todas enlazadas con `{% url %}`, sin direcciones a mano.

## 3. Datos de prueba (ver `seed_news.py`)
- 3 categorías (Tecnología, Deportes, Cultura), 2 autores,
  6 noticias publicadas; "IA en las aulas" en 2 categorías.

## 4. Casos de prueba
- `/news/` → 200 y muestra "Django 6 llega con mejoras de rendimiento".
- `/news/article/1/` → 200 con imagen (si hay), autor y categorías.
- `/news/category/1/` → 200 reutilizando las tarjetas.
- `/static/news/css/portal.css` → 200.
- Sin noticias: la portada muestra "Todavía no hay noticias publicadas."

## 5. Escapado automático (paso 12)
- Artículo "Prueba de escapado HTML" (`/news/article/6/`) guarda en `body`:
  `Texto normal <strong>texto en negrita</strong> <script>alert("xss")</script> fin.`
- La página muestra las etiquetas como texto literal (`&lt;strong&gt;`,
  `&lt;script&gt;`) y NO ejecuta el script.
- Por qué: Django escapa por defecto toda variable `{{ ... }}` para prevenir
  XSS. Solo se renderizaría HTML con el filtro `|safe`, que exige contenido
  confiable o sanitizado.

## 6. Capturas para el campus
- Portada con tarjetas, detalle con autor/categorías, listado por categoría,
  admin de Article con filtros/búsqueda, y detalle del artículo 6 mostrando
  las etiquetas escapadas.

## 7. Repositorio
- Rama `news-portal` con migraciones `news/migrations/0001_initial.py`,
  plantillas, estilos y scripts `seed_news.py`.
