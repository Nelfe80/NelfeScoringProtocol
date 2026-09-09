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

## Homologación en el momento de la publicación

Una ficha de build no sirve de nada mientras la plataforma no la conozca. Mientras la
homologación fue un gesto manual, **cada nueva versión del listener invalidaba la flota**
hasta que alguien se acordaba de registrarla: las máquinas actualizadas veían rechazadas sus
puntuaciones por build desconocido, justo lo contrario del efecto buscado.

Por eso el manifiesto se **publica junto al binario**, firmado, y la plataforma va a leerlo:

```json
{
  "built_at": "2026-09-05T21:13:53Z",
  "sha256": "1bd08a9d5d9aaac16692eab6f52278b3f072a143c20436271883d28025034e75",
  "signature": "MEUCIQD5QTn8FMBbiLBZKXLL9P_-1_f6cQAtiLFv9vphxYmqtQIgGdTPvOkMoF5EbwCiSCsBNu_IMJY94d6vGr_Fl60WPRI",
  "subject": "CN=nelfeTech",
  "version": "0.334.0.0"
}
```

La firma es **ECDSA P-256 / SHA-256** sobre el cuerpo canonicalizado (RFC 8785), transportada
en base64url. La plataforma la verifica contra una **clave pública fijada en su propio
código**, nunca contra una clave suministrada por el manifiesto: sin ese anclaje, cualquiera
que publicase un archivo con el formato correcto conseguiría homologar su propio binario.

Tres propiedades de esta elección merecen decirse:

- **El manifiesto se recoge, no se envía.** La plataforma consulta una URL pública a intervalos
  regulares. Cualquiera puede leer el mismo archivo y rehacer la misma verificación, lo que
  hace la homologación observable desde fuera.
- **Un build nunca desaparece solo.** La automatización añade, no retira.
- **La revocación sigue siendo un acto deliberado** (véase más abajo) y prevalece sobre la
  publicación: un build retirado no se vuelve a homologar por seguir estando en línea.

Como este archivo es el anclaje de toda la flota, debe ser **producido por la propia cadena de
firma**, nunca escrito a mano: un manifiesto que anunciara una versión sin corresponder al
binario firmado homologaría una huella inexistente, y todas las máquinas actualizadas caerían
de golpe.

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
