# NelfePlay - Puntuación retro certificada

**Registrar y clasificar la puntuación *real* de un juego retro, verificable por
cualquiera - sin que el servidor tenga la ROM ni el emulador.**

[Los récords certificados →](records.md){ .md-button .md-button--primary }
[Verificar una puntuación →](https://nelfeplay.com/verify/){ .md-button }

![](assets/chain-of-trust-es.svg)

## El principio, en una frase
> Las **reglas y la verificación** son **públicas y repetibles**. La **medición en
> memoria** la realiza un **listener propietario homologado, firmado, versionado y
> auditado**.

## Lo que es público (este repositorio)
El **formato del pasaporte** (`schemas/`) · el **algoritmo de verificación** (`ref/`, el
*CoreVerifier*, en varios lenguajes) · los **perfiles firmados** (`manifest/`) · los
**vectores de prueba** repetibles (`vectors/`) · los **códigos de rechazo**, las **reglas
de clasificación** y la prueba de **anclaje en Bitcoin**.

## Verificar sin confiar en nosotros
1. **Firma** - cada pasaporte se firma (ECDSA P-256) sobre su forma canónica (JCS, RFC 8785).
2. **Vectores** - ejecuta el verificador público sobre `vectors/*`: los mismos veredictos.
3. **Anterioridad** - cada puntuación se ancla vía **OpenTimestamps en Bitcoin**.

## Ir más lejos
- [Los récords certificados - todo el proceso](records.md)
- [Transparencia: qué es abierto y qué no](transparence.md)
- [Verificar una puntuación tú mismo](verifier-un-score.md)
- [Alojar el verificador](heberger-le-verifieur.md)
- [Homologación del listener](homologation.md)
