from django import template
import environ
import json
from config import settings 
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def vite() -> str:
    env = environ.Env()
    vite_port = env("VITE_PORT")
    
    manifest_path = settings.STATIC_ROOT / "manifest.json"

    print(manifest_path)

    if not settings.DEBUG and not manifest_path.exists():
        raise Exception("Error: manifest.json not found.")

    manifest = json.loads(manifest_path.read_text())

    css_file = "static/" +  manifest["src/js/main.css"]["file"] 
    js_file = "static/" +  manifest["src/js/main.js"]["file"]  

    if settings.DEBUG:
        return mark_safe(
            f'''<script type="module" src="http://localhost:{vite_port}/@vite/client"></script>
            <script type="module" src="http://localhost:{vite_port}/src/js/main.js"></script>'''
        )
    else:
        return mark_safe(
                f'''<link rel="stylesheet" type="text/css" href="{css_file}">
            <script type="module" src="{js_file}"></script>'''
        )
