// ---------------------------------------------------------------------------
// 5) Datos (formato de Elementor: form_fields[...])
// ---------------------------------------------------------------------------
function limpiar(string $v): string { return trim(strip_tags($v)); }
$form_id = limpiar((string) ($_POST['form_id'] ?? ''));
$conf = FORMULARIOS[$form_id] ?? ['nombre' => 'Formulario web', 'para' => DESTINO_DEFECTO, 'asunto' => 'Nuevo mensaje desde clinicabelba.com', 'campos' => []];
$campos = is_array($_POST['form_fields'] ?? null) ? $_POST['form_fields'] : [];
$datos = [];
foreach ($campos as $k => $v) {
    if (is_array($v)) { $v = implode(', ', array_map('strval', $v)); }
    $datos[(string) $k] = limpiar((string) $v);
}
$pagina = limpiar((string) ($_POST['page'] ?? '/'));
if (!preg_match('~^/[^\s?#]*$~', $pagina)) { $pagina = '/'; }
$idioma = limpiar((string) ($_POST['lang'] ?? 'es'));
$email_usuario = '';
foreach ($datos as $v) { if (filter_var($v, FILTER_VALIDATE_EMAIL)) { $email_usuario = $v; break; } }
if (implode('', $datos) === '' && !$es_bot) { http_response_code(422); exit('Formulario vacío.'); }

$cuerpo = "Formulario: {$conf['nombre']} ({$form_id})\nPágina: https://" . DOMINIO_PERMITIDO . "{$pagina}\nIdioma: {$idioma}\n\n";
foreach ($datos as $k => $v) {
    $etq = $conf['campos'][$k] ?? $k;
    $cuerpo .= "{$etq}: {$v}\n";
}
$cuerpo .= "\nIP: {$ip}\nFecha: " . date('Y-m-d H:i:s') . "\n";

// ---------------------------------------------------------------------------
// 6) Envío
// ---------------------------------------------------------------------------
/*SMTP*/
$enviado = false;
if (!$es_bot) {
    $para = implode(', ', $conf['para'] ?: DESTINO_DEFECTO);
    $asunto = '=?UTF-8?B?' . base64_encode($conf['asunto']) . '?=';
    if ($SMTP_HOST && $SMTP_USER && $SMTP_PASS) {
        $enviado = smtp_enviar($SMTP_HOST, $SMTP_PORT, $SMTP_USER, $SMTP_PASS, $SMTP_SEGURIDAD, $SMTP_USER, $para, $asunto, $cuerpo, $email_usuario ?: null);
    }
    if (!$enviado) {
        $cab = 'From: ' . REMITENTE_DEFECTO . "\r\nContent-Type: text/plain; charset=UTF-8\r\n" . ($email_usuario ? "Reply-To: {$email_usuario}\r\n" : '');
        $enviado = @mail($para, $asunto, $cuerpo, $cab);
    }
    if (!$enviado) {
        error_log('form-handler: fallo de envío (' . $form_id . ' ' . $pagina . ')');
        // Último recurso para no perder el lead: se guarda fuera del document root.
        @file_put_contents(dirname(__DIR__) . '/secrets/leads-no-enviados.log',
            json_encode(['t' => date('c'), 'form' => $form_id, 'page' => $pagina, 'datos' => $datos], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND);
    }
}

// ---------------------------------------------------------------------------
// 7) Vuelta a la misma página (303)
// ---------------------------------------------------------------------------
header('Location: ' . $pagina . '?enviado=1', true, 303);
exit;
