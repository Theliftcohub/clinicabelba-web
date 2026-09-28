#!/usr/bin/env python3
"""Genera public/css/site.css (CSS local renombrado + fuentes locales) y copia las fuentes."""
import os, re, shutil, glob, sys
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
'''

def main():
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
