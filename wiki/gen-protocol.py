#!/usr/bin/env python3
# Traductions en/es/ja/zh/ko des 3 pages protocole (le FR existe déjà).
import os
here=os.path.dirname(os.path.abspath(__file__))
def write(page,lng,body): open(os.path.join(here,f"{page}.{lng}.md"),'w',encoding='utf-8').write(body.strip()+"\n")

BOUND = """```
RetroArch
   │  ▼
NelfeMemoryListener  - CLOSED · HOMOLOGATED ----------------
   reads memory, resolves addresses, computes score+counters,
   emits raw checkpoints
   │  ▼  normalized event { score, counters, frame, time, event }
Open protocol (this repo)  - PUBLIC ------------------------
   ticket · JCS canonicalization · passport · signature · verify · submit
```"""

TRANS = {
 'en':f"""# Transparency: what is open, what is not

Our transparency is about **how NelfePlay decides**, not **how the listener extracts the
signal**. That distinction is deliberate.

## The trust boundary
{BOUND}
The public code knows how to verify the **continuity** and **consistency** of these
events; it does **not** know how they were obtained.

## Why the listener is closed
Memory-reading logic is expensive know-how (one definition per game, re-validated on
every core change). Opening it would hand it to competitors **and** help cheaters. We
keep it closed - like the firmware of a measuring instrument.

## What closure is NOT
Closure is **not part of the security** (Kerckhoffs' principle). The system's security
rests **only** on the secrecy of the **device signing key** - never on secret rules. All
rules, all checks, all refusal codes are **public**. If the listener code leaked
tomorrow, the guarantee would not change by an inch: it comes from the open.

## The honest limit
The open protocol **will never mathematically prove** the listener *actually* read
memory. It proves, verifiably: the **homologated build** (known hash) was **present**,
**bound to the right process**, **unmodified** during the session; the events were **not
altered** after emission (signature); and the server applied **the public rules**.

Trust in the *measurement* therefore rests on a listener that is **homologated, signed,
versioned and audited** - see [Homologation](homologation.md).

## What stays 100% public
Passport format · tickets · manifest · profile rules · allowed fingerprints · signature
verification · submission states · ranking rules · **OpenTimestamps-on-Bitcoin
anchoring** · **refusal codes** · the **public verifier** · the listener's
**homologation-suite results**.

## A promise we can keep
> "NelfePlay's rules and verification are public and replayable. The memory measurement
> is done by a proprietary listener that is homologated, signed, versioned and audited."

Not "cheating is mathematically impossible" - that would be false for software running on
the player's PC. But a **precise, accountable** guarantee beats an unverifiable promise.
""",
 'es':f"""# Transparencia: qué es abierto y qué no

Nuestra transparencia trata de **cómo decide NelfePlay**, no de **cómo el listener extrae
la señal**. Es una distinción deliberada.

## La frontera de confianza
{BOUND}
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
""",
 'ja':f"""# 透明性：何が公開で、何が非公開か

私たちの透明性は、**NelfePlay がどう判断するか**についてであり、**リスナーがどう信号を抽出
するか**ではありません。これは意図的な区別です。

## 信頼の境界
{BOUND}
公開コードはこれらのイベントの**連続性**と**整合性**を検証できますが、それがどう得られた
かは**知りません**。

## なぜリスナーは非公開か
メモリ読み取りのロジックは高価なノウハウです（ゲームごとの定義、コア更新のたびに再検証）。
公開すれば競合に渡り、**かつ**チートを助けます。だから計測器のファームウェアのように閉じて
います。

## 「非公開」が意味しないこと
非公開は**セキュリティの一部ではありません**（ケルクホフスの原理）。システムの安全性は
**端末の署名鍵**の秘密**のみ**に依存し、秘密のルールには依存しません。すべてのルール・検査・
却下コードは**公開**です。仮にリスナーのコードが流出しても、保証は一切変わりません。保証は
公開に由来するからです。

## 正直な限界
オープンプロトコルはリスナーが*実際に*メモリを読んだことを**数学的には決して証明しません**。
検証可能に証明するのは：**認定ビルド**（既知のハッシュ）が**存在**し、**正しいプロセスに結び
付き**、セッション中**改変されていない**こと。イベントが発行後**改変されていない**こと（署名）。
そしてサーバーが**公開ルール**を適用したこと。

したがって*計測*への信頼は、**認定・署名・版管理・監査**されたリスナーに基づきます -
[認定](homologation.md)参照。

## 100% 公開のまま
パスポート形式・チケット・マニフェスト・プロファイル規則・許可指紋・署名検証・提出状態・
ランキング規則・**OpenTimestamps による Bitcoin アンカー**・**却下コード**・**公開検証
ツール**・リスナーの**認定スイート結果**。

## 守れる約束
> 「NelfePlay のルールと検証は公開・再現可能。メモリ計測は、認定・署名・版管理・監査された
> 専有リスナーが行う。」

「チートは数学的に不可能」ではありません - プレイヤーの PC 上で動くソフトには偽りです。しかし
**正確で説明責任のある**保証は、検証できない約束に勝ります。
""",
 'zh':f"""# 透明度：何为开放，何为不开放

我们的透明度关乎 **NelfePlay 如何裁决**，而非**监听器如何提取信号**。这是有意的区分。

## 信任边界
{BOUND}
公开代码知道如何验证这些事件的**连续性**与**一致性**；它**不知道**它们是如何获得的。

## 为何监听器闭源
内存读取逻辑是昂贵的专有技术（每款游戏一份定义，每次核心更新都要重新验证）。开放它会拱手
让给竞争者，**并且**帮助作弊者。因此我们像计量仪器的固件一样将其闭源。

## 闭源“不是”什么
闭源**不属于安全性**（柯克霍夫斯原则）。系统安全**仅**依赖**本机签名密钥**的保密-绝不依赖
秘密规则。所有规则、检查、拒绝码都是**公开**的。即便明天监听器代码泄露，保证也丝毫不变：它
来自开放。

## 诚实的边界
开放协议**永远无法在数学上证明**监听器*确实*读取了内存。它可验证地证明：**认证构建**（已知
哈希）**存在**、**绑定到正确进程**、会话期间**未被修改**；事件在发出后**未被篡改**（签名）；
以及服务器应用了**公开规则**。

因此对*测量*的信任，建立在一个**已认证、已签名、有版本、经审计**的监听器之上-见
[认证](homologation.md)。

## 保持 100% 公开的
护照格式 · 票据 · 清单 · 配置规则 · 允许的指纹 · 签名验证 · 提交状态 · 排名规则 ·
**OpenTimestamps 于 Bitcoin 的锚定** · **拒绝码** · **公开验证器** · 监听器的
**认证套件结果**。

## 一个我们能兑现的承诺
> “NelfePlay 的规则与验证是公开且可重放的。内存测量由一个已认证、已签名、有版本、经审计的
> 专有监听器完成。”

不是“作弊在数学上不可能”-对运行于玩家 PC 上的软件而言那是虚假的。但一个**精确、可追责**的
保证，胜过无法验证的承诺。
""",
 'ko':f"""# 투명성: 무엇이 공개이고 무엇이 아닌가

우리의 투명성은 **NelfePlay가 어떻게 판정하는가**에 관한 것이지, **리스너가 어떻게 신호를
추출하는가**가 아닙니다. 이는 의도된 구분입니다.

## 신뢰 경계
{BOUND}
공개 코드는 이 이벤트들의 **연속성**과 **일관성**을 검증할 줄 압니다. 그것들이 어떻게
얻어졌는지는 **알지 못합니다**.

## 왜 리스너는 비공개인가
메모리 읽기 로직은 값비싼 노하우입니다(게임마다 정의, 코어 변경마다 재검증). 공개하면
경쟁자에게 넘어가고 **동시에** 부정행위를 돕습니다. 그래서 계측기 펌웨어처럼 닫아 둡니다.

## 비공개가 아닌 것
비공개는 **보안의 일부가 아닙니다**(케르크호프스 원리). 시스템 보안은 **기기 서명 키**의
비밀에**만** 의존하며, 비밀 규칙에는 의존하지 않습니다. 모든 규칙·검사·거부 코드는
**공개**입니다. 내일 리스너 코드가 유출되어도 보장은 조금도 변하지 않습니다. 보장은 공개에서
오기 때문입니다.

## 정직한 한계
오픈 프로토콜은 리스너가 *실제로* 메모리를 읽었음을 **결코 수학적으로 증명하지 않습니다**.
검증 가능하게 증명하는 것은: **인증 빌드**(알려진 해시)가 **존재**했고, **올바른 프로세스에
묶였으며**, 세션 중 **수정되지 않았고**; 이벤트가 발행 후 **변조되지 않았으며**(서명); 서버가
**공개 규칙**을 적용했다는 것입니다.

따라서 *측정*에 대한 신뢰는 **인증·서명·버전 관리·감사**된 리스너에 기반합니다 -
[인증](homologation.md) 참조.

## 100% 공개로 유지되는 것
패스포트 형식 · 티켓 · 매니페스트 · 프로필 규칙 · 허용 지문 · 서명 검증 · 제출 상태 · 순위
규칙 · **OpenTimestamps의 Bitcoin 앵커링** · **거부 코드** · **공개 검증기** · 리스너의
**인증 스위트 결과**.

## 지킬 수 있는 약속
> “NelfePlay의 규칙과 검증은 공개·재현 가능하다. 메모리 측정은 인증·서명·버전 관리·감사된
> 독점 리스너가 수행한다.”

“부정행위가 수학적으로 불가능”이 아닙니다 - 플레이어 PC에서 도는 소프트웨어에는 거짓입니다.
그러나 **정확하고 책임 있는** 보장이 검증 불가능한 약속보다 낫습니다.
""",
}

VERIF = {
 'en':"""# Verify a score yourself

You don't have to take our word for it. Three independent checks.

## 1. Replay the verifier on the test vectors
The **vectors** (`vectors/*.json`) are **(passport, expected verdict)** pairs. The public
verifier (`ref/`) must return **exactly** those verdicts - the same verdict, byte for
byte, in every implementation (C#, PHP, C++…). That is the protocol's exit criterion.

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 vectors at the expected verdict
```

## 2. Verify a passport's signature
Every passport is **signed** by the machine (ECDSA P-256) over its **canonical form**
(JSON Canonicalization Scheme, **RFC 8785**):

1. remove the `signature` field;
2. canonicalize the rest in JCS (sorted keys, no spaces, minimal escaping);
3. verify the signature (ASN.1 DER, base64url) with the device public key
   (`key_id = SHA-256(SPKI DER)`).

The signature covers **everything**: score, core/content/MEM/listener fingerprints,
checkpoints, ticket. One byte changed afterwards = invalid signature.

## 3. Verify anteriority (blockchain anchoring)
Every ranked score - and each game's **opening** - is grouped into a Merkle tree whose
root is anchored via **OpenTimestamps on Bitcoin**. With a standard OpenTimestamps
client, anyone can verify, **without us**, that the data existed **before a given Bitcoin
block**.

Anchoring proves **anteriority**, not veracity: it guarantees a record wasn't backdated
before the game's opening, and that a later withdrawal is **also** timestamped (history
grows, it is not rewritten).

## What the three establish together
| Check | What it proves |
|---|---|
| Vectors | The **rules** applied are exactly those published. |
| Signature | The passport was **not altered** and comes from **that machine**. |
| Anchoring | The data **existed before** a Bitcoin block - no backdating. |

What they do not prove: that the closed listener *read* the right memory address. That
trust comes from the [listener homologation](homologation.md).
""",
 'es':"""# Verificar una puntuación tú mismo

No tienes que creernos. Tres comprobaciones independientes.

## 1. Repetir el verificador sobre los vectores de prueba
Los **vectores** (`vectors/*.json`) son pares **(pasaporte, veredicto esperado)**. El
verificador público (`ref/`) debe devolver **exactamente** esos veredictos - el mismo
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
Cada puntuación clasificada - y la **apertura** de cada juego - se agrupa en un árbol de
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
| Anclaje | El dato **existía antes** de un bloque Bitcoin - sin antedatar. |

Lo que no prueban: que el listener cerrado *leyó* la dirección correcta. Esa confianza
viene de la [homologación del listener](homologation.md).
""",
 'ja':"""# 自分でスコアを検証する

私たちの言葉を信じる必要はありません。独立した 3 つの検証です。

## 1. テストベクタで検証ツールを再実行
**ベクタ**（`vectors/*.json`）は **(パスポート, 期待される判定)** の組です。公開検証ツール
（`ref/`）は**厳密に**その判定を返さねばなりません - どの実装（C#, PHP, C++…）でもバイト単位
で同一の判定。これがプロトコルの出口基準です。

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 ベクタが期待判定
```

## 2. パスポートの署名を検証
各パスポートは端末により**正規形**（JSON Canonicalization Scheme, **RFC 8785**）に対して
**署名**されています（ECDSA P-256）：

1. `signature` フィールドを取り除く；
2. 残りを JCS で正規化（キー整列、空白なし、最小エスケープ）；
3. デバイス公開鍵（`key_id = SHA-256(SPKI DER)`）で署名（ASN.1 DER, base64url）を検証。

署名は**すべて**を覆います：スコア、コア/コンテンツ/MEM/リスナーの指紋、チェックポイント、
チケット。後から 1 バイト変えれば署名は無効。

## 3. 先行性を検証（ブロックチェーン・アンカー）
ランクインした各スコア - と各ゲームの**開始** - は Merkle ツリーにまとめられ、その根が
**OpenTimestamps で Bitcoin** にアンカーされます。標準クライアントで、誰でも**私たち抜き**で、
データが**特定の Bitcoin ブロック以前に存在**したことを検証できます。

アンカーは**先行性**を証明し、真偽は証明しません：記録が開始前に遡って作られていないこと、
そして後の取り消しも**同様に**時刻印されること（歴史は増えるだけで書き換えられない）を保証。

## 3 つが合わせて確立すること
| 検証 | 証明すること |
|---|---|
| ベクタ | 適用された**ルール**が公開されたものと完全に一致。 |
| 署名 | パスポートが**改変されておらず**、**その端末**から来た。 |
| アンカー | データが Bitcoin ブロック**以前に存在** - 遡及なし。 |

証明しないこと：閉じたリスナーが正しいメモリアドレスを*読んだ*こと。その信頼は
[リスナーの認定](homologation.md)から来ます。
""",
 'zh':"""# 亲自验证一个分数

无需听我们的一面之词。三项独立检查。

## 1. 在测试向量上重放验证器
**向量**（`vectors/*.json`）是 **(护照, 期望裁决)** 对。公开验证器（`ref/`）必须**精确**返回
这些裁决-每种实现（C#、PHP、C++…）逐字节相同的裁决。这是协议的出口标准。

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 向量达到期望裁决
```

## 2. 验证护照签名
每份护照由本机对其**规范形式**（JSON Canonicalization Scheme, **RFC 8785**）**签名**
（ECDSA P-256）：

1. 移除 `signature` 字段；
2. 将其余部分按 JCS 规范化（键排序、无空格、最小转义）；
3. 用设备公钥（`key_id = SHA-256(SPKI DER)`）验证签名（ASN.1 DER, base64url）。

签名覆盖**一切**：分数，核心/内容/MEM/监听器指纹，检查点，票据。事后改动一个字节 = 签名无效。

## 3. 验证先后性（区块链锚定）
每个上榜分数-以及每款游戏的**开局**-都归入一棵 Merkle 树，其根通过 **OpenTimestamps 锚定
于 Bitcoin**。用标准客户端，任何人都能**在没有我们**的情况下验证数据**存在于某个 Bitcoin 区块
之前**。

锚定证明**先后性**，而非真伪：它保证记录未被回填到开局之前，且后续撤回**同样**带时间戳（历史
只增不改）。

## 三者共同确立
| 检查 | 证明什么 |
|---|---|
| 向量 | 所应用的**规则**正是已公布的。 |
| 签名 | 护照**未被篡改**且来自**那台机器**。 |
| 锚定 | 数据**存在于** Bitcoin 区块**之前**-无回填。 |

它们不证明：闭源监听器*读取了*正确的内存地址。那份信任来自[监听器认证](homologation.md)。
""",
 'ko':"""# 직접 점수 검증하기

우리 말을 믿을 필요 없습니다. 독립적인 세 가지 검사.

## 1. 테스트 벡터로 검증기 재실행
**벡터**(`vectors/*.json`)는 **(패스포트, 예상 판정)** 쌍입니다. 공개 검증기(`ref/`)는
**정확히** 그 판정을 반환해야 합니다 - 모든 구현(C#, PHP, C++…)에서 바이트 단위로 동일한
판정. 이것이 프로토콜의 종료 기준입니다.

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 벡터가 예상 판정
```

## 2. 패스포트 서명 검증
각 패스포트는 기기가 **정규형**(JSON Canonicalization Scheme, **RFC 8785**)에 대해
**서명**합니다(ECDSA P-256):

1. `signature` 필드 제거;
2. 나머지를 JCS로 정규화(키 정렬, 공백 없음, 최소 이스케이프);
3. 기기 공개키(`key_id = SHA-256(SPKI DER)`)로 서명(ASN.1 DER, base64url) 검증.

서명은 **전부**를 덮습니다: 점수, 코어/콘텐츠/MEM/리스너 지문, 체크포인트, 티켓. 이후 1바이트
변경 = 서명 무효.

## 3. 선후성 검증(블록체인 앵커링)
순위에 오른 각 점수 - 그리고 각 게임의 **개시** - 는 Merkle 트리로 묶이고 그 루트가
**OpenTimestamps로 Bitcoin에** 앵커됩니다. 표준 클라이언트로 누구나 **우리 없이** 데이터가
**특정 Bitcoin 블록 이전에 존재**했음을 검증할 수 있습니다.

앵커링은 **선후성**을 증명하지 진위를 증명하지 않습니다: 기록이 개시 이전으로 소급되지 않았고,
이후의 철회도 **마찬가지로** 타임스탬프됨(역사는 늘어날 뿐 다시 쓰이지 않음)을 보장합니다.

## 세 가지가 함께 확립하는 것
| 검사 | 증명하는 것 |
|---|---|
| 벡터 | 적용된 **규칙**이 공개된 것과 정확히 일치. |
| 서명 | 패스포트가 **변조되지 않았고** **그 기기**에서 옴. |
| 앵커링 | 데이터가 Bitcoin 블록 **이전에 존재** - 소급 없음. |

증명하지 않는 것: 닫힌 리스너가 올바른 메모리 주소를 *읽었다*는 것. 그 신뢰는
[리스너 인증](homologation.md)에서 옵니다.
""",
}

HOMO = {
 'en':"""# Listener homologation

The listener (`NelfeMemoryListener`) is the closed component that **measures** the score
in memory. Its credibility comes not from its (secret) code, but from its
**homologation** - like the closed firmware of a measuring instrument (a **technical**
analogy, not a regulatory claim).

## Vocabulary (precise)
- **NelfePlay-homologated**: each official build is signed and attested by the publisher.
- **Audited**: said only when an independent external audit **actually** took place.
- **Certified**: reserved for a real, formal certification program (accredited body). We
  do not use it until such a program exists.

## Public build sheet
Each listener version publishes:
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
Each **scoring profile** references the authorized builds (`allowed_listener_sha256`).
The **passport** carries the listener hash **before / loaded / after** - measured
**independently by the open component** (not by the listener itself, to avoid
self-attestation).

## Homologation suite (black box, public)
Behavior can be proven **without revealing the algorithm**:
> ROM X + scenario Y → the on-screen score is **12,500** → the official listener must
> produce **12,500**.

The results are public; the memory address and how it is read are not.

## Revocation
A flaw in a build? We **revoke that build for new sessions** (`status: revoked`) without
making old scores unreadable: they stay verifiable with the historical profile and build.

## Toward crediting the closed component
Signed binary · **public SHA-256** per build · **external audit under NDA** with a
**public, code-free report** · public **SBOM** · optional source **escrow** · **public
behavioral tests** · **revocation policy** · **version history** · **vulnerability
disclosure program**.

## The limit, again
None of this *mathematically* proves the listener read the right address. It establishes
that a **homologated, unmodified** build was **bound to the right process** and that the
**public rules** were applied. Trust in the measurement rests on homologation - a
defensible basis, the same as real-world measuring instruments.
""",
 'es':"""# Homologación del listener

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
""",
 'ja':"""# リスナーの認定

リスナー（`NelfeMemoryListener`）は、メモリ内でスコアを**計測**する非公開コンポーネントです。
その信頼性は（秘密の）コードではなく、**認定**から来ます - 計測器の非公開ファームウェアのよう
に（**技術的**な類推であり、規制上の主張ではありません）。

## 用語（正確に）
- **NelfePlay 認定**：各公式ビルドは発行者により署名・証明される。
- **監査済み**：独立した外部監査が**実際に**行われた場合にのみ言う。
- **認証済み**：正式な認証プログラム（認定機関）に限定。そうしたプログラムが存在するまでは
  使わない。

## ビルドの公開シート
各リスナー版が公開するもの：
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
各**スコアリングプロファイル**は許可ビルド（`allowed_listener_sha256`）を参照。**パスポート**は
リスナーのハッシュを**前 / 読込 / 後**で保持 - **公開コンポーネントが独立に**計測（自己証明を
避けるため、リスナー自身ではない）。

## 認定スイート（ブラックボックス、公開）
**アルゴリズムを明かさず**に挙動を証明できます：
> ROM X + シナリオ Y → 画面のスコアは **12,500** → 公式リスナーは **12,500** を出さねばならない。

結果は公開；メモリアドレスと読み方は非公開。

## 失効
ビルドに欠陥？ そのビルドを**新規プレイに対して失効**（`status: revoked`）します。過去のスコア
を読めなくすることはありません：歴史的なプロファイルとビルドで検証可能なままです。

## 非公開コンポーネントの信頼性を高めるために
署名済みバイナリ・ビルドごとの**公開 SHA-256**・**NDA 下の外部監査**と**コードなしの公開
報告**・公開 **SBOM**・任意のソース**エスクロー**・**公開の挙動テスト**・**失効ポリシー**・
**版履歴**・**脆弱性開示プログラム**。

## 再び、限界
これらのいずれも、リスナーが正しいアドレスを読んだことを*数学的に*証明しません。**認定・未改変**
のビルドが**正しいプロセスに結び付き**、**公開ルール**が適用されたことを確立します。計測への信頼
は認定に基づきます - 現実の計測器と同じ、擁護可能な基盤です。
""",
 'zh':"""# 监听器认证

监听器（`NelfeMemoryListener`）是在内存中**测量**分数的闭源组件。它的可信度并非来自（保密的）
代码，而是来自其**认证**-如同计量仪器的闭源固件（**技术**类比，而非监管主张）。

## 术语（精确）
- **NelfePlay 认证**：每个官方构建都由发行者签名并背书。
- **已审计**：仅当独立的外部审计**确实**发生时才使用。
- **已认证**：保留给真正的正式认证计划（获授权机构）。在这样的计划存在之前我们不使用它。

## 构建的公开信息表
每个监听器版本发布：
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
每个**计分配置**引用被授权的构建（`allowed_listener_sha256`）。**护照**携带监听器的哈希
**之前 / 加载 / 之后**-由**开放组件独立测量**（而非监听器自身，以避免自我背书）。

## 认证套件（黑盒，公开）
可以在**不泄露算法**的前提下证明行为：
> ROM X + 场景 Y → 屏幕上的分数是 **12,500** → 官方监听器必须产出 **12,500**。

结果公开；内存地址与读取方式不公开。

## 撤销
某个构建有缺陷？我们**对新对局撤销该构建**（`status: revoked`），同时不使旧分数无法解读：它们
仍可用历史配置与构建验证。

## 为闭源组件增信
签名二进制 · 每个构建的**公开 SHA-256** · **NDA 下的外部审计**并附**无代码的公开报告** ·
公开 **SBOM** · 可选的源码**托管** · **公开的行为测试** · **撤销政策** · **版本历史** ·
**漏洞披露计划**。

## 再谈边界
以上都不能*在数学上*证明监听器读取了正确地址。它们确立的是：一个**已认证、未修改**的构建
**绑定到正确进程**，并应用了**公开规则**。对测量的信任建立在认证之上-这是可辩护的基础，与
现实世界的计量仪器相同。
""",
 'ko':"""# 리스너 인증

리스너(`NelfeMemoryListener`)는 메모리에서 점수를 **측정**하는 닫힌 구성요소입니다. 그 신뢰성은
(비밀) 코드가 아니라 **인증**에서 옵니다 - 계측기의 닫힌 펌웨어처럼(**기술적** 비유이며 규제상
주장이 아님).

## 용어(정확히)
- **NelfePlay 인증**: 각 공식 빌드는 발행자가 서명·증명.
- **감사됨**: 독립적인 외부 감사가 **실제로** 있었을 때만 사용.
- **인증됨(Certified)**: 정식 인증 프로그램(공인 기관)에만 사용. 그런 프로그램이 존재하기
  전까지는 쓰지 않음.

## 빌드 공개 시트
각 리스너 버전이 공개하는 것:
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
각 **스코어링 프로필**은 허가된 빌드(`allowed_listener_sha256`)를 참조합니다. **패스포트**는
리스너 해시를 **이전 / 로드됨 / 이후**로 담습니다 - **공개 구성요소가 독립적으로** 측정(자기
증명을 피하기 위해 리스너 자신이 아님).

## 인증 스위트(블랙박스, 공개)
**알고리즘을 드러내지 않고** 동작을 증명할 수 있습니다:
> ROM X + 시나리오 Y → 화면 점수는 **12,500** → 공식 리스너는 **12,500**을 내야 한다.

결과는 공개; 메모리 주소와 읽는 방법은 비공개.

## 폐기(Revocation)
빌드에 결함? 해당 빌드를 **새 세션에 대해 폐기**(`status: revoked`)하되, 과거 점수를 읽을 수
없게 만들지 않습니다: 역사적 프로필과 빌드로 여전히 검증 가능합니다.

## 닫힌 구성요소의 신뢰성을 높이기 위해
서명된 바이너리 · 빌드별 **공개 SHA-256** · **NDA 하의 외부 감사**와 **코드 없는 공개 보고서** ·
공개 **SBOM** · 선택적 소스 **에스크로** · **공개 동작 테스트** · **폐기 정책** · **버전 이력** ·
**취약점 공개 프로그램**.

## 다시, 한계
이 중 어느 것도 리스너가 올바른 주소를 읽었음을 *수학적으로* 증명하지 않습니다. **인증되고
수정되지 않은** 빌드가 **올바른 프로세스에 묶였고** **공개 규칙**이 적용되었음을 확립합니다.
측정에 대한 신뢰는 인증에 기반합니다 - 현실의 계측기와 같은, 방어 가능한 근거입니다.
""",
}

for lng in ['en','es','ja','zh','ko']:
    write('transparence',lng,TRANS[lng])
    write('verifier-un-score',lng,VERIF[lng])
    write('homologation',lng,HOMO[lng])
    print('protocol', lng)
