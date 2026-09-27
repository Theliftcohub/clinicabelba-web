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
/*FORMULARIOS*/
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

