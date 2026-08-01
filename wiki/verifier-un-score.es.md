# Verificar una puntuación tú mismo

No tienes que creernos. Tres comprobaciones independientes.

## 1. Repetir el verificador sobre los vectores de prueba
Los **vectores** (`vectors/*.json`) son pares **(pasaporte, veredicto esperado)**. El
verificador público (`ref/`) debe devolver **exactamente** esos veredictos — el mismo
veredicto, byte a byte, en cada implementación (C#, PHP, C++…). Es el criterio de salida
del protocolo.

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 vectores con el veredicto esperado
```

## 2. Verificar la firma de un pasaporte
Cada pasaporte está **firmado** por la máquina (ECDSA P-256) sobre su **forma canónica**
(JSON Canonicalization Scheme, **RFC 8785**):

1. quita el campo `signature`;
2. canonicaliza el resto en JCS (claves ordenadas, sin espacios, escape mínimo);
3. verifica la firma (ASN.1 DER, base64url) con la clave pública del device
   (`key_id = SHA-256(SPKI DER)`).

La firma cubre **todo**: puntuación, huellas de core/contenido/MEM/listener, checkpoints,
ticket. Un byte cambiado después = firma inválida.

## 3. Verificar la anterioridad (anclaje blockchain)
Cada puntuación clasificada — y la **apertura** de cada juego — se agrupa en un árbol de
Merkle cuya raíz se ancla vía **OpenTimestamps en Bitcoin**. Con un cliente estándar,
cualquiera puede verificar, **sin nosotros**, que el dato existía **antes de un bloque de
Bitcoin dado**.

El anclaje prueba **anterioridad**, no veracidad: garantiza que un récord no se antedató
antes de la apertura, y que una retirada posterior **también** lleva sello temporal (la
historia crece, no se reescribe).

## Lo que las tres establecen juntas
| Comprobación | Qué prueba |
|---|---|
| Vectores | Las **reglas** aplicadas son exactamente las publicadas. |
| Firma | El pasaporte **no fue alterado** y viene de **esa máquina**. |
| Anclaje | El dato **existía antes** de un bloque Bitcoin — sin antedatar. |

Lo que no prueban: que el listener cerrado *leyó* la dirección correcta. Esa confianza
viene de la [homologación del listener](homologation.md).
