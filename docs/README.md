# praxis — landing page (GitHub Pages)

Página estática de promoción del plugin **praxis**. Sin build, sin dependencias:
HTML + CSS + JS vanilla. Se sirve tal cual desde GitHub Pages.

## Archivos

| Archivo        | Propósito                                              |
| -------------- | ------------------------------------------------------ |
| `index.html`   | Página principal (hero, expertos, memoria, instalación)|
| `styles.css`   | Estilos (tema oscuro, responsive, WCAG AA)             |
| `script.js`    | Tabs, menú móvil, copiar al portapapeles, reveal       |
| `favicon.svg`  | Icono                                                  |
| `.nojekyll`    | Desactiva el procesado Jekyll de GitHub Pages          |

## Cómo activar GitHub Pages

1. En GitHub: **Settings → Pages**.
2. En **Build and deployment → Source**, elige **Deploy from a branch**.
3. Selecciona la rama (por ejemplo `main`) y la carpeta **`/docs`**.
4. Guarda. La página quedará publicada en:
   `https://marcrabadan.github.io/praxis/`

> Si prefieres publicar desde otra rama, selecciónala en el paso 3.
> El contenido de `/docs` se sirve sin modificaciones gracias a `.nojekyll`.

## Desarrollo local

Cualquier servidor estático sirve. Por ejemplo:

```bash
cd docs && python3 -m http.server 8080
# abre http://localhost:8080
```
