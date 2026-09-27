#!/usr/bin/env python3
"""Genera public/form-handler.php a partir de la plantilla de la skill y de la configuración
de formularios de Elementor (migracion/forms_elementor.json, sacada del SQL)."""
import json
B = '/home/claude/belba'
TPL = '/root/.claude/skills/synced/cda2b152-b6b2-4e27-9ef1-c7f2e7529a97_6810d0a6-7c92-4367-a0e3-d22dc8af911f/migracion-wp-theliftv2/assets/form-handler.php'
F = json.load(open(B + '/migracion/forms_elementor.json'))
def php(s):
    return "'" + str(s).replace('\\', '\\\\').replace("'", "\\'") + "'"
rows = []
for fid, f in F.items():
    to = [f['email_to']] if f['email_to'] else []
    if f['actions'] == ['save-to-database']:
        to = sorted(set(to + ['info@clinicabelba.com']))
    campos = ', '.join('%s => %s' % (php(c[0]), php(c[2] or c[0])) for c in f['fields'] if c[0])
    asunto = f['email_subject'].replace('&quot;', '"')
    rows.append("    %s => ['nombre' => %s, 'para' => [%s], 'asunto' => %s, 'campos' => [%s]]," % (
        php(fid), php(f['form_name']), ', '.join(php(x) for x in to), php(asunto), campos))
cfg = '\n'.join(rows)
tpl = open(TPL).read()
rest = tpl[tpl.index("// ---------------------------------------------------------------------------\n// 1) Solo POST"):]
pre = rest[:rest.index("// ---------------------------------------------------------------------------\n// 5) Validación")]
smtp_fn = rest[rest.index("function smtp_enviar("):rest.index('$cuerpo = "Nuevo mensaje desde')]
smtp_fn = smtp_fn.replace('$escribir("RCPT TO:<{$para}>");\n    $leer();',
                          "foreach (array_map('trim', explode(',', $para)) as $dest) { $escribir(\"RCPT TO:<{$dest}>\"); $leer(); }")
head = open(B + '/scripts/form-handler.head.php').read().replace('/*FORMULARIOS*/', cfg)
tail = open(B + '/scripts/form-handler.tail.php').read().replace('/*SMTP*/', smtp_fn)
open(B + '/public/form-handler.php', 'w').write(head + pre + tail)
print('ok', len(rows), 'formularios')
