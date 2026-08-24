# Transparencia: qué es abierto y qué no

Nuestra transparencia trata de **cómo decide NelfePlay**, no de **cómo el listener extrae
la señal**. Es una distinción deliberada.

## La frontera de confianza
```
RetroArch
   │  ▼
NelfeMemoryListener  - CLOSED · HOMOLOGATED ----------------
   reads memory, resolves addresses, computes score+counters,
   emits raw checkpoints
   │  ▼  normalized event { score, counters, frame, time, event }
Open protocol (this repo)  - PUBLIC ------------------------
   ticket · JCS canonicalization · passport · signature · verify · submit
```
El código público sabe verificar la **continuidad** y **coherencia** de estos eventos;
**no** sabe cómo se obtuvieron.

## Por qué el listener es cerrado
La lógica de lectura de memoria es un saber-hacer costoso (una definición por juego,
revalidada en cada cambio de core). Abrirla la daría a la competencia **y** facilitaría
la trampa. La mantenemos cerrada - como el firmware de un instrumento de medición.

## Lo que el cierre NO es
El cierre **no forma parte de la seguridad** (principio de Kerckhoffs). La seguridad del
sistema se basa **solo** en el secreto de la **clave de firma de la máquina** - nunca en
reglas secretas. Todas las reglas, controles y códigos de rechazo son **públicos**. Si el
código del listener se filtrara mañana, la garantía no cambiaría ni un ápice: viene de lo
abierto.

## El límite, con honestidad
El protocolo abierto **nunca probará matemáticamente** que el listener *leyó* la memoria.
Prueba, de forma verificable: que el **build homologado** (hash conocido) estaba
**presente**, **ligado al proceso correcto**, **sin modificar** durante la sesión; que
los eventos **no se alteraron** tras su emisión (firma); y que el servidor aplicó **las
reglas públicas**.

La confianza en la *medición* se basa por tanto en un listener **homologado, firmado,
versionado y auditado** - ver [Homologación](homologation.md).

## Lo que sigue 100% público
Formato del pasaporte · tickets · manifiesto · reglas de perfil · huellas permitidas ·
verificación de firmas · estados de envío · reglas de clasificación · **anclaje
OpenTimestamps en Bitcoin** · **códigos de rechazo** · el **verificador público** · los
**resultados de la suite de homologación** del listener.

## Una promesa que podemos cumplir
> «Las reglas y la verificación de NelfePlay son públicas y repetibles. La medición en
> memoria la hace un listener propietario homologado, firmado, versionado y auditado.»

No «hacer trampa es matemáticamente imposible» - sería falso para software en el PC del
jugador. Pero una garantía **precisa y exigible** vale más que una promesa inverificable.
