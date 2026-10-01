<?php
/**
 * form-handler.php — Clínica Belba. Sustituye a los formularios de Elementor Pro del WordPress.
 * Generado por scripts/build_form_handler.py (no editar a mano: cambia la configuración y regenera).
 * - Destinatarios y asunto por formulario (form_id de Elementor), copiados de la configuración del WordPress.
 * - Campos form_fields[...] como en Elementor, con sus etiquetas en el email.
 * - Tras enviar: 303 a la misma página con ?enviado=1 (Elementor mostraba el mensaje en la misma página).
 * - SMTP fuera del repositorio: ../secrets/smtp.php (un nivel por encima de httpdocs) o variables de entorno.
 */
declare(strict_types=1);

const DOMINIO_PERMITIDO   = 'clinicabelba.com';
const HONEYPOT_FIELD      = 'website';
const MAX_ENVIOS_POR_VENTANA = 5;
const VENTANA_SEGUNDOS       = 600;
const REMITENTE_DEFECTO      = 'info@clinicabelba.com';
const DESTINO_DEFECTO        = ['info@clinicabelba.com'];
const FORMULARIOS = [
    'aa3e4c7' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    'e2de0b0' => ['nombre' => 'New Form', 'para' => ['alejandro@theliftco.eu', 'info@clinicabelba.com'], 'asunto' => 'New message from "Clinica Belba"', 'campos' => ['name' => 'name', 'email' => 'email']],
    '5ff55c52' => ['nombre' => 'New Form', 'para' => ['nicols@theliftco.eu'], 'asunto' => 'Consulta ginecomastia — más información', 'campos' => ['name' => 'Nombre', 'tel' => 'Teléfono']],
    'a3aa38a' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '4cdb1f81' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '7669add9' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '2892be87' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '3e5f3c7e' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '4aba9df7' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '7d6b6661' => ['nombre' => 'Consulta online', 'para' => ['info@clinicabelba.com'], 'asunto' => 'Nuevo mensaje desde Consulta Online', 'campos' => ['name' => 'Nombre', 'field_384dfb5' => 'Apellidos', 'email' => 'Email', 'field_9d6e8f4' => 'Teléfono', 'field_abf2e61' => 'Elige al doctor', 'message' => 'Mensaje', 'field_5ada86d' => 'field_5ada86d']],
    '75a0c2af' => ['nombre' => 'New Form', 'para' => ['alejandro@theliftco.eu'], 'asunto' => 'New message from "Clinica Belba"', 'campos' => ['name' => 'name', 'email' => 'email']],
    '7cb4277f' => ['nombre' => 'New Form', 'para' => ['alejandro@theliftco.eu'], 'asunto' => 'New message from "Clinica Belba"', 'campos' => ['name' => 'name', 'email' => 'email']],
];

$smtp_config_externo = dirname(__DIR__) . '/secrets/smtp.php';
if (is_readable($smtp_config_externo)) {
    require $smtp_config_externo; // define SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_SEGURIDAD
}
$SMTP_HOST = getenv('SMTP_HOST') ?: (defined('SMTP_HOST') ? SMTP_HOST : null);
$SMTP_PORT = (int) (getenv('SMTP_PORT') ?: (defined('SMTP_PORT') ? SMTP_PORT : 587));
$SMTP_USER = getenv('SMTP_USER') ?: (defined('SMTP_USER') ? SMTP_USER : null);
$SMTP_PASS = getenv('SMTP_PASS') ?: (defined('SMTP_PASS') ? SMTP_PASS : null);
$SMTP_SEGURIDAD = getenv('SMTP_SEGURIDAD') ?: (defined('SMTP_SEGURIDAD') ? SMTP_SEGURIDAD : 'tls');

// ---------------------------------------------------------------------------
// 1) Solo POST
// ---------------------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    exit('Método no permitido.');
}

// ---------------------------------------------------------------------------
// 2) Origen: Origin (o Referer si falta) debe ser del propio dominio
// ---------------------------------------------------------------------------
function origen_valido(): bool
{
    $origen = $_SERVER['HTTP_ORIGIN'] ?? '';
    $referer = $_SERVER['HTTP_REFERER'] ?? '';
    $candidato = $origen ?: $referer;
    if ($candidato === '') {
        return false; // sin Origin ni Referer: probablemente no viene de un navegador real
    }
    $host = parse_url($candidato, PHP_URL_HOST) ?? '';
    $host = strtolower(preg_replace('/^www\./', '', $host));
    return $host === strtolower(DOMINIO_PERMITIDO);
}

if (!origen_valido()) {
    http_response_code(403);
    exit('Origen no permitido.');
}

// ---------------------------------------------------------------------------
// 3) Honeypot: si el campo trampa viene relleno, es un bot. Respondemos "bien" sin enviar nada.
// ---------------------------------------------------------------------------
$es_bot = trim((string) ($_POST[HONEYPOT_FIELD] ?? '')) !== '';

// ---------------------------------------------------------------------------
// 4) Límite básico por IP (best-effort, archivo temporal)
// ---------------------------------------------------------------------------
function limite_superado(string $ip): bool
{
    $archivo = sys_get_temp_dir() . '/formhandler_' . md5($ip) . '.json';
    $ahora = time();
    $envios = [];
    if (is_readable($archivo)) {
        $envios = json_decode((string) file_get_contents($archivo), true) ?: [];
    }
    $envios = array_values(array_filter($envios, fn($t) => $ahora - $t < VENTANA_SEGUNDOS));
    if (count($envios) >= MAX_ENVIOS_POR_VENTANA) {
        return true;
    }
    $envios[] = $ahora;
    @file_put_contents($archivo, json_encode($envios));
    return false;
}

$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
if (!$es_bot && limite_superado($ip)) {
    http_response_code(429);
    exit('Demasiados envíos. Inténtalo más tarde.');
}

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
// Webhook genérico (n8n, Make o cualquier servicio que reciba JSON por POST): WEBHOOK_URL / WEBHOOK_TOKEN, o los nombres antiguos N8N_*
$N8N_URL = getenv('WEBHOOK_URL') ?: getenv('N8N_WEBHOOK_URL') ?: (defined('WEBHOOK_URL') ? WEBHOOK_URL : (defined('N8N_WEBHOOK_URL') ? N8N_WEBHOOK_URL : null));
$N8N_TOKEN = getenv('WEBHOOK_TOKEN') ?: getenv('N8N_WEBHOOK_TOKEN') ?: (defined('WEBHOOK_TOKEN') ? WEBHOOK_TOKEN : (defined('N8N_WEBHOOK_TOKEN') ? N8N_WEBHOOK_TOKEN : null));
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
function smtp_enviar(string $host, int $port, string $usuario, string $clave, string $seguridad,
                      string $de, string $para, string $asunto, string $cuerpo, ?string $responder_a = null): bool
{
    $transporte = $seguridad === 'ssl' ? "ssl://{$host}" : $host;
    $fp = @stream_socket_client("{$transporte}:{$port}", $errno, $errstr, 15);
    if (!$fp) {
        error_log("form-handler SMTP: no se pudo conectar a {$host}:{$port} ({$errstr})");
        return false;
    }
    $leer = function () use ($fp) {
        $linea = fgets($fp, 512);
        return $linea === false ? '' : $linea;
    };
    $escribir = function (string $cmd) use ($fp) {
        fwrite($fp, $cmd . "\r\n");
    };
    $leer();
    $escribir('EHLO ' . DOMINIO_PERMITIDO);
    $leer();
    if ($seguridad === 'tls') {
        $escribir('STARTTLS');
        $leer();
        stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
        $escribir('EHLO ' . DOMINIO_PERMITIDO);
        $leer();
    }
    $escribir('AUTH LOGIN');
    $leer();
    $escribir(base64_encode($usuario));
    $leer();
    $escribir(base64_encode($clave));
    $resp = $leer();
    if (strpos($resp, '235') !== 0) {
        error_log('form-handler SMTP: autenticación rechazada');
        fclose($fp);
        return false;
    }
    $escribir("MAIL FROM:<{$de}>");
    $leer();
    foreach (array_map('trim', explode(',', $para)) as $dest) { $escribir("RCPT TO:<{$dest}>"); $leer(); }
    $escribir('DATA');
    $leer();
    $cabeceras = "From: {$de}\r\nTo: {$para}\r\nSubject: {$asunto}\r\n"
        . ($responder_a ? "Reply-To: {$responder_a}\r\n" : '')
        . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n";
    $escribir($cabeceras . $cuerpo . "\r\n.");
    $resp = $leer();
    $escribir('QUIT');
    fclose($fp);
    return strpos($resp, '250') === 0;
}


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
