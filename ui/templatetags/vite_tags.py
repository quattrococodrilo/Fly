from django import template
import environ
import json
from config.settings import STATIC_ROOT, DEBUG

register = template.Library()

@register.simple_tag
def vite() -> str:
    env = environ.Env()
    vite_port = env("VITE_PORT", 5173)
    
    manifest_path = STATIC_ROOT / "manifest.json"

    if not DEBUG and not manifest_path.exists():
        raise Exception("Error: manifest.json not found.")

    manifest = json.loads(manifest_path.read_text())

    css_file = manifest["src/css/main.css"]["file"] 
    js_file = manifest["src/js/main.js"]["file"]  

    if DEBUG:
        return (
            f'<script type="module" src="http://localhost:{vite_port}/@vite/client"></script>'
            "\n"
            f'<script type="module" src="http://localhost:{vite_port}/src/js/main.js"></script>'
        )
    else:
        return (
            f'<link rel="stylesheet" type="text/css" href="{css_file}">' 
            "\n"
            f'<script type="module" src="{js_file}"></script>'  
        )
