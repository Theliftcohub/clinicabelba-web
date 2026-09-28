#!/usr/bin/env python3
"""Genera public/css/site.css (CSS local renombrado + fuentes locales) y copia las fuentes."""
import json, os, re, shutil, glob, sys
B = '/home/claude/belba'
sys.path.insert(0, B + '/scripts')
from convert import ren_css

W = B + '/migracion/wpcss/'
ORDER = [
    'themes__hello-elementor__assets__css__reset.css',
    'themes__hello-elementor__assets__css__theme.css',
    'themes__hello-elementor__assets__css__header-footer.css',
    'plugins__elementor__assets__css__frontend.min.css',
    'plugins__elementor__assets__css__widget-heading.min.css',
    'plugins__elementor__assets__css__widget-image.min.css',
    'plugins__elementor__assets__css__widget-icon-list.min.css',
    'plugins__elementor__assets__css__widget-social-icons.min.css',
    'plugins__elementor-pro__assets__css__widget-nav-menu.min.css',
    'plugins__elementor-pro__assets__css__modules__sticky.min.css',
    'plugins__elementor__assets__css__widget-google_maps.min.css',
    'plugins__elementor__assets__css__widget-accordion.min.css',
    'plugins__elementor__assets__css__widget-spacer.min.css',
    'plugins__elementor__assets__css__widget-video.min.css',
    'plugins__elementor__assets__css__widget-image-gallery.min.css',
    'plugins__elementor__assets__css__widget-image-box.min.css',
    'plugins__elementor-pro__assets__css__widget-form.min.css',
    'plugins__elementor__assets__css__widget-divider.min.css',
    'plugins__elementor-pro__assets__css__widget-posts.min.css',
    'plugins__elementor__assets__css__conditionals__e-swiper.min.css',
    'plugins__elementor__assets__lib__swiper__v8__css__swiper.min.css',
    'plugins__elementor__assets__css__widget-menu-anchor.min.css',
    'plugins__elementor__assets__css__widget-image-carousel.min.css',
    'plugins__elementor__assets__css__widget-nested-accordion.min.css',
    'plugins__elementor-pro__assets__css__widget-author-box.min.css',
    'plugins__elementor-pro__assets__css__widget-post-info.min.css',
    'plugins__elementor__assets__css__widget-icon-box.min.css',
    'plugins__elementor-pro__assets__css__widget-table-of-contents.min.css',
    'plugins__elementor-pro__assets__css__widget-carousel-module-base.min.css',
    'plugins__elementor-pro__assets__css__widget-testimonial-carousel.min.css',
    'plugins__elementor__assets__css__widget-nested-tabs.min.css',
    'plugins__elementor-pro__assets__css__widget-slides.min.css',
    'plugins__elementor-pro__assets__css__widget-price-list.min.css',
    'plugins__elementor-pro__assets__css__widget-animated-headline.min.css',
    'plugins__translatepress-multilingual__assets__css__trp-language-switcher-v2.css',
    'themes__hello-elementor-child__style.css',
]

def fonts_css():
    src = B + '/node_modules/@fontsource/montserrat/'
    os.makedirs(B + '/public/fonts', exist_ok=True)
    out = []
    for wgt in ('300', '400', '500', '600', '700', '800'):
        for style in ('', '-italic') if wgt == '400' else ('',):
            fn = src + (f'{wgt}{style}.css')
            if not os.path.exists(fn):
                continue
            css = open(fn).read()
            # solo latin, latin-ext, cyrillic, cyrillic-ext
            blocks = re.findall(r'/\*[^*]*\*/\s*@font-face\s*\{[^}]*\}', css)
            for bl in blocks:
                if not re.search(r'montserrat-(latin|latin-ext|cyrillic|cyrillic-ext)-\d', bl):
                    continue
                files = re.findall(r'url\(\./files/([^)]+\.woff2)\)', bl)
                for f in files:
                    shutil.copy(src + 'files/' + f, B + '/public/fonts/' + f)
                bl = re.sub(r'url\(\./files/([^)]+\.woff2)\)\s*format\(\'woff2\'\)\s*,\s*url\([^)]+\)\s*format\(\'woff\'\)', r"url(/fonts/\1) format('woff2')", bl)
                bl = bl.replace('url(./files/', 'url(/fonts/')
                bl = bl.replace("font-family: 'Montserrat'", 'font-family: "Montserrat"')
                out.append(bl)
    return '\n'.join(out)

EXTRA = r'''
/* ---- ajustes propios de la web estática ---- */
.k-sticky-top{position:sticky;top:0;z-index:99}
.kt-header{position:relative;z-index:100}
.k-invisible{visibility:visible!important}
.hp-field{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
details.k-accordion-item>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:.5em}
details.k-accordion-item>summary::-webkit-details-marker{display:none}
details.k-accordion-item .k-accordion-icon-opened{display:none}
details.k-accordion-item[open] .k-accordion-icon-opened{display:inline-block}
details.k-accordion-item[open] .k-accordion-icon-closed{display:none}
details.k-accordion-item>.k-tab-content{display:block}
.k-accordion .k-accordion-title{margin:0;font:inherit;color:inherit}
.k-video-iframe{width:100%;aspect-ratio:16/9;border:0;display:block}
.k-widget-video .k-wrapper{aspect-ratio:var(--video-aspect-ratio-css,16/9)}
.swiper{overflow:hidden;position:relative}
.swiper-wrapper{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;transform:none!important}
.swiper-wrapper::-webkit-scrollbar{display:none}
.swiper-slide{flex:0 0 calc(100% / var(--spv,1));scroll-snap-align:start;width:auto!important}
.k-toc__list-wrapper{margin:0;padding-left:1.2em}
.k-toc__sub{margin-left:1em}
.k-nav-menu--main .sub-menu{display:none}
.k-nav-menu--main li:hover>.sub-menu,.k-nav-menu--main li:focus-within>.sub-menu{display:block}
.k-nav-menu--main .sub-menu .sub-menu{left:100%;top:0}
.k-nav-menu--dropdown.k-nav-menu__container{display:none}
.k-menu-toggle.k-active + .k-nav-menu--dropdown.k-nav-menu__container{display:block;max-height:80vh;overflow:auto;transform:none}
.k-nav-menu--dropdown .sub-menu{display:none;position:static}
.k-nav-menu--dropdown li.open>.sub-menu{display:block}
.form-aviso{padding:.8em 1em;border:1px solid #008488;color:#143852;background:#D3E4EA;margin:0 0 1em;font-size:14px}
.form-ok{padding:1em;background:#e8f6ef;color:#14532d;border:1px solid #86c9a3;margin-top:1em}
/* Formularios nativos (sustituyen a Typeform) */
.belba-form{max-width:640px;margin:0 auto;padding:28px 24px;background:#fff;border-radius:14px;box-shadow:0 6px 28px rgba(23,34,57,.10);font-family:Montserrat,sans-serif;color:#172239;text-align:left}
.belba-form [hidden]{display:none!important}
.bf-progress{height:4px;background:#EEEEEE;border-radius:4px;margin-bottom:22px;overflow:hidden}
.bf-progress span{display:block;height:100%;width:0;background:#008488;transition:width .3s}
.bf-count{display:block;margin:0 0 6px;font-size:13px;color:#008488;font-weight:600}
.bf-legend{padding:0;margin:0 0 16px;display:block;width:100%}.bf-legend .bf-title{margin:0}
.bf-title{display:block;margin:0 0 16px;font-size:20px;line-height:1.35;font-weight:600;color:#172239}
.bf-text{font-size:16px;line-height:1.55;margin:0 0 18px}
.bf-fieldset{border:0;margin:0;padding:0;min-width:0}
.bf-choices{display:grid;gap:10px}
.bf-choice{display:flex;align-items:center;gap:10px;padding:12px 14px;border:1.5px solid #D3E4EA;border-radius:10px;cursor:pointer;font-size:15px;transition:border-color .15s,background .15s}
.bf-choice:hover{border-color:#008488}
.bf-choice input{accent-color:#008488;width:18px;height:18px;margin:0;flex:none}
.bf-choice:has(input:checked){border-color:#008488;background:#E9F5F5}
.bf-input,.bf-sub input{width:100%;box-sizing:border-box;padding:12px 14px;border:1.5px solid #D3E4EA;border-radius:10px;font:inherit;font-size:16px;color:#172239;background:#fff}
.bf-input:focus,.bf-sub input:focus{outline:none;border-color:#008488;box-shadow:0 0 0 3px rgba(0,132,136,.15)}
.bf-subs{display:grid;gap:12px}
.bf-sub span{display:block;font-size:13px;font-weight:600;margin-bottom:4px}
.bf-nav{display:flex;justify-content:space-between;gap:10px;margin-top:20px}
.bf-next,.bf-submit{margin-left:auto;background:#008488;color:#fff;border:0;border-radius:14px;padding:12px 26px;font:600 15px Montserrat,sans-serif;cursor:pointer}
.bf-next:hover,.bf-submit:hover{background:#006d70}
.bf-back{background:transparent;color:#143852;border:1.5px solid #D3E4EA;border-radius:14px;padding:12px 20px;font:600 15px Montserrat,sans-serif;cursor:pointer}
.bf-submit[disabled]{opacity:.6;cursor:wait}
.bf-invalid .bf-choices,.bf-invalid .bf-input,.bf-invalid .bf-subs input:invalid{outline:2px solid #c0392b;outline-offset:2px;border-radius:10px}
.bf-legal{font-size:12px;color:#555;margin:14px 0 0}
.bf-legal a{color:#008488}
.bf-thanks p{font-size:18px;line-height:1.5;font-weight:600;color:#008488;margin:0}
.bf-error{color:#c0392b;font-size:14px;margin:12px 0 0}
@media (max-width:600px){.belba-form{padding:20px 16px}.bf-title{font-size:18px}}
/* ===== TEMA BELBA (decisión Oscar 28/09): toda la web con el estilo de la home nueva. Solo presentación; textos y URLs intactos ===== */
:root{--b-navy:#172239;--b-navy2:#143852;--b-teal:#008488;--b-teal2:#006d70;--b-sky:#D3E4EA;--b-grey:#F3F5F4;--b-radius:14px}
main .k-button,main .k-button-link{border-radius:var(--b-radius)!important;font-weight:600;letter-spacing:0;text-transform:none;box-shadow:none;transition:background .15s,transform .15s}
main .k-button:hover,main .k-button-link:hover{transform:translateY(-1px)}
main .k-field-textual,main input.k-field,main textarea.k-field,main select.k-field-textual{border:1.5px solid var(--b-sky);border-radius:10px;padding:12px 14px;font-family:Montserrat,sans-serif;font-size:16px;color:var(--b-navy);background:#fff}
main .k-field-textual:focus,main input.k-field:focus,main textarea.k-field:focus{outline:none;border-color:var(--b-teal);box-shadow:0 0 0 3px rgba(0,132,136,.15)}
main .k-form .k-button{background:var(--b-teal);color:#fff;border:0;padding:12px 26px}
main .k-form .k-button:hover{background:var(--b-teal2)}
main .k-widget-image img,main .k-widget-image-box img,main .k-widget-call-to-action .k-cta__bg,main .k-widget-video .k-wrapper,main .k-widget-image-carousel .swiper-slide img,main .k-post__thumbnail img{border-radius:16px}
main .k-widget-image-box .k-image-box-wrapper,main .k-widget-icon-box{border-radius:18px}
main .k-accordion .k-accordion-item{border:1px solid #e6ecee!important;border-radius:12px;margin-bottom:10px;overflow:hidden;background:#fff}
main .k-accordion .k-tab-title{font-family:Montserrat,sans-serif;font-weight:600;color:var(--b-navy);padding:16px 20px;cursor:pointer;list-style:none}
main .k-accordion .k-tab-title::-webkit-details-marker{display:none}
main .k-accordion .k-tab-title.k-active{color:var(--b-teal)}
main .k-accordion .k-tab-content{border-top:1px solid #eef2f3!important;padding:16px 20px}
main .k-toggle .k-tab-title{font-weight:600;color:var(--b-navy)}
main .k-post{border-radius:18px;overflow:hidden;border:1px solid #e6ecee;box-shadow:none}
main .k-post__title a{color:var(--b-navy)}.k-post__title a:hover{color:var(--b-teal)}
main .k-widget-heading .k-heading-title{letter-spacing:0}
main .k-widget-testimonial{border-radius:18px}
main .k-widget-counter .k-counter-number-wrapper{color:var(--b-teal)}
main .e-n-accordion-item{border:1px solid #e6ecee;border-radius:12px;margin-bottom:10px;background:#fff}
main .e-n-accordion-item-title{padding:16px 20px;font-weight:600;color:var(--b-navy)}
main .k-widget-table-of-contents .k-toc__header{border-radius:12px 12px 0 0}
main .k-widget-table-of-contents{border-radius:12px;border-color:#e6ecee}
/* cabecera: sin el margen negativo (compensaba la barra de TranslatePress, que ya no existe); sticky en tablet/móvil como en el WP */
.k-38 .k-element.k-element-ce67a94{margin-top:0!important}
@media(max-width:1024px){header.k-38{position:sticky;top:0;z-index:9998;background:#fff;box-shadow:0 2px 12px rgba(23,34,57,.08)}
/* menú móvil a todo el ancho bajo la cabecera (lo hacía el JS de Elementor) */
header.k-38 .k-section,header.k-38 .k-container,header.k-38 .k-column,header.k-38 .k-widget-wrap,header.k-38 .k-widget-nav-menu,header.k-38 .k-widget-nav-menu>.k-widget-container{position:static}
header.k-38 .k-element.k-widget-nav-menu .k-nav-menu__container.k-nav-menu--dropdown{position:absolute;left:0;right:0;width:100%;top:100%;margin-top:0!important;max-height:calc(100vh - 90px);overflow:auto;z-index:9999}
.k-nav-menu--dropdown .menu-item-has-children>.sub-menu{position:static;width:100%;min-width:0;max-width:none;display:none;background:rgba(0,0,0,.08)}
.k-nav-menu--dropdown li.open>.sub-menu{display:block}}
/* desplegables del menú: ancho al contenido (el JS de Elementor lo hacía en tiempo real) y sin cortes */
.k-nav-menu--main .k-nav-menu ul{width:auto;min-width:12em;max-width:22em}
.k-nav-menu--main .k-nav-menu--dropdown a{white-space:nowrap;padding:12px 18px}
.k-nav-menu--main li.open>.sub-menu{display:block}
.k-nav-menu--main .sub-menu{box-shadow:0 12px 32px rgba(23,34,57,.16);border-radius:0 0 10px 10px;overflow:hidden}
/* selector de idioma en la cabecera */
.k-38 .ls-widget{width:auto;margin-left:12px;position:relative;z-index:101}
.ls{position:relative;font-family:Montserrat,sans-serif}
.ls__cur{display:inline-flex;align-items:center;gap:7px;background:#fff;border:1.5px solid #D3E4EA;border-radius:10px;padding:7px 10px;font:600 13px Montserrat,sans-serif;color:#143852;cursor:pointer;line-height:1}
.ls__cur:hover,.ls.is-open .ls__cur{border-color:#008488}
.ls__cur img,.ls__list img{width:20px;height:15px;border-radius:2px;object-fit:cover;display:block}
.ls__chev{width:7px;height:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg);margin:-3px 2px 0}
.ls__list{position:absolute;right:0;top:calc(100% + 8px);margin:0;padding:6px;list-style:none;background:#fff;border:1px solid #e6ecee;border-radius:12px;box-shadow:0 12px 32px rgba(23,34,57,.14);min-width:170px}
.ls__list[hidden]{display:none}
.ls__list a{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:8px;color:#172239;text-decoration:none;font-size:14px;white-space:nowrap}
.ls__list a:hover{background:#E9F5F5;color:#008488}
@media(max-width:1024px){.k-38 .ls-widget{margin-left:8px}.ls__code{display:none}.ls__cur{padding:7px 8px}}
/* pie compacto global (build_footer.py) */
.hn-wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.hn-footer{background:var(--b-navy);color:#c9d3df;padding:56px 0 90px;font-size:14px;font-family:Montserrat,sans-serif;line-height:1.6}
.hn-footer a{color:#e6f2f2;text-decoration:none}.hn-footer a:hover{color:#9fd8d9}
.hn-footer__grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.2fr;gap:40px}
.hn-footer__brand img{height:44px;width:auto;filter:brightness(0) invert(1);margin-bottom:14px}
.hn-footer__brand p{margin:0 0 6px}
.hn-footer__h{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#9fd8d9;font-weight:700;margin:0 0 12px}
.hn-footer ul{list-style:none;margin:0;padding:0}.hn-footer li{padding:4px 0}
.hn-footer__bottom{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 28px;margin-top:40px;padding-top:22px;border-top:1px solid rgba(255,255,255,.12);font-size:13px}
.hn-footer__bottom p{margin:0}.hn-footer__legal{display:flex;flex-wrap:wrap;gap:6px 18px}
.hn-footer__eu-row{margin-top:18px}
.hn-footer .hn-footer__eu{height:56px!important;width:auto!important;max-width:none;background:#fff;border-radius:8px;padding:6px 10px;flex:0 0 auto}
@media(max-width:820px){.hn-footer__grid{grid-template-columns:1fr 1fr;gap:28px}}
@media(max-width:480px){.hn-footer__grid{grid-template-columns:1fr}}
/* Formularios de Elementor largos, por pasos (site.js añade .is-steps) */
.k-form.is-steps .k-step{width:100%;display:flex;flex-wrap:wrap;align-items:flex-end}
.k-form.is-steps .k-step[hidden]{display:none!important}
.k-form.is-steps .bf-count,.k-form.is-steps .bf-nav{width:100%;padding:0 calc(var(--column-gap,10px)/2)}
.k-form.is-steps .bf-progress{width:100%}
.k-form.is-steps .k-field-type-submit{margin-top:6px}
.bf-follow{margin-top:14px;padding:20px}
.bf-follow .bf-title{font-size:17px;margin-bottom:12px}
.k-form [hidden]{display:none!important}
.bf-follow{box-sizing:border-box;width:100%}
.bf-follow .bf-choice{width:100%;box-sizing:border-box;white-space:normal;background:#fff;text-align:left;font:500 15px Montserrat,sans-serif;color:#172239}
.bf-follow .bf-choice:hover,.bf-follow .bf-choice:focus-visible{border-color:#008488;background:#E9F5F5;outline:none}
.bf-follow .bf-skip{margin-top:12px;padding:8px 16px;font-size:14px}
.bf-ok{margin:0 0 6px;color:#008488;font-weight:700;font-size:18px}
.bf-thanks-txt{margin:0;font-size:16px;font-weight:600;color:#008488;line-height:1.5}
'''

def write_follow():
    """Pregunta de cualificación (tras formularios cortos) en los 9 idiomas → site.js entre /*FOLLOW-START*/ y /*FOLLOW-END*/."""
    import sys; sys.path.insert(0, B + '/scripts')
    from home_i18n import FOLLOW
    js = 'var FOLLOW = ' + json.dumps({k: {'q': v[0], 'o': v[1], 'skip': v[2], 'thanks': v[3]} for k, v in FOLLOW.items()}, ensure_ascii=False) + ';'
    p = B + '/public/js/site.js'
    src = open(p, encoding='utf-8').read()
    new = re.sub(r'/\*FOLLOW-START\*/.*?/\*FOLLOW-END\*/', '/*FOLLOW-START*/ ' + js.replace('\\', '\\\\') + ' /*FOLLOW-END*/', src, flags=re.S)
    if new != src: open(p, 'w', encoding='utf-8').write(new)

def main():
    write_follow()
    parts = [fonts_css()]
    for f in ORDER:
        css = open(W + f, encoding='utf-8', errors='replace').read()
        css = re.sub(r'@import[^;]+;', '', css)
        parts.append(f'/* {f} */\n' + ren_css(css))
    lc = B + '/migracion/layout.css'
    if os.path.exists(lc):
        parts.append('/* cabecera y pie (Elementor 38/135) */\n' + open(lc).read())
    cc = B + '/migracion/wp_custom_css.css'
    if os.path.exists(cc):
        parts.append('/* wp-custom-css */\n' + open(cc).read())
    parts.append(EXTRA)
    css = '\n'.join(parts)
    css = re.sub(r'/\*# sourceMappingURL=[^*]*\*/', '', css)
    os.makedirs(B + '/public/css', exist_ok=True)
    open(B + '/public/css/site.css', 'w').write(css)
    for opt in ('uploads__trustindex-google-widget.css', 'css__dist__block-library__style.min.css'):
        open(B + '/public/css/' + opt.split('__')[-1], 'w').write(ren_css(open(W + opt, encoding='utf-8', errors='replace').read()))
    print('site.css', len(css))

if __name__ == '__main__':
    main()
