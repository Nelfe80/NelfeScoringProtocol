#!/usr/bin/env python3
import os
here=os.path.dirname(os.path.abspath(__file__)); LANGS=['fr','en','es','ja','zh','ko']
RECORDS="https://nelfeplay.com/records/megadrive/sonic-the-hedgehog/1cc/"; VERIFY="https://nelfeplay.com/verify/"
def write(page,lng,body):
    open(os.path.join(here, f"{page}.md" if lng=='fr' else f"{page}.{lng}.md"),'w',encoding='utf-8').write(body.strip()+"\n")
def chain(lng): return f"![](assets/chain-of-trust-{lng}.svg)"
IDX={
 'fr':f"""# NelfePlay — Scoring rétro certifié

**Enregistrer et classer le *vrai* score d'un jeu rétro, de façon vérifiable par
n'importe qui — sans que le serveur possède la ROM ni l'émulateur.**

[Les records certifiés →](records.md){{ .md-button .md-button--primary }}
[Vérifier un score →]({VERIFY}){{ .md-button }}

{chain('fr')}

## Le principe en une phrase
> Les **règles et la vérification** sont **publiques et rejouables**. La **mesure
> mémoire** est réalisée par un **listener propriétaire homologué, signé, versionné et
> audité**.

## Ce qui est public (ce dépôt)
Le **format du passeport** (`schemas/`) · l'**algorithme de vérification** (`ref/`, le
*CoreVerifier*, en plusieurs langages) · les **profils signés** (`manifest/`) · les
**vecteurs de test** rejouables (`vectors/`) · les **codes de refus**, les **règles de
classement**, la preuve d'**ancrage Bitcoin**.

## Trois façons de vérifier, sans nous faire confiance
1. **La signature** — chaque passeport est signé (ECDSA P-256) sur sa forme canonique
   (JCS, RFC 8785).
2. **Les vecteurs** — lancez le vérifieur public sur `vectors/*` : mêmes verdicts que nous.
3. **L'antériorité** — chaque score est ancré via **OpenTimestamps sur Bitcoin**.

## Aller plus loin
- [Les records certifiés — tout le process](records.md)
- [Transparence : ce qui est ouvert, ce qui ne l'est pas](transparence.md)
- [Vérifier un score soi-même](verifier-un-score.md)
- [Héberger le vérifieur](heberger-le-verifieur.md)
- [Homologation du listener](homologation.md)
""",
 'en':f"""# NelfePlay — Certified Retro Scoring

**Record and rank a retro game's *real* score, verifiable by anyone — without the
server holding the ROM or the emulator.**

[The certified records →](records.md){{ .md-button .md-button--primary }}
[Verify a score →]({VERIFY}){{ .md-button }}

{chain('en')}

## The principle, in one sentence
> The **rules and verification** are **public and replayable**. The **memory
> measurement** is performed by a **proprietary listener that is homologated, signed,
> versioned and audited**.

## What is public (this repo)
The **passport format** (`schemas/`) · the **verification algorithm** (`ref/`, the
*CoreVerifier*, in several languages) · the **signed profiles** (`manifest/`) · the
replayable **test vectors** (`vectors/`) · the **refusal codes**, **ranking rules**, and
the **Bitcoin anchoring** proof.

## Verify without trusting us
1. **Signature** — every passport is signed (ECDSA P-256) over its canonical form
   (JCS, RFC 8785).
2. **Vectors** — run the public verifier over `vectors/*`: the same verdicts we get.
3. **Anteriority** — every score is anchored via **OpenTimestamps on Bitcoin**.

## Go further
- [The certified records — the whole process](records.md)
- [Transparency: what is open, what is not](transparence.md)
- [Verify a score yourself](verifier-un-score.md)
- [Host the verifier](heberger-le-verifieur.md)
- [Listener homologation](homologation.md)
""",
 'es':f"""# NelfePlay — Puntuación retro certificada

**Registrar y clasificar la puntuación *real* de un juego retro, verificable por
cualquiera — sin que el servidor tenga la ROM ni el emulador.**

[Los récords certificados →](records.md){{ .md-button .md-button--primary }}
[Verificar una puntuación →]({VERIFY}){{ .md-button }}

{chain('es')}

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
1. **Firma** — cada pasaporte se firma (ECDSA P-256) sobre su forma canónica (JCS, RFC 8785).
2. **Vectores** — ejecuta el verificador público sobre `vectors/*`: los mismos veredictos.
3. **Anterioridad** — cada puntuación se ancla vía **OpenTimestamps en Bitcoin**.

## Ir más lejos
- [Los récords certificados — todo el proceso](records.md)
- [Transparencia: qué es abierto y qué no](transparence.md)
- [Verificar una puntuación tú mismo](verifier-un-score.md)
- [Alojar el verificador](heberger-le-verifieur.md)
- [Homologación del listener](homologation.md)
""",
 'ja':f"""# NelfePlay — 認証レトロスコアリング

**レトロゲームの*本当の*スコアを記録・ランク付けし、誰でも検証可能に — サーバーは ROM も
エミュレータも持ちません。**

[認証された記録 →](records.md){{ .md-button .md-button--primary }}
[スコアを検証 →]({VERIFY}){{ .md-button }}

{chain('ja')}

## 一文で言えば
> **ルールと検証は公開・再現可能**。**メモリ計測**は、**認定・署名・版管理・監査**された
> **専有リスナー**が行う。

## 公開されているもの（本リポジトリ）
**パスポート形式**（`schemas/`）・**検証アルゴリズム**（`ref/`、複数言語の *CoreVerifier*）
・**署名済みプロファイル**（`manifest/`）・再現可能な**テストベクタ**（`vectors/`）・
**却下コード**、**ランキング規則**、**Bitcoin アンカー**の証明。

## 私たちを信用せず検証する
1. **署名** — 各パスポートは正規形（JCS, RFC 8785）に対して署名（ECDSA P-256）。
2. **ベクタ** — `vectors/*` に公開検証ツールを実行：私たちと同じ判定。
3. **先行性** — 各スコアは **OpenTimestamps で Bitcoin** にアンカー。

## さらに詳しく
- [認証された記録 — 全プロセス](records.md)
- [透明性：何が公開で何が非公開か](transparence.md)
- [自分でスコアを検証](verifier-un-score.md)
- [検証ツールをホスト](heberger-le-verifieur.md)
- [リスナーの認定](homologation.md)
""",
 'zh':f"""# NelfePlay — 认证复古计分

**记录并排名复古游戏的*真实*分数，任何人皆可验证 —— 服务器既不持有 ROM 也不持有模拟器。**

[认证记录 →](records.md){{ .md-button .md-button--primary }}
[验证分数 →]({VERIFY}){{ .md-button }}

{chain('zh')}

## 一句话原则
> **规则与验证公开且可重放**。**内存测量**由一个**已认证、已签名、有版本、经审计**的
> **专有监听器**完成。

## 公开的内容（本仓库）
**护照格式**（`schemas/`）· **验证算法**（`ref/`，多语言 *CoreVerifier*）· **已签名的配置
文件**（`manifest/`）· 可重放的**测试向量**（`vectors/`）· **拒绝码**、**排名规则** 与
**Bitcoin 锚定**证明。

## 无需信任我们即可验证
1. **签名** —— 每份护照对其规范形式（JCS, RFC 8785）签名（ECDSA P-256）。
2. **向量** —— 对 `vectors/*` 运行公开验证器：与我们相同的裁决。
3. **先后性** —— 每个分数都通过 **OpenTimestamps 锚定于 Bitcoin**。

## 深入了解
- [认证记录 —— 全过程](records.md)
- [透明度：何为开放，何为不开放](transparence.md)
- [亲自验证一个分数](verifier-un-score.md)
- [自行托管验证器](heberger-le-verifieur.md)
- [监听器认证](homologation.md)
""",
 'ko':f"""# NelfePlay — 인증 레트로 스코어링

**레트로 게임의 *진짜* 점수를 기록·순위 매기고 누구나 검증 가능 — 서버는 ROM도 에뮬레이터도
갖지 않습니다.**

[인증된 기록 →](records.md){{ .md-button .md-button--primary }}
[점수 검증 →]({VERIFY}){{ .md-button }}

{chain('ko')}

## 한 문장 원칙
> **규칙과 검증은 공개·재현 가능**. **메모리 측정**은 **인증·서명·버전 관리·감사**된
> **독점 리스너**가 수행.

## 공개되는 것 (이 저장소)
**패스포트 형식**(`schemas/`) · **검증 알고리즘**(`ref/`, 여러 언어의 *CoreVerifier*) ·
**서명된 프로필**(`manifest/`) · 재현 가능한 **테스트 벡터**(`vectors/`) · **거부 코드**,
**순위 규칙**, **Bitcoin 앵커링** 증명.

## 우리를 믿지 않고 검증
1. **서명** — 각 패스포트는 정규형(JCS, RFC 8785)에 서명(ECDSA P-256).
2. **벡터** — `vectors/*`에 공개 검증기 실행: 우리와 동일한 판정.
3. **선후성** — 각 점수는 **OpenTimestamps로 Bitcoin에** 앵커.

## 더 알아보기
- [인증된 기록 — 전체 프로세스](records.md)
- [투명성: 무엇이 공개이고 무엇이 아닌가](transparence.md)
- [직접 점수 검증](verifier-un-score.md)
- [검증기 호스팅](heberger-le-verifieur.md)
- [리스너 인증](homologation.md)
""",
}
for lng in LANGS:
    write('index',lng,IDX[lng]); print('index',lng)
