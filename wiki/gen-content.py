#!/usr/bin/env python3
# Génère les pages wiki en 6 langues (suffixe i18n : page.md=fr, page.<lng>.md).
# Pages « riches » (records, héberger, index) écrites ici ; les pages protocole
# existantes (transparence, verifier-un-score, homologation) sont traduites par
# gen-protocol.py.
import os
here = os.path.dirname(os.path.abspath(__file__))
LANGS = ['fr','en','es','ja','zh','ko']

RECORDS = "https://nelfeplay.com/records/megadrive/sonic-the-hedgehog/1cc/"
VERIFY  = "https://nelfeplay.com/verify/"
PACK    = "https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer"

def write(page, lng, body):
    name = f"{page}.md" if lng=='fr' else f"{page}.{lng}.md"
    open(os.path.join(here,name),'w',encoding='utf-8').write(body.strip()+"\n")

# ── PAGE « records » (le cœur : screenshots + schéma + tout le process) ──────────
def records(lng):
    chain = f"![]({{}})".format(f"assets/chain-of-trust-{lng}.svg")
    shot_b = "![](assets/shots/records.png)"
    shot_c = "![](assets/shots/certificate.png)"
    shot_v = "![](assets/shots/verify.png)"
    T = {
     'fr':f"""# Les records certifiés

Un **classement public** de scores rétro que **personne ne peut truquer** - et que
**n'importe qui peut vérifier**, sans nous faire confiance. Voici tout ce qui se passe,
de la partie jouée jusqu'à la preuve sur Bitcoin.

[Voir le classement en direct →]({RECORDS}){{ .md-button .md-button--primary }}
[Vérifier soi-même →]({VERIFY}){{ .md-button }}

## La chaîne de confiance, d'un coup d'œil

{chain}

Chaque étape est **soit publique et rejouable, soit homologuée et signée**. La sécurité
ne repose **jamais** sur un secret (principe de Kerckhoffs) - seulement sur l'ouvert.

## 1 · Mesuré, pas déclaré
Le score n'est **pas envoyé par le jeu**. Un **composant homologué** (le *listener*) lit
la valeur directement dans la mémoire de l'émulateur, à la source, avec des *checkpoints*
horodatés. Aucun score « déclaré » n'entre dans le système.

## 2 · Signé sur la machine
La borne assemble un **passeport de session** (score, empreintes du core/dump/listener,
checkpoints, ticket) et le **signe** avec une clé matérielle **non exportable**
(ECDSA P-256). Un octet modifié après coup = signature invalide.

## 3 · Vérifié côté serveur
Le serveur **ne rejoue pas le jeu** : il applique des **règles publiques** (le
*CoreVerifier*, open source) - empreintes attendues, monotonie de la trajectoire, fin de
partie, ticket valide - puis rend un verdict **publié**, **retenu** (anomalie statistique,
jamais un refus sec) ou **refusé**. Zéro arbitre humain.

## 4 · Publié dans un index signé
Les scores publiés forment un **index signé** : la liste complète + une **empreinte
SHA-256** signée par l'émetteur. C'est cet index qui reconstruit le classement - et qui
rend une perte de base **sans conséquence** (il est reconstructible et miroitable).

{shot_b}

## 5 · Scellé sur Bitcoin
L'empreinte de l'index est **horodatée sur Bitcoin** via **OpenTimestamps**. Une fois
confirmée, elle prouve que les records **existaient avant un bloc donné** - antériorité
**immuable**. Un score fraîchement scellé s'affiche en **or** ; la preuve `.ots` est
téléchargeable et vérifiable avec le client OpenTimestamps standard.

## 6 · Le Certificat de record
Chaque score a une page **immuable et partageable** : score, empreintes du dump
(MD5 + SHA-256), signature ✓, et le **sceau Bitcoin** (bloc). Pas de rang dessus - le
rang vit sur le classement.

{shot_c}

## 7 · Vérifiable sans nous faire confiance
Le **vérifieur public** recalcule l'empreinte, **vérifie la signature** (Web Crypto) et
lit l'état de scellement - **dans votre navigateur**. Il ne prend rien pour argent
comptant. Vous pouvez même l'**héberger vous-même**.

{shot_v}

[Vérifier maintenant →]({VERIFY}){{ .md-button .md-button--primary }}
[Héberger le vérifieur →](heberger-le-verifieur.md){{ .md-button }}

## La limite, dite honnêtement
Le protocole ouvert **ne prouve pas mathématiquement** que le listener fermé a *lu* la
bonne adresse. Il prouve que le **build homologué était présent, lié au bon processus,
non modifié**, et que les **règles publiques ont été appliquées**. La confiance dans la
*mesure* vient d'un listener **homologué, signé, versionné, audité** - voir
[Transparence](transparence.md) et [Homologation](homologation.md).
""",
     'en':f"""# Certified records

A **public leaderboard** of retro scores that **nobody can fake** - and that **anyone
can verify**, without trusting us. Here is everything that happens, from the game played
to the proof on Bitcoin.

[See the live leaderboard →]({RECORDS}){{ .md-button .md-button--primary }}
[Verify it yourself →]({VERIFY}){{ .md-button }}

## The chain of trust, at a glance

{chain}

Every step is **either public and replayable, or homologated and signed**. Security
**never** rests on a secret (Kerckhoffs' principle) - only on the open.

## 1 · Measured, not declared
The score is **not sent by the game**. A **homologated component** (the *listener*) reads
the value straight from the emulator's memory, at the source, with timestamped
*checkpoints*. No "declared" score ever enters the system.

## 2 · Signed on the machine
The cabinet assembles a **session passport** (score, core/dump/listener fingerprints,
checkpoints, ticket) and **signs** it with a **non-exportable** hardware key
(ECDSA P-256). One byte changed afterwards = invalid signature.

## 3 · Verified server-side
The server **does not replay the game**: it applies **public rules** (the open-source
*CoreVerifier*) - expected fingerprints, trajectory monotonicity, game end, valid ticket
- then returns a verdict: **published**, **held** (statistical anomaly, never a hard
refusal) or **refused**. No human referee.

## 4 · Published in a signed index
Published scores form a **signed index**: the full list + a **SHA-256 fingerprint**
signed by the issuer. This index rebuilds the leaderboard - and makes a database loss
**inconsequential** (it is rebuildable and mirrorable).

{shot_b}

## 5 · Sealed on Bitcoin
The index fingerprint is **timestamped on Bitcoin** via **OpenTimestamps**. Once
confirmed, it proves the records **existed before a given block** - **immutable**
priority. A freshly sealed score shows in **gold**; the `.ots` proof is downloadable and
verifiable with the standard OpenTimestamps client.

## 6 · The record certificate
Each score has an **immutable, shareable** page: score, dump fingerprints
(MD5 + SHA-256), signature ✓, and the **Bitcoin seal** (block). No rank on it - the rank
lives on the leaderboard.

{shot_c}

## 7 · Verifiable without trusting us
The **public verifier** recomputes the fingerprint, **verifies the signature** (Web
Crypto) and reads the seal state - **in your browser**. It takes nothing at face value.
You can even **host it yourself**.

{shot_v}

[Verify now →]({VERIFY}){{ .md-button .md-button--primary }}
[Host the verifier →](heberger-le-verifieur.md){{ .md-button }}

## The honest limit
The open protocol **does not mathematically prove** the closed listener *read* the right
address. It proves the **homologated build was present, bound to the right process,
unmodified**, and that the **public rules were applied**. Trust in the *measurement*
comes from a listener that is **homologated, signed, versioned, audited** - see
[Transparency](transparence.md) and [Homologation](homologation.md).
""",
     'es':f"""# Récords certificados

Una **clasificación pública** de puntuaciones retro que **nadie puede falsificar** - y
que **cualquiera puede verificar**, sin confiar en nosotros. Esto es todo lo que ocurre,
desde la partida jugada hasta la prueba en Bitcoin.

[Ver la clasificación en vivo →]({RECORDS}){{ .md-button .md-button--primary }}
[Verificar tú mismo →]({VERIFY}){{ .md-button }}

## La cadena de confianza, de un vistazo

{chain}

Cada paso es **público y repetible, o homologado y firmado**. La seguridad **nunca** se
basa en un secreto (principio de Kerckhoffs) - solo en lo abierto.

## 1 · Medido, no declarado
La puntuación **no la envía el juego**. Un **componente homologado** (el *listener*) lee
el valor directamente en la memoria del emulador, en el origen, con *checkpoints*
sellados. Ninguna puntuación «declarada» entra en el sistema.

## 2 · Firmado en la máquina
La máquina arma un **pasaporte de sesión** (puntuación, huellas de core/dump/listener,
checkpoints, ticket) y lo **firma** con una clave hardware **no exportable**
(ECDSA P-256). Un byte cambiado después = firma inválida.

## 3 · Verificado en el servidor
El servidor **no repite el juego**: aplica **reglas públicas** (el *CoreVerifier*, open
source) - huellas esperadas, monotonía de la trayectoria, fin de partida, ticket válido
- y emite un veredicto: **publicado**, **retenido** (anomalía estadística, nunca un
rechazo seco) o **rechazado**. Sin árbitro humano.

## 4 · Publicado en un índice firmado
Las puntuaciones publicadas forman un **índice firmado**: la lista completa + una
**huella SHA-256** firmada por el emisor. Ese índice reconstruye la clasificación - y
hace que perder la base de datos sea **irrelevante** (es reconstruible y replicable).

{shot_b}

## 5 · Sellado en Bitcoin
La huella del índice se **sella en Bitcoin** vía **OpenTimestamps**. Una vez confirmada,
prueba que los récords **existían antes de un bloque dado** - anterioridad **inmutable**.
Una puntuación recién sellada se muestra en **oro**; la prueba `.ots` es descargable y
verificable con el cliente OpenTimestamps estándar.

## 6 · El certificado de récord
Cada puntuación tiene una página **inmutable y compartible**: puntuación, huellas del
dump (MD5 + SHA-256), firma ✓ y el **sello Bitcoin** (bloque). Sin rango - el rango vive
en la clasificación.

{shot_c}

## 7 · Verificable sin confiar en nosotros
El **verificador público** recalcula la huella, **verifica la firma** (Web Crypto) y lee
el estado del sello - **en tu navegador**. No da nada por sentado. Incluso puedes
**alojarlo tú mismo**.

{shot_v}

[Verificar ahora →]({VERIFY}){{ .md-button .md-button--primary }}
[Alojar el verificador →](heberger-le-verifieur.md){{ .md-button }}

## El límite, dicho con honestidad
El protocolo abierto **no prueba matemáticamente** que el listener cerrado *leyó* la
dirección correcta. Prueba que el **build homologado estaba presente, ligado al proceso
correcto, sin modificar**, y que se aplicaron las **reglas públicas**. La confianza en la
*medición* viene de un listener **homologado, firmado, versionado, auditado** - ver
[Transparencia](transparence.md) y [Homologación](homologation.md).
""",
     'ja':f"""# 認証された記録

**誰も改ざんできない**レトロスコアの**公開ランキング** - そして**誰でも検証**でき、私た
ちを信用する必要はありません。プレイから Bitcoin 上の証明まで、起きることのすべてです。

[ライブランキングを見る →]({RECORDS}){{ .md-button .md-button--primary }}
[自分で検証する →]({VERIFY}){{ .md-button }}

## 信頼の連鎖（概観）

{chain}

各ステップは**公開・再現可能**か、**認定・署名済み**のいずれかです。安全性は秘密ではなく
**公開**にのみ基づきます（ケルクホフスの原理）。

## 1 · 申告ではなく計測
スコアは**ゲームが送るのではありません**。**認定コンポーネント**（*リスナー*）がエミュ
レータのメモリから、発生源で、タイムスタンプ付き*チェックポイント*とともに直接読み取り
ます。「申告」スコアは一切入りません。

## 2 · 端末で署名
端末は**セッションパスポート**（スコア、コア/ダンプ/リスナーの指紋、チェックポイント、
チケット）を組み立て、**非エクスポート**のハードウェア鍵（ECDSA P-256）で**署名**します。
後から 1 バイトでも変えれば署名は無効です。

## 3 · サーバーで検証
サーバーは**ゲームを再実行しません**。**公開ルール**（オープンソースの *CoreVerifier*）
-期待される指紋、軌跡の単調性、ゲーム終了、有効なチケット-を適用し、**公開** /
**保留**（統計的異常。頭ごなしの却下はしない）/ **却下** の判定を返します。人間の審判は
いません。

## 4 · 署名付きインデックスに公開
公開スコアは**署名付きインデックス**を成します。全リスト + 発行者が署名した **SHA-256
指紋**。このインデックスがランキングを再構築し、データベース喪失を**無意味**にします
（再構築・ミラー可能）。

{shot_b}

## 5 · Bitcoin に封印
インデックスの指紋を **OpenTimestamps** で **Bitcoin に刻印**します。確認されると、記録が
**ある特定のブロック以前に存在した**ことを証明します - **不変**の先行性。封印直後のスコア
は**金色**で表示され、`.ots` 証明はダウンロードでき、標準 OpenTimestamps クライアントで
検証できます。

## 6 · 記録証明書
各スコアには**不変で共有可能**なページがあります。スコア、ダンプ指紋（MD5 + SHA-256）、
署名 ✓、そして **Bitcoin 封印**（ブロック）。順位は載せません - 順位はランキングにあります。

{shot_c}

## 7 · 私たちを信用せず検証可能
**公開検証ツール**は指紋を再計算し、**署名を検証**（Web Crypto）し、封印状態を読みます -
**あなたのブラウザ内で**。何も鵜呑みにしません。**自分でホスト**することもできます。

{shot_v}

[今すぐ検証 →]({VERIFY}){{ .md-button .md-button--primary }}
[検証ツールをホスト →](heberger-le-verifieur.md){{ .md-button }}

## 正直な限界
オープンプロトコルは、閉じたリスナーが正しいアドレスを*読んだ*ことを**数学的には証明しま
せん**。証明するのは、**認定ビルドが存在し、正しいプロセスに結び付き、改変されていない**
こと、そして**公開ルールが適用された**ことです。*計測*への信頼は、**認定・署名・版管理・
監査**されたリスナーに由来します - [透明性](transparence.md)・[認定](homologation.md)参照。
""",
     'zh':f"""# 认证记录

一个**无人能造假**的复古分数**公开排行榜** - 而且**任何人都能验证**，无需信任我们。以下
是从游玩到 Bitcoin 上证明的全过程。

[查看实时排行榜 →]({RECORDS}){{ .md-button .md-button--primary }}
[亲自验证 →]({VERIFY}){{ .md-button }}

## 信任链一览

{chain}

每一步要么**公开且可重放**，要么**已认证并签名**。安全性**从不**依赖秘密（柯克霍夫斯原
则），只依赖开放。

## 1 · 测量，而非申报
分数**不由游戏发送**。一个**认证组件**（*监听器*）直接从模拟器内存中、在源头、带时间戳的
*检查点*读取。任何“申报”分数都不会进入系统。

## 2 · 在本机签名
本机组装**会话护照**（分数，核心/转储/监听器指纹，检查点，票据），并用**不可导出**的硬件
密钥（ECDSA P-256）**签名**。事后改动一个字节 = 签名无效。

## 3 · 服务器端校验
服务器**不重放游戏**：它应用**公开规则**（开源的 *CoreVerifier*）-预期指纹、轨迹单调
性、游戏结束、有效票据-然后给出裁决：**发布**、**保留**（统计异常，绝不硬性拒绝）或
**拒绝**。没有人工裁判。

## 4 · 发布进签名索引
已发布分数构成**签名索引**：完整清单 + 由签发者签名的 **SHA-256 指纹**。该索引重建排行
榜，并使数据库丢失**无关紧要**（可重建、可镜像）。

{shot_b}

## 5 · 封印于 Bitcoin
索引指纹通过 **OpenTimestamps** **盖时间戳于 Bitcoin**。一经确认，即证明记录**存在于某个
区块之前** - **不可变**的先后。刚封印的分数显示为**金色**；`.ots` 证明可下载，并用标准
OpenTimestamps 客户端验证。

## 6 · 记录证书
每个分数都有**不可变、可分享**的页面：分数、转储指纹（MD5 + SHA-256）、签名 ✓，以及
**Bitcoin 封印**（区块）。上面没有排名 - 排名在排行榜上。

{shot_c}

## 7 · 无需信任我们即可验证
**公开验证器**重算指纹、**验证签名**（Web Crypto）并读取封印状态 - **在你的浏览器中**。
它绝不轻信。你甚至可以**自行托管**。

{shot_v}

[立即验证 →]({VERIFY}){{ .md-button .md-button--primary }}
[自行托管验证器 →](heberger-le-verifieur.md){{ .md-button }}

## 诚实的边界
开放协议**不能在数学上证明**闭源监听器*读取了*正确地址。它证明的是**认证构建存在、绑定到
正确进程、未被修改**，以及**应用了公开规则**。对*测量*的信任来自一个**已认证、已签名、有
版本、经审计**的监听器 - 见[透明度](transparence.md)与[认证](homologation.md)。
""",
     'ko':f"""# 인증된 기록

**누구도 조작할 수 없는** 레트로 점수 **공개 순위표** - 그리고 우리를 믿지 않고도 **누구나
검증**할 수 있습니다. 플레이부터 Bitcoin 상의 증명까지, 일어나는 모든 것입니다.

[실시간 순위 보기 →]({RECORDS}){{ .md-button .md-button--primary }}
[직접 검증하기 →]({VERIFY}){{ .md-button }}

## 신뢰의 사슬 한눈에

{chain}

각 단계는 **공개·재현 가능**하거나 **인증·서명**되어 있습니다. 보안은 비밀이 아니라
**공개**에만 기반합니다(케르크호프스 원리).

## 1 · 신고가 아니라 측정
점수는 **게임이 보내지 않습니다**. **인증 구성요소**(*리스너*)가 에뮬레이터 메모리에서,
원천에서, 타임스탬프가 찍힌 *체크포인트*와 함께 직접 읽습니다. “신고” 점수는 시스템에
들어오지 않습니다.

## 2 · 기기에서 서명
기기는 **세션 패스포트**(점수, 코어/덤프/리스너 지문, 체크포인트, 티켓)를 만들고
**비추출** 하드웨어 키(ECDSA P-256)로 **서명**합니다. 이후 1바이트라도 바뀌면 서명 무효.

## 3 · 서버에서 검증
서버는 **게임을 재실행하지 않습니다**. **공개 규칙**(오픈소스 *CoreVerifier*) - 기대 지문,
궤적 단조성, 게임 종료, 유효 티켓 - 을 적용하고 **게시** / **보류**(통계 이상, 즉시 거부는
없음) / **거부** 판정을 내립니다. 사람 심판은 없습니다.

## 4 · 서명된 인덱스에 게시
게시된 점수는 **서명된 인덱스**를 이룹니다. 전체 목록 + 발행자가 서명한 **SHA-256 지문**.
이 인덱스가 순위를 재구성하며, 데이터베이스 손실을 **무의미**하게 만듭니다(재구성·미러
가능).

{shot_b}

## 5 · Bitcoin에 봉인
인덱스 지문을 **OpenTimestamps**로 **Bitcoin에 타임스탬프**합니다. 확인되면 기록이 **특정
블록 이전에 존재**했음을 증명합니다 - **불변**의 선후. 갓 봉인된 점수는 **금색**으로
표시되며, `.ots` 증명은 다운로드하여 표준 OpenTimestamps 클라이언트로 검증할 수 있습니다.

## 6 · 기록 증명서
각 점수에는 **불변·공유 가능**한 페이지가 있습니다. 점수, 덤프 지문(MD5 + SHA-256),
서명 ✓, 그리고 **Bitcoin 봉인**(블록). 순위는 없습니다 - 순위는 순위표에 있습니다.

{shot_c}

## 7 · 우리를 믿지 않고 검증 가능
**공개 검증기**는 지문을 재계산하고 **서명을 검증**(Web Crypto)하며 봉인 상태를 읽습니다 -
**당신의 브라우저에서**. 아무것도 곧이곧대로 받아들이지 않습니다. **직접 호스팅**할 수도
있습니다.

{shot_v}

[지금 검증 →]({VERIFY}){{ .md-button .md-button--primary }}
[검증기 호스팅 →](heberger-le-verifieur.md){{ .md-button }}

## 정직한 한계
오픈 프로토콜은 닫힌 리스너가 올바른 주소를 *읽었다*는 것을 **수학적으로 증명하지
않습니다**. 증명하는 것은 **인증 빌드가 존재했고, 올바른 프로세스에 묶였으며, 수정되지
않았고**, **공개 규칙이 적용**되었다는 것입니다. *측정*에 대한 신뢰는 **인증·서명·버전
관리·감사**된 리스너에서 옵니다 - [투명성](transparence.md), [인증](homologation.md) 참조.
""",
    }
    return T[lng]

for lng in LANGS:
    write('records', lng, records(lng))
    print('records', lng)
