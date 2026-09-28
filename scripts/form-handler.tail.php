// ---------------------------------------------------------------------------
// 5) Datos: formularios nativos (campos sueltos) y los de Elementor (form_fields[...])
// ---------------------------------------------------------------------------
function limpiar(string $v): string { return trim(strip_tags($v)); }
$SISTEMA = ['form_id', 'form_name', 'page', 'lang', 'post_id', HONEYPOT_FIELD, 'form_fields', 'lead_ref'];
$ATRIB = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ad_id', 'adgroup_id',
          'campaign_id', 'first_source', 'first_medium', 'first_landing', 'first_referrer', 'first_ts', 'referrer', 'landing', 'ga_client_id'];
$form_id = limpiar((string) ($_POST['form_id'] ?? ''));
$form_key = preg_replace('/^el-/', '', $form_id);
// Segunda fase de un formulario corto (pregunta de cualificación tras dejar nombre y teléfono): mismo formulario, tipo 'cualificacion'
$es_cualif = (bool) preg_match('/-cualificacion$/', $form_key);
$form_key = preg_replace('/-cualificacion$/', '', $form_key);
// Identificador que une las dos fases del mismo lead en n8n/Kommo
$lead_ref = substr(preg_replace('/[^A-Za-z0-9-]/', '', (string) ($_POST['lead_ref'] ?? '')), 0, 40);
$conf = FORMULARIOS[$form_key] ?? ['nombre' => limpiar((string) ($_POST['form_name'] ?? 'Formulario web')), 'para' => DESTINO_DEFECTO, 'asunto' => 'Nuevo lead desde clinicabelba.com', 'campos' => []];
$datos = [];
if (is_array($_POST['form_fields'] ?? null)) {
    foreach ($_POST['form_fields'] as $k => $v) {
        if (is_array($v)) { $v = implode(', ', array_map('strval', $v)); }
        $datos[(string) $k] = limpiar((string) $v);
    }
}
$atribucion = [];
foreach ($_POST as $k => $v) {
    if (in_array($k, $SISTEMA, true) || is_array($v)) { continue; }
    if (in_array($k, $ATRIB, true)) { $atribucion[$k] = limpiar((string) $v); continue; }
    $datos[(string) $k] = limpiar((string) $v);
}
$pagina = limpiar((string) ($_POST['page'] ?? '/'));
if (!preg_match('~^/[^\s?#]*$~', $pagina)) { $pagina = '/'; }
$idioma = limpiar((string) ($_POST['lang'] ?? 'es'));
$email_usuario = '';
foreach ($datos as $v) { if (filter_var($v, FILTER_VALIDATE_EMAIL)) { $email_usuario = $v; break; } }
$quiere_json = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
function responder(bool $ok, bool $json, string $pagina): void {
    if ($json) { header('Content-Type: application/json; charset=utf-8'); echo json_encode(['ok' => $ok]); exit; }
    header('Location: ' . $pagina . ($ok ? '?enviado=1' : '?error=1'), true, 303); exit;
}
if (implode('', $datos) === '' && !$es_bot) { http_response_code(422); responder(false, $quiere_json, $pagina); }

$lead = [
    'form_id' => $form_id, 'form_name' => $conf['nombre'], 'tipo' => $es_cualif ? 'cualificacion' : 'lead', 'lead_ref' => $lead_ref,
    'page' => 'https://' . DOMINIO_PERMITIDO . $pagina,
    'lang' => $idioma, 'datos' => $datos, 'atribucion' => $atribucion, 'ip' => $ip, 'user_agent' => substr((string) ($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 250),
    'fecha' => date('c'), 'destinatarios' => $conf['para'],
];

// ---------------------------------------------------------------------------
// 6) Envío: 1º n8n (webhook fuera del repo, en secrets); si falla o no está, email
// ---------------------------------------------------------------------------
$N8N_URL = getenv('N8N_WEBHOOK_URL') ?: (defined('N8N_WEBHOOK_URL') ? N8N_WEBHOOK_URL : null);
$N8N_TOKEN = getenv('N8N_WEBHOOK_TOKEN') ?: (defined('N8N_WEBHOOK_TOKEN') ? N8N_WEBHOOK_TOKEN : null);
function n8n_enviar(string $url, ?string $token, array $lead): bool {
    $cuerpo = json_encode($lead, JSON_UNESCAPED_UNICODE);
    $cab = "Content-Type: application/json\r\n" . ($token ? "X-Belba-Token: {$token}\r\n" : '');
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => $cab, 'content' => $cuerpo, 'timeout' => 8, 'ignore_errors' => true]]);
    $r = @file_get_contents($url, false, $ctx);
    $st = 0;
    if (isset($http_response_header[0]) && preg_match('~\s(\d{3})\s~', $http_response_header[0], $m)) { $st = (int) $m[1]; }
    if ($st < 200 || $st >= 300) { error_log("form-handler n8n: HTTP {$st}"); return false; }
    return true;
}
/*SMTP*/
$enviado = false;
if (!$es_bot) {
    if ($N8N_URL) { $enviado = n8n_enviar($N8N_URL, $N8N_TOKEN, $lead); }
    if (!$enviado) {
        $cuerpo = "Formulario: {$conf['nombre']} ({$form_id})\nTipo: {$lead['tipo']}\nReferencia del lead: {$lead_ref}\nPágina: {$lead['page']}\nIdioma: {$idioma}\n\n";
        foreach ($datos as $k => $v) { $cuerpo .= (($conf['campos'][$k] ?? $k)) . ": {$v}\n"; }
        $cuerpo .= "\n--- Origen del lead ---\n";
        foreach ($atribucion as $k => $v) { if ($v !== '') { $cuerpo .= "{$k}: {$v}\n"; } }
        $cuerpo .= "\nIP: {$ip}\nFecha: " . date('Y-m-d H:i:s') . "\n";
        $para = implode(', ', $conf['para'] ?: DESTINO_DEFECTO);
        $asunto = '=?UTF-8?B?' . base64_encode(($es_cualif ? 'Cualificación · ' : '') . $conf['asunto']) . '?=';
        if ($SMTP_HOST && $SMTP_USER && $SMTP_PASS) {
            $enviado = smtp_enviar($SMTP_HOST, $SMTP_PORT, $SMTP_USER, $SMTP_PASS, $SMTP_SEGURIDAD, $SMTP_USER, $para, $asunto, $cuerpo, $email_usuario ?: null);
        }
        if (!$enviado) {
            $cab = 'From: ' . REMITENTE_DEFECTO . "\r\nContent-Type: text/plain; charset=UTF-8\r\n" . ($email_usuario ? "Reply-To: {$email_usuario}\r\n" : '');
            $enviado = @mail($para, $asunto, $cuerpo, $cab);
        }
    }
    if (!$enviado) {
        error_log('form-handler: fallo de envío (' . $form_id . ' ' . $pagina . ')');
        @file_put_contents(dirname(__DIR__) . '/secrets/leads-no-enviados.log', json_encode($lead, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND);
        $enviado = true; // el lead queda guardado: al usuario se le confirma igualmente
    }
}
responder(true, $quiere_json, $pagina);
