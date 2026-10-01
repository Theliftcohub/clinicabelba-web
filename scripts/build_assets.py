#!/usr/bin/env python3
"""Genera public/css/site.css (CSS local renombrado + fuentes locales) y copia las fuentes."""
import json, os, re, shutil, glob, sys
B = os.environ.get('BELBA_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raíz del repo (o BELBA_ROOT)
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
/* (el menú desplegable de tablet/móvil está más abajo, en «cabecera (30/09)») */
/* desplegables del menú: ancho al contenido (el JS de Elementor lo hacía en tiempo real) y sin cortes */
.k-nav-menu--main .k-nav-menu ul{width:auto;min-width:12em;max-width:none}
.k-nav-menu--main .k-nav-menu--dropdown a{white-space:nowrap;padding:12px 18px}
.k-nav-menu--main li.open>.sub-menu{display:block}
.k-nav-menu--main .sub-menu{box-shadow:0 12px 32px rgba(23,34,57,.16);border-radius:0 0 10px 10px}
/* 3.er y 4.º nivel del menú de escritorio: se abren a la derecha, como en el WP (30/09; antes los tapaba overflow:hidden) */
.k-nav-menu--main .sub-menu li{position:relative}
.k-nav-menu--main .sub-menu>li:first-child>a{border-radius:0}
.k-nav-menu--main .sub-menu>li:last-child>a{border-radius:0 0 10px 10px}
.k-nav-menu--layout-horizontal .k-nav-menu>li .sub-menu .sub-menu{top:0!important;left:100%!important;inset-inline-start:100%!important;margin:0!important;border-radius:0 10px 10px 10px}
.k-nav-menu--main .sub-menu .sub-menu>li:first-child>a{border-radius:0 10px 0 0}
.k-nav-menu--main .sub-menu .menu-item-has-children>a .sub-arrow{margin-left:auto;padding-left:14px}
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
/* cabecera (30/09): completa y en una fila en escritorio, sin depender del CSS del kit de cada página (la home nueva no lo trae) */
header.k-38 .k-section-boxed>.k-container{max-width:1280px}
header.k-38 .k-element.k-element-ce67a94{padding:10px 0!important;border-bottom:1px solid #eef2f3}
header.k-38 .k-widget-wrap{align-items:center!important;flex-wrap:nowrap!important;gap:0 14px}
header.k-38 .k-widget-theme-site-logo{flex:0 0 auto}
header.k-38 .k-widget-theme-site-logo img{width:176px;height:auto;display:block}
header.k-38 .k-widget-nav-menu{margin-left:auto;min-width:0}
header.k-38 .ls-widget{flex:0 0 auto;margin-left:0;position:relative;z-index:101}
header.k-38 .k-nav-menu--main .k-nav-menu{flex-wrap:nowrap}
header.k-38 .k-nav-menu--main .k-nav-menu>li{flex-grow:0}
header.k-38 .k-nav-menu--main .k-nav-menu>li>.k-item{white-space:nowrap;justify-content:center}
/* los dos botones: principal (Consulta online) y secundario (Test paciente), con las esquinas del resto de la web */
header.k-38 .k-nav-menu--main .btn_consulta_online{border-radius:10px;margin:0 0 0 8px!important;transition:background .2s}
header.k-38 .k-nav-menu--main .btn_consulta_online>.k-item{padding-left:16px!important;padding-right:16px!important}
header.k-38 .k-nav-menu--main .btn_consulta_online:hover{background:#006d70}
header.k-38 .k-nav-menu--main .btn_consulta_online>a:hover,header.k-38 .k-nav-menu--main .btn_consulta_online>a:focus{color:#fff!important}
header.k-38 .k-nav-menu--main .btn_consulta_online>a .sub-arrow svg{fill:currentColor}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010{background:#fff;box-shadow:inset 0 0 0 1.5px #008488}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a{color:#008488!important}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010:hover{background:#E9F5F5}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a:hover{color:#006d70!important}
header.k-38 .k-nav-menu--main .btn_consulta_online>.sub-menu{border-radius:10px}
@media(min-width:1440px){header.k-38 .k-section-boxed>.k-container{max-width:1360px}
html[lang|=ru] header.k-38 .k-section-boxed>.k-container,html[lang|=uk] header.k-38 .k-section-boxed>.k-container{max-width:1400px}
html[lang|=ru] header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item,html[lang|=uk] header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item{padding-left:7px;padding-right:7px;font-size:12px}
html[lang|=ru] header.k-38 .k-widget-theme-site-logo img,html[lang|=uk] header.k-38 .k-widget-theme-site-logo img{width:150px}
html[lang|=ru] header.k-38 .ls__code,html[lang|=uk] header.k-38 .ls__code{display:none}}
/* portátil (1280-1439 px): misma fila, más compacta */
@media(min-width:1280px) and (max-width:1439px){header.k-38 .k-widget-theme-site-logo img{width:150px}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item{padding-left:7px;padding-right:7px;font-size:12px}
header.k-38 .k-nav-menu--main .btn_consulta_online>.k-item{padding-left:12px!important;padding-right:12px!important}
header.k-38 .ls__code{display:none}}
/* menú desplegable: tablet y móvil como en el WP, y también por debajo de 1280 px (el menú completo no cabe);
   en ruso y ucraniano, con el menú más largo, por debajo de 1440 px */
@media(max-width:1279px){
header.k-38{position:sticky;top:0;z-index:9998;background:#fff;box-shadow:0 2px 12px rgba(23,34,57,.08)}
header.k-38 .k-section,header.k-38 .k-container,header.k-38 .k-column,header.k-38 .k-widget-wrap,header.k-38 .k-widget-nav-menu,header.k-38 .k-widget-nav-menu>.k-widget-container{position:static}
header.k-38 .k-element.k-widget-nav-menu .k-nav-menu__container.k-nav-menu--dropdown{position:absolute;left:0;right:0;width:100%;top:100%;margin-top:0!important;max-height:calc(100vh - 90px);overflow:auto;z-index:9999}
.k-nav-menu--dropdown .menu-item-has-children>.sub-menu{position:static;width:100%;min-width:0;max-width:none;display:none;background:rgba(0,0,0,.08)}
.k-nav-menu--dropdown li.open>.sub-menu{display:block}
.ls__code{display:none}
.ls__cur{padding:7px 8px}
header.k-38 .k-widget-theme-site-logo img{width:150px}
header.k-38 .ls-widget{order:1;margin-left:auto}
header.k-38 .k-widget-nav-menu{order:2;margin-left:0}
header.k-38 .k-element.k-element-c45204a>.k-widget-container{margin:0!important}
header.k-38 .k-menu-toggle{border-radius:10px;padding:9px}}
@media(min-width:1025px) and (max-width:1279px){
header.k-38 .k-nav-menu--dropdown-tablet .k-nav-menu--main{display:none}
header.k-38 .k-nav-menu--dropdown-tablet .k-menu-toggle{display:flex}
header.k-38 .k-nav-menu--dropdown-tablet nav.k-nav-menu--dropdown.k-nav-menu__container{display:block}}
@media(min-width:1280px) and (max-width:1439px){
html[lang|=ru] header.k-38,html[lang|=uk] header.k-38{position:sticky;top:0;z-index:9998;background:#fff;box-shadow:0 2px 12px rgba(23,34,57,.08)}
html[lang|=ru] header.k-38 .k-section,html[lang|=ru] header.k-38 .k-container,html[lang|=ru] header.k-38 .k-column,html[lang|=ru] header.k-38 .k-widget-wrap,html[lang|=ru] header.k-38 .k-widget-nav-menu,html[lang|=ru] header.k-38 .k-widget-nav-menu>.k-widget-container,html[lang|=uk] header.k-38 .k-section,html[lang|=uk] header.k-38 .k-container,html[lang|=uk] header.k-38 .k-column,html[lang|=uk] header.k-38 .k-widget-wrap,html[lang|=uk] header.k-38 .k-widget-nav-menu,html[lang|=uk] header.k-38 .k-widget-nav-menu>.k-widget-container{position:static}
html[lang|=ru] header.k-38 .k-element.k-widget-nav-menu .k-nav-menu__container.k-nav-menu--dropdown,html[lang|=uk] header.k-38 .k-element.k-widget-nav-menu .k-nav-menu__container.k-nav-menu--dropdown{position:absolute;left:0;right:0;width:100%;top:100%;margin-top:0!important;max-height:calc(100vh - 90px);overflow:auto;z-index:9999}
html[lang|=ru] .k-nav-menu--dropdown .menu-item-has-children>.sub-menu,html[lang|=uk] .k-nav-menu--dropdown .menu-item-has-children>.sub-menu{position:static;width:100%;min-width:0;max-width:none;display:none;background:rgba(0,0,0,.08)}
html[lang|=ru] .k-nav-menu--dropdown li.open>.sub-menu,html[lang|=uk] .k-nav-menu--dropdown li.open>.sub-menu{display:block}
html[lang|=ru] .ls__code,html[lang|=uk] .ls__code{display:none}
html[lang|=ru] .ls__cur,html[lang|=uk] .ls__cur{padding:7px 8px}
html[lang|=ru] header.k-38 .k-widget-theme-site-logo img,html[lang|=uk] header.k-38 .k-widget-theme-site-logo img{width:150px}
html[lang|=ru] header.k-38 .ls-widget,html[lang|=uk] header.k-38 .ls-widget{order:1;margin-left:auto}
html[lang|=ru] header.k-38 .k-widget-nav-menu,html[lang|=uk] header.k-38 .k-widget-nav-menu{order:2;margin-left:0}
html[lang|=ru] header.k-38 .k-element.k-element-c45204a>.k-widget-container,html[lang|=uk] header.k-38 .k-element.k-element-c45204a>.k-widget-container{margin:0!important}
html[lang|=ru] header.k-38 .k-menu-toggle,html[lang|=uk] header.k-38 .k-menu-toggle{border-radius:10px;padding:9px}
html[lang|=ru] header.k-38 .k-nav-menu--dropdown-tablet .k-nav-menu--main,html[lang|=uk] header.k-38 .k-nav-menu--dropdown-tablet .k-nav-menu--main{display:none}
html[lang|=ru] header.k-38 .k-nav-menu--dropdown-tablet .k-menu-toggle,html[lang|=uk] header.k-38 .k-nav-menu--dropdown-tablet .k-menu-toggle{display:flex}
html[lang|=ru] header.k-38 .k-nav-menu--dropdown-tablet nav.k-nav-menu--dropdown.k-nav-menu__container,html[lang|=uk] header.k-38 .k-nav-menu--dropdown-tablet nav.k-nav-menu--dropdown.k-nav-menu__container{display:block}}
/* cabecera refinada (30/09 noche, petición de Nicols): menú en minúsculas, botones redondos, barra fija con desenfoque */
header.k-38 .k-element.k-element-ce67a94{padding:14px 0!important;border-bottom:1px solid #ECE7DF;background:rgba(255,255,255,.92)!important;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
header.k-38{position:sticky;top:0;z-index:9998}
header.k-38 .k-widget-theme-site-logo img{width:160px}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item{text-transform:none;font-size:14px;font-weight:600;letter-spacing:-.1px;color:#172239;padding:10px 12px}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item:hover,header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item.k-item-active,header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item.highlighted,header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-item:focus{color:#008488;fill:#008488}
header.k-38 .k-nav-menu--main .sub-arrow{opacity:.55}header.k-38 .k-nav-menu--main .sub-arrow svg{width:.8em;height:.8em}
header.k-38 .k-nav-menu--main .btn_consulta_online{border-radius:999px;margin:0 0 0 10px!important;background:#008488;box-shadow:none}
header.k-38 .k-nav-menu--main .btn_consulta_online>.k-item{padding:11px 20px!important;color:#fff!important;font-size:14px!important;font-weight:700!important;text-transform:none}
header.k-38 .k-nav-menu--main .btn_consulta_online:hover{background:#172239}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010{background:transparent;box-shadow:inset 0 0 0 1.5px #172239}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a{color:#172239!important}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010:hover{background:#172239}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a:hover{color:#fff!important}
header.k-38 .k-nav-menu--main .btn_consulta_online>.sub-menu{border-radius:14px;margin-top:10px!important;overflow:hidden}
header.k-38 .k-nav-menu--main .sub-menu{border-radius:14px;background:#fff;box-shadow:0 20px 50px -10px rgba(23,34,57,.25);border:1px solid #ECE7DF}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a{color:#172239;fill:#172239;text-transform:none;font-size:13.5px;font-weight:500;background:#fff}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-nav-menu--dropdown a:hover,header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-nav-menu--dropdown a:focus,header.k-38 .k-element.k-element-c45204a .k-nav-menu--main .k-nav-menu--dropdown a.highlighted{background:#F7F4EF;color:#008488}
header.k-38 .k-nav-menu--main .btn_consulta_online .sub-menu a{background:#fff}
header.k-38 .k-nav-menu--main .sub-menu .sub-menu{border-radius:14px}
header.k-38 .ls__cur{border-radius:999px;border-color:#ECE7DF;color:#172239}
@media(min-width:1280px){header.k-38 .k-nav-menu--main .k-nav-menu>li:first-child>.k-item{padding-left:0}}
@media(max-width:1279px){header.k-38 .k-menu-toggle{border-radius:999px;background:#172239}
header.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a{text-transform:none;font-size:15px;font-weight:600;color:#172239;background:#fff}
header.k-38 .k-element.k-widget-nav-menu .k-nav-menu__container.k-nav-menu--dropdown{background:#fff;border-top:1px solid #ECE7DF;box-shadow:0 30px 60px -20px rgba(23,34,57,.3)}
.k-nav-menu--dropdown .menu-item-has-children>.sub-menu{background:#F7F4EF}}
/* desplegables: blancos y en minúsculas (misma especificidad que el kit de Elementor) */
.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown,.k-38 .k-element.k-element-c45204a .k-nav-menu--main .sub-menu{background-color:#fff!important;background:#fff!important;border:1px solid #ECE7DF;border-radius:14px}
.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a,.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown .k-item,.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown .k-sub-item{color:#172239!important;fill:#172239!important;text-transform:none!important;font-size:13.5px!important;font-weight:500!important;background:transparent!important}
.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a:hover,.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a:focus,.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a.highlighted,.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a.k-item-active{background:#F7F4EF!important;color:#008488!important}
.k-38 .k-element.k-element-c45204a .k-nav-menu--main>.k-nav-menu>li>.k-nav-menu--dropdown{margin-top:12px!important}
@media(max-width:1279px){.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown{border:0;border-radius:0}
.k-38 .k-element.k-element-c45204a .k-nav-menu--dropdown a{font-size:15px!important;font-weight:600!important}
.k-nav-menu--dropdown .menu-item-has-children>.sub-menu{background:#F7F4EF!important}}
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
/* cabecera (30/09 noche, corrección Nicols): barra de 84 px, logo en alta resolución, botón de idioma sin el rosa del kit
   ([type=button]:focus/hover del tema), «Test paciente» con borde fino turquesa y menú móvil como panel blanco con los dos botones */
header.k-38 .k-element.k-element-ce67a94{padding:8px 0!important}
header.k-38 .k-column>.k-widget-wrap{padding:6px 10px!important}
header.k-38 .k-widget-theme-site-logo a{display:block;line-height:0}
header.k-38 .k-widget-theme-site-logo img{width:190px}
header.k-38 .ls__cur:hover,header.k-38 .ls__cur:focus,header.k-38 .ls.is-open .ls__cur{background:#fff!important;color:#143852!important}
header.k-38 .k-nav-menu--main .btn_consulta_online>.k-item{font-weight:600}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010{background:transparent;box-shadow:inset 0 0 0 1px #008488}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a{color:#008488!important}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010:hover{background:#E9F5F5}
header.k-38 .k-nav-menu--main .btn_consulta_online.menu-item-9010>a:hover{color:#006d70!important}
@media(min-width:1280px) and (max-width:1439px){header.k-38 .k-widget-theme-site-logo img{width:164px}}
html[lang|=ru] header.k-38 .k-widget-theme-site-logo img,html[lang|=uk] header.k-38 .k-widget-theme-site-logo img{width:164px}
/* menú móvil/tablet (el kit fija colores con !important y 5 clases: hay que superar esa especificidad) */
@media(max-width:1439px){
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown{background:#fff!important;padding:6px 0 18px!important;border-top:1px solid #ECE7DF}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown>ul>li>a.k-item{justify-content:flex-start!important;padding:14px 24px!important;font-size:15px!important;font-weight:600!important;color:#172239!important;border-bottom:1px solid #F1EEE9!important;text-transform:none!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown .sub-menu{background:#F7F4EF!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown .sub-menu a.k-sub-item{justify-content:flex-start!important;padding:11px 24px 11px 36px!important;font-size:14px!important;font-weight:500!important;color:#2C3A52!important;text-transform:none!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown .sub-menu .sub-menu a.k-sub-item{padding-left:52px!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online{background:#008488!important;border-radius:10px!important;margin:14px 24px 0!important;box-shadow:none!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online>a.k-item{color:#fff!important;justify-content:center!important;border-bottom:0!important;padding:13px 20px!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online>a.k-item .sub-arrow svg{fill:#fff}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online.menu-item-9010{background:#fff!important;box-shadow:inset 0 0 0 1.5px #008488!important;margin-top:10px!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online.menu-item-9010>a.k-item{color:#008488!important}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online>.sub-menu{background:transparent!important;margin-top:4px}
header.k-38 .k-element.k-element-c45204a nav.k-nav-menu--dropdown li.btn_consulta_online>.sub-menu a.k-sub-item{color:#fff!important;justify-content:center!important;padding:8px 20px!important}
}
/* QA de render 30/09 (rastreo de las 1198 páginas en 390 y 1440 px): desbordes horizontales en 176 páginas móviles.
   Causas: márgenes negativos y anchos fijos del kit en móvil, tablas de 4 columnas, palabras largas (DE/NL/RU) y una rejilla
   de proceso fija. `overflow-x:clip` en html/body es la red de seguridad (clip no crea contenedor de scroll: la cabecera sticky sigue funcionando). */
html,body{overflow-x:clip}
.swiper,.swiper-container{overflow:hidden}
.tbl-scroll{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}
.tbl-scroll>table{margin-bottom:0}
@media(max-width:1024px){
.k .k-widget>.k-widget-container{margin-left:0!important;margin-right:0!important}
.k .k-widget{max-width:100%!important}
.k h1,.k h2,.k h3,.k h4,.k p,.k li,.k a,.k span,.k strong,.k em{overflow-wrap:anywhere}
.k td,.k th{overflow-wrap:normal}.tbl-scroll>table{min-width:560px}
.k .k-button{max-width:100%;box-sizing:border-box;white-space:normal}
.process-grid{grid-template-columns:1fr!important}.process-item{min-width:0}
}
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
