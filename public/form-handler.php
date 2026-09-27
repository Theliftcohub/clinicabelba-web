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
