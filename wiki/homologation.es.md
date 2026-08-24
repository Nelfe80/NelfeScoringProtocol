# Homologación del listener

El listener (`NelfeMemoryListener`) es el componente cerrado que **mide** la puntuación
en memoria. Su credibilidad no viene de su código (secreto), sino de su
**homologación** - como el firmware cerrado de un instrumento de medición (analogía
**técnica**, no una afirmación regulatoria).

## Vocabulario (preciso)
- **Homologado NelfePlay**: cada build oficial está firmado y atestiguado por el editor.
- **Auditado**: se dice solo cuando una auditoría externa independiente **realmente**
  tuvo lugar.
- **Certificado**: reservado a un programa de certificación formal (organismo acreditado).
  No lo usamos mientras no exista tal programa.

## Ficha pública de un build
Cada versión del listener publica:
```json
{
  "listener_build": "4.2.0",
  "sha256": "…",
  "publisher_signature": "…",
  "released_at": "…",
  "supported_protocol": 1,
  "homologation_suite": "listener-tests-2026.1",
  "audit_report": "…",
  "status": "authorized"
}
```
Cada **perfil de scoring** referencia los builds autorizados (`allowed_listener_sha256`).
El **pasaporte** lleva el hash del listener **antes / cargado / después** - medido
**independientemente por el componente abierto** (no por el propio listener, para evitar
la auto-atestación).

## Suite de homologación (caja negra, pública)
Se puede probar el comportamiento **sin revelar el algoritmo**:
> ROM X + escenario Y → la puntuación en pantalla es **12 500** → el listener oficial debe
> producir **12 500**.

Los resultados son públicos; la dirección de memoria y cómo se lee, no.

## Revocación
¿Un fallo en un build? **Revocamos ese build para nuevas partidas** (`status: revoked`)
sin volver ilegibles los scores antiguos: siguen verificables con el perfil y build
históricos.

## Hacia acreditar el componente cerrado
Binario firmado · **SHA-256 público** por build · **auditoría externa bajo NDA** con
**informe público sin código** · **SBOM** pública · **depósito** del fuente opcional ·
**pruebas de comportamiento públicas** · **política de revocación** · **historial de
versiones** · **programa de divulgación de vulnerabilidades**.

## El límite, otra vez
Nada de esto prueba *matemáticamente* que el listener leyó la dirección correcta.
Establece que un build **homologado, sin modificar** estaba **ligado al proceso correcto**
y que se aplicaron las **reglas públicas**. La confianza en la medición se basa en la
homologación - una base defendible, la misma que los instrumentos de medición reales.
