#!/usr/bin/env python3
"""srcset con anchos reales.

convert.py escribía en cada imagen `srcset="X-800.webp 800w, X.webp 1600w"` sin mirar el tamaño del archivo. Con un
descriptor mayor que el ancho real, el navegador calcula una densidad falsa (800 / ancho de pantalla) y pinta la imagen
a la mitad o a un tercio de su tamaño: en móvil, una miniatura de 550 px salía a 268 px y la foto de un doctor de 500 px
a 243 px (aviso de Nicols 01/10 con la web ya en producción). Regla: si el archivo original mide 800 px o menos no hay
versión más grande y el srcset sobra (queda solo `src`); si es mayor, los descriptores llevan el ancho real de cada archivo.
Idempotente; va en el pipeline tras build_blog.py. También lo usan convert.py y build_blog.py al generar."""
import glob, json, os, re, struct

B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}


def webp_size(path):
    """(ancho, alto) de un WebP (VP8, VP8L o VP8X) sin PIL; None si no es WebP o no existe."""
    if path in _cache:
        return _cache[path]
    size = None
    try:
        with open(path, 'rb') as fh:
            b = fh.read(64)
        if b[:4] == b'RIFF' and b[8:12] == b'WEBP':
            c = b[12:16]
            if c == b'VP8X':
                size = (int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1)
            elif c == b'VP8 ':
                i = b.find(b'\x9d\x01\x2a')
                if i > 0:
                    w, h = struct.unpack('<HH', b[i + 3:i + 7])
                    size = (w & 0x3fff, h & 0x3fff)
            elif c == b'VP8L':
                bits = int.from_bytes(b[21:25], 'little')
                size = ((bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1)
    except OSError:
        pass
    _cache[path] = size
    return size


def srcset_for(src, public=None):
    """srcset correcto para una imagen local `/images/...webp`, o None si no procede (sin versión -800 o ≤ 800 px)."""
    public = public or (B + '/public')
    if not src.startswith('/') or not src.endswith('.webp'):
        return None
    small = src[:-5] + '-800.webp'
    big = webp_size(public + src)
    if big is None or big[0] <= 800 or not os.path.exists(public + small):
        return None
    return f'{small} 800w, {src} {big[0]}w'


_IMG = re.compile(r'<img\b[^>]*>', re.I)
_SRC = re.compile(r'\ssrc="([^"]+)"')
_SRCSET = re.compile(r'\s(?:srcset|sizes)="[^"]*"')


def fix_html(html, public=None):
    cambios = [0]

    def img(m):
        tag = m.group(0)
        if 'srcset=' not in tag:
            return tag
        s = _SRC.search(tag)
        if not s:
            return tag
        nuevo = srcset_for(s.group(1), public)
        limpio = _SRCSET.sub('', tag)
        if nuevo:
            limpio = limpio[:-1].rstrip('/') .rstrip() + f' srcset="{nuevo}" sizes="(max-width: 800px) 100vw, 800px"' + ('/>' if tag.endswith('/>') else '>')
        if limpio != tag:
            cambios[0] += 1
        return limpio

    out = _IMG.sub(img, html)
    return out, cambios[0]


def main():
    archivos = glob.glob(B + '/src/content/pages/*/*.json') + glob.glob(B + '/src/content/layout/*.json')
    tocados = imgs = 0
    for f in archivos:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        n = 0

        def walk(o):
            nonlocal n
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(v, str) and '<img' in v:
                        o[k], c = fix_html(v)
                        n += c
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(d)
        if n:
            tocados += 1
            imgs += n
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False)
    print(f'srcset: {imgs} imágenes corregidas en {tocados} archivos')


if __name__ == '__main__':
    main()
