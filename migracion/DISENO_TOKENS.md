# Tokens de marca (sacados del CSS real, 27/09/2026)

Origen: el kit global de Elementor y los estilos computados en la portada (`design_tokens_raw.json`). Las capturas de las 9 plantillas, en escritorio y móvil, están en `screenshots/`.

| Token | Valor | Uso visto |
|---|---|---|
| `--navy` | #172239 | titulares y fondos oscuros (kit dca9c6e / df59760) |
| `--navy-2` | #143852 | fondo de enlaces y botones del menú |
| `--navy-deep` | #0E1624 | pie |
| `--teal` | #008488 | botón principal (CTA "Solicita tu valoración", "Consulta online") |
| `--sky` | #D3E4EA | fondos suaves |
| `--taupe` | #9C847D | acentos |
| `--grey-50` | #F3F5F4 | fondos de sección |
| `--grey-100` | #EEEEEE | separadores |
| `--text` | #333333 | cuerpo |
| `--white` | #FFFFFF | |

Los colores por defecto de Elementor (#6EC1E4, #54595F, #7A7A7A, #61CE70) no se usan en la web: no se migran.

Tipografía:
- **Montserrat**: cuerpo a 17 px / 400; H1 a 40 px / 700; H2 a 32 px / 500; botones a 15 px.
- Roboto Slab está declarada en el kit, pero no se ha visto en uso. Se confirma en la fase 3 y, si no aparece, no se carga.

## Navegación de plantilla que hay que replicar (enlazado interno)
- Menú: Quiénes somos (desplegable) · Cirugía plástica (desplegable) · Contacto · Guía del paciente · Blog · **Consulta online** (botón con desplegable) · **Test paciente** (botón).
- Franja de logos: Clínica Belba · Quirónsalud · Centro Médico Teknon.
- WhatsApp flotante y selector de idioma flotante (TranslatePress).

## Defectos de la web actual que NO se replican
- Aviso de TranslatePress "We've detected you might be speaking a different language" encima de la cabecera.
- En móvil, en `/aumento-pecho-barcelona/` aparece un texto suelto `";` donde debería estar la cabecera (marcado roto). Se revisará en las demás plantillas en la fase 3.
