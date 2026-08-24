#!/usr/bin/env python3
# heberger-le-verifieur (self-host) + index, en 6 langues.
import os
here = os.path.dirname(os.path.abspath(__file__))
LANGS = ['fr','en','es','ja','zh','ko']
VERIFY = "https://nelfeplay.com/verify/"
PACK   = "https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer"

def write(page, lng, body):
    name = f"{page}.md" if lng=='fr' else f"{page}.{lng}.md"
    open(os.path.join(here,name),'w',encoding='utf-8').write(body.strip()+"\n")

# ── héberger le vérifieur (pack self-host) ──────────────────────────────────────
HEB = {
 'fr':f"""# Héberger le vérifieur

Le vérifieur est un **fichier HTML autonome**. **N'importe qui peut l'héberger,
n'importe où** - et comme tout est recalculé dans le navigateur du visiteur, l'héberger
**ne réduit pas la confiance** : le visiteur re-vérifie tout lui-même.

[Le pack sur GitHub →]({PACK}){{ .md-button .md-button--primary }}

## Le pack `records-viewer/`
| Fichier | Rôle |
|---|---|
| `verify.html` | Le **vérifieur** : recalcule l'empreinte et **vérifie la signature ECDSA P-256** dans le navigateur, puis lit l'état du sceau Bitcoin. Zéro serveur, zéro build, zéro dépendance. |
| `mirror.sh` | Prend un **instantané durable** (`snapshot/`) - index signé, ancres, et chaque preuve `.ots` - pour que les records restent prouvables **même si nelfeplay.com disparaît**. |

## L'héberger (30 secondes)
`verify.html` est un simple fichier statique :

- **GitHub Pages / Netlify / Cloudflare Pages** - déposez le fichier.
- **En local** - ouvrez `verify.html`, ou `python3 -m http.server`.
- **Hors-ligne / archive** - lancez `./mirror.sh` d'abord, gardez le dossier.

Il lit l'**API publique** de `nelfeplay.com` (CORS activé).

## Deux modes
| Mode | Ce qu'il fait | Intérêt |
|---|---|---|
| **Direct** | interroge l'API en direct | Zéro config, toujours à jour |
| **Instantané** | vérifie contre une copie locale (`mirror.sh`) | **Résistant à la censure** : marche même si le site disparaît |

Le mode instantané rend « immuable » **vraiment** vrai : tant que vous gardez le dossier,
les records restent prouvables - pour toujours, sans nous.

## Construire son propre vérifieur
Vous n'avez même pas besoin de notre fichier - l'API est **publique et signée**.

| Endpoint | Renvoie |
|---|---|
| `GET /api/v1/scores/index` | l'index signé : `records`, `root` (SHA-256 des lignes canoniques), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | les ancres : `generation`, `root_sha256`, `bitcoin_block`, dates |
| `GET /api/v1/scores/anchor-proof?generation=N` | la preuve `.ots` (base64) d'une génération |

Les trois envoient `Access-Control-Allow-Origin: *`. L'algorithme de vérification et la
canonicalisation (JCS, RFC 8785) sont dans `ref/` de ce dépôt.
""",
 'en':f"""# Host the verifier

The verifier is a **self-contained HTML file**. **Anyone can host it, anywhere** - and
because everything is recomputed in the visitor's browser, hosting it **does not reduce
trust**: the visitor re-verifies everything.

[The pack on GitHub →]({PACK}){{ .md-button .md-button--primary }}

## The `records-viewer/` pack
| File | What it does |
|---|---|
| `verify.html` | The **verifier**: recomputes the fingerprint and **verifies the ECDSA P-256 signature** in the browser, then reads the Bitcoin seal state. No server, no build, no dependency. |
| `mirror.sh` | Takes a **durable snapshot** (`snapshot/`) - signed index, anchors, every `.ots` proof - so the records stay provable **even if nelfeplay.com disappears**. |

## Host it (30 seconds)
`verify.html` is just a static file:

- **GitHub Pages / Netlify / Cloudflare Pages** - drop the file.
- **Locally** - open `verify.html`, or `python3 -m http.server`.
- **Offline / archival** - run `./mirror.sh` first, keep the folder.

It reads the **public API** at `nelfeplay.com` (CORS-enabled).

## Two modes
| Mode | What it does | Why |
|---|---|---|
| **Live** | queries the live API | Zero config, always current |
| **Snapshot** | verifies against a local copy (`mirror.sh`) | **Censorship-resistant**: works even if the site disappears |

Snapshot mode makes "immutable" **truly** true: as long as you keep the folder, the
records stay provable - forever, without us.

## Build your own verifier
You don't even need our file - the API is **public and signed**.

| Endpoint | Returns |
|---|---|
| `GET /api/v1/scores/index` | signed index: `records`, `root` (SHA-256 of canonical lines), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | anchors: `generation`, `root_sha256`, `bitcoin_block`, timestamps |
| `GET /api/v1/scores/anchor-proof?generation=N` | the `.ots` proof (base64) for a generation |

All three send `Access-Control-Allow-Origin: *`. The verification algorithm and the
canonicalization (JCS, RFC 8785) live in this repo's `ref/`.
""",
 'es':f"""# Alojar el verificador

El verificador es un **archivo HTML autónomo**. **Cualquiera puede alojarlo, donde
sea** - y como todo se recalcula en el navegador del visitante, alojarlo **no reduce la
confianza**: el visitante lo re-verifica todo.

[El pack en GitHub →]({PACK}){{ .md-button .md-button--primary }}

## El pack `records-viewer/`
| Archivo | Rol |
|---|---|
| `verify.html` | El **verificador**: recalcula la huella y **verifica la firma ECDSA P-256** en el navegador, luego lee el estado del sello Bitcoin. Sin servidor, sin build, sin dependencias. |
| `mirror.sh` | Toma una **instantánea duradera** (`snapshot/`) - índice firmado, anclas y cada prueba `.ots` - para que los récords sigan siendo demostrables **aunque nelfeplay.com desaparezca**. |

## Alojarlo (30 segundos)
`verify.html` es solo un archivo estático:

- **GitHub Pages / Netlify / Cloudflare Pages** - sube el archivo.
- **En local** - abre `verify.html`, o `python3 -m http.server`.
- **Sin conexión / archivo** - ejecuta `./mirror.sh` primero, guarda la carpeta.

Lee la **API pública** de `nelfeplay.com` (CORS activado).

## Dos modos
| Modo | Qué hace | Por qué |
|---|---|---|
| **En vivo** | consulta la API en vivo | Cero configuración, siempre al día |
| **Instantánea** | verifica contra una copia local (`mirror.sh`) | **Resistente a la censura**: funciona aunque el sitio desaparezca |

El modo instantánea hace que «inmutable» sea **de verdad** cierto: mientras guardes la
carpeta, los récords siguen siendo demostrables - para siempre, sin nosotros.

## Crea tu propio verificador
Ni siquiera necesitas nuestro archivo - la API es **pública y firmada**.

| Endpoint | Devuelve |
|---|---|
| `GET /api/v1/scores/index` | índice firmado: `records`, `root` (SHA-256 de líneas canónicas), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | anclas: `generation`, `root_sha256`, `bitcoin_block`, fechas |
| `GET /api/v1/scores/anchor-proof?generation=N` | la prueba `.ots` (base64) de una generación |

Los tres envían `Access-Control-Allow-Origin: *`. El algoritmo de verificación y la
canonicalización (JCS, RFC 8785) están en `ref/` de este repositorio.
""",
 'ja':f"""# 検証ツールをホストする

検証ツールは**自己完結型の HTML ファイル**です。**誰でも、どこでもホスト**できます。すべ
ては訪問者のブラウザで再計算されるため、ホストしても**信頼は下がりません** - 訪問者が自分
で全部を再検証します。

[GitHub のパック →]({PACK}){{ .md-button .md-button--primary }}

## `records-viewer/` パック
| ファイル | 役割 |
|---|---|
| `verify.html` | **検証ツール**：ブラウザ内で指紋を再計算し **ECDSA P-256 署名を検証**、続いて Bitcoin 封印の状態を読む。サーバー不要・ビルド不要・依存なし。 |
| `mirror.sh` | **恒久スナップショット**（`snapshot/`）を取得 - 署名付きインデックス、アンカー、各 `.ots` 証明 - **nelfeplay.com が消えても**記録を証明可能に保つ。 |

## ホスト方法（30 秒）
`verify.html` は単なる静的ファイルです：

- **GitHub Pages / Netlify / Cloudflare Pages** - ファイルを置くだけ。
- **ローカル** - `verify.html` を開く、または `python3 -m http.server`。
- **オフライン / アーカイブ** - 先に `./mirror.sh` を実行し、フォルダを保管。

`nelfeplay.com` の**公開 API**（CORS 有効）を読みます。

## 2 つのモード
| モード | 内容 | 意義 |
|---|---|---|
| **ライブ** | ライブ API を参照 | 設定ゼロ、常に最新 |
| **スナップショット** | ローカルコピーで検証（`mirror.sh`） | **検閲耐性**：サイトが消えても動作 |

スナップショットモードは「不変」を**本当に**不変にします。フォルダを保管する限り、記録は
証明可能なまま - 永久に、私たち抜きで。

## 自分の検証ツールを作る
私たちのファイルすら不要です - API は**公開・署名済み**です。

| エンドポイント | 返すもの |
|---|---|
| `GET /api/v1/scores/index` | 署名付きインデックス：`records`、`root`（正規化行の SHA-256）、`signature`（ECDSA P-256, base64url DER）、`issuer_public_key`（SPKI PEM） |
| `GET /api/v1/scores/anchors` | アンカー：`generation`、`root_sha256`、`bitcoin_block`、日時 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 世代の `.ots` 証明（base64） |

3 つとも `Access-Control-Allow-Origin: *` を返します。検証アルゴリズムと正規化（JCS,
RFC 8785）は本リポジトリの `ref/` にあります。
""",
 'zh':f"""# 自行托管验证器

验证器是一个**自包含的 HTML 文件**。**任何人都能在任何地方托管它** - 由于一切都在访问者
的浏览器中重算，托管它**不会降低信任**：访问者会自行重新验证一切。

[GitHub 上的工具包 →]({PACK}){{ .md-button .md-button--primary }}

## `records-viewer/` 工具包
| 文件 | 作用 |
|---|---|
| `verify.html` | **验证器**：在浏览器中重算指纹并**验证 ECDSA P-256 签名**，然后读取 Bitcoin 封印状态。无服务器、无构建、无依赖。 |
| `mirror.sh` | 生成**持久快照**（`snapshot/`）- 签名索引、锚点及每份 `.ots` 证明 - 使记录**即使 nelfeplay.com 消失**也可证明。 |

## 托管它（30 秒）
`verify.html` 只是一个静态文件：

- **GitHub Pages / Netlify / Cloudflare Pages** - 放上文件即可。
- **本地** - 打开 `verify.html`，或 `python3 -m http.server`。
- **离线 / 存档** - 先运行 `./mirror.sh`，保留该文件夹。

它读取 `nelfeplay.com` 的**公开 API**（已启用 CORS）。

## 两种模式
| 模式 | 作用 | 意义 |
|---|---|---|
| **实时** | 查询实时 API | 零配置，始终最新 |
| **快照** | 对本地副本验证（`mirror.sh`） | **抗审查**：即使网站消失也能运行 |

快照模式让“不可变”**真正**成立：只要你保留该文件夹，记录就始终可证明 - 永远，无需我们。

## 构建你自己的验证器
你甚至不需要我们的文件 - API 是**公开且签名**的。

| 端点 | 返回 |
|---|---|
| `GET /api/v1/scores/index` | 签名索引：`records`、`root`（规范化行的 SHA-256）、`signature`（ECDSA P-256，base64url DER）、`issuer_public_key`（SPKI PEM） |
| `GET /api/v1/scores/anchors` | 锚点：`generation`、`root_sha256`、`bitcoin_block`、时间 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 某代的 `.ots` 证明（base64） |

三者都发送 `Access-Control-Allow-Origin: *`。验证算法与规范化（JCS, RFC 8785）位于本仓库
的 `ref/`。
""",
 'ko':f"""# 검증기 호스팅

검증기는 **자기 완결형 HTML 파일**입니다. **누구나, 어디서나 호스팅**할 수 있습니다. 모든
것이 방문자의 브라우저에서 재계산되므로, 호스팅해도 **신뢰가 낮아지지 않습니다** - 방문자가
직접 전부를 재검증합니다.

[GitHub의 팩 →]({PACK}){{ .md-button .md-button--primary }}

## `records-viewer/` 팩
| 파일 | 역할 |
|---|---|
| `verify.html` | **검증기**: 브라우저에서 지문을 재계산하고 **ECDSA P-256 서명을 검증**한 뒤 Bitcoin 봉인 상태를 읽음. 서버·빌드·의존성 없음. |
| `mirror.sh` | **영구 스냅샷**(`snapshot/`)을 만듦 - 서명 인덱스, 앵커, 각 `.ots` 증명 - **nelfeplay.com이 사라져도** 기록을 증명 가능하게 유지. |

## 호스팅하기 (30초)
`verify.html`은 그냥 정적 파일입니다:

- **GitHub Pages / Netlify / Cloudflare Pages** - 파일을 올리세요.
- **로컬** - `verify.html`을 열거나 `python3 -m http.server`.
- **오프라인 / 보관** - 먼저 `./mirror.sh`를 실행하고 폴더를 보관.

`nelfeplay.com`의 **공개 API**(CORS 허용)를 읽습니다.

## 두 가지 모드
| 모드 | 하는 일 | 이유 |
|---|---|---|
| **라이브** | 라이브 API 조회 | 설정 없음, 항상 최신 |
| **스냅샷** | 로컬 사본으로 검증(`mirror.sh`) | **검열 저항**: 사이트가 사라져도 동작 |

스냅샷 모드는 “불변”을 **진짜로** 불변으로 만듭니다. 폴더를 보관하는 한 기록은 증명 가능한
채로 남습니다 - 영원히, 우리 없이.

## 자신만의 검증기 만들기
우리 파일조차 필요 없습니다 - API는 **공개·서명**되어 있습니다.

| 엔드포인트 | 반환 |
|---|---|
| `GET /api/v1/scores/index` | 서명 인덱스: `records`, `root`(정규화 행의 SHA-256), `signature`(ECDSA P-256, base64url DER), `issuer_public_key`(SPKI PEM) |
| `GET /api/v1/scores/anchors` | 앵커: `generation`, `root_sha256`, `bitcoin_block`, 시간 |
| `GET /api/v1/scores/anchor-proof?generation=N` | 해당 세대의 `.ots` 증명(base64) |

셋 다 `Access-Control-Allow-Origin: *`를 보냅니다. 검증 알고리즘과 정규화(JCS, RFC 8785)는
이 저장소의 `ref/`에 있습니다.
""",
}
for lng in LANGS:
    write('heberger-le-verifieur', lng, HEB[lng])
    print('heberger', lng)
